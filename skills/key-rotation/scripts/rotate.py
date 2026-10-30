#!/usr/bin/env python3
"""Dual-key rotation state machine.

Old key stays live until the new key is minted, dual-written, live-tested,
cut over, and consumer-verified. Only then is the old key retired.

Usage:
  python3 rotate.py --demo
  python3 rotate.py --secret-id technitium --stores-dir ./stores
"""
from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable


PHASES = [
    "inventory",
    "mint",
    "dual_write",
    "verify_new",
    "cutover",
    "verify_consumers",
    "retire_old",
    "reconcile_stores",
]


def fp(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:12]


class RotationError(RuntimeError):
    pass


@dataclass
class SecretState:
    live_alias: str
    v1_name: str
    v2_name: str
    previous_name: str
    v1_value: str | None
    v2_value: str | None
    live_points_to: str
    retired: list[str]


class TwoStoreVault:
    """Minimal model of ember-keyring + Proton Pass."""

    def __init__(self, root: Path):
        self.ember = root / "ember-keyring"
        self.proton = root / "proton-pass"
        self.ember.mkdir(parents=True, exist_ok=True)
        self.proton.mkdir(parents=True, exist_ok=True)

    def _path(self, store: str, name: str) -> Path:
        base = self.ember if store == "ember" else self.proton
        return base / name

    def write(self, store: str, name: str, value: str) -> None:
        p = self._path(store, name)
        p.write_text(value)
        p.chmod(0o600)

    def read(self, store: str, name: str) -> str | None:
        p = self._path(store, name)
        if not p.exists():
            return None
        return p.read_text()

    def delete(self, store: str, name: str) -> None:
        p = self._path(store, name)
        if p.exists():
            p.unlink()

    def alias(self, store: str, alias: str, target: str) -> None:
        # alias is a file containing "alias -> target"
        self.write(store, alias, f"@{target}")

    def resolve(self, store: str, name: str) -> str | None:
        raw = self.read(store, name)
        if raw and raw.startswith("@"):
            return self.read(store, raw[1:])
        return raw

    def drift(self, name: str) -> dict:
        a = self.resolve("ember", name)
        b = self.resolve("proton", name)
        return {
            "ember_fp": fp(a) if a else None,
            "proton_fp": fp(b) if b else None,
            "in_sync": bool(a) and a == b,
        }


class Issuer:
    """Fake issuer so --demo can prove dual-key without a live API."""

    def __init__(self):
        self.valid: set[str] = set()
        self.disabled: set[str] = set()

    def mint(self) -> str:
        token = "tok_" + secrets.token_hex(16)
        self.valid.add(token)
        return token

    def accept(self, token: str) -> bool:
        return token in self.valid and token not in self.disabled

    def disable(self, token: str) -> None:
        self.disabled.add(token)


class Rotator:
    def __init__(
        self,
        secret_id: str,
        vault: TwoStoreVault,
        issuer: Issuer,
        consumer_probe: Callable[[str], bool] | None = None,
    ):
        self.secret_id = secret_id
        self.vault = vault
        self.issuer = issuer
        self.consumer_probe = consumer_probe or (lambda token: issuer.accept(token))
        self.log: list[dict] = []
        self.state = SecretState(
            live_alias=secret_id,
            v1_name=f"{secret_id}.v1",
            v2_name=f"{secret_id}.v2",
            previous_name=f"{secret_id}.previous",
            v1_value=None,
            v2_value=None,
            live_points_to="v1",
            retired=[],
        )

    def _note(self, phase: str, ok: bool, **extra) -> None:
        rec = {"ts": time.time(), "phase": phase, "ok": ok, **extra}
        self.log.append(rec)
        flag = "OK" if ok else "FAIL"
        print(f"[{flag}] {phase}: {json.dumps({k: v for k, v in extra.items() if k != 'value'})}")

    def inventory(self) -> None:
        ember = self.vault.resolve("ember", self.secret_id)
        proton = self.vault.resolve("proton", self.secret_id)
        if not ember:
            raise RotationError("no live secret in ember-keyring — refuse to rotate thin air")
        self.state.v1_value = ember
        self.issuer.valid.add(ember)
        drift = self.vault.drift(self.secret_id)
        self._note(
            "inventory",
            True,
            ember_fp=fp(ember),
            proton_fp=fp(proton) if proton else None,
            stores_in_sync=drift["in_sync"],
            warning=None if drift["in_sync"] else "Proton Pass drifted — will reconcile at end, will not overwrite live v1",
        )

    def mint(self) -> None:
        # Old key is not touched.
        new = self.issuer.mint()
        self.state.v2_value = new
        self._note("mint", True, new_fp=fp(new), old_still_valid=self.issuer.accept(self.state.v1_value or ""))

    def dual_write(self) -> None:
        if not self.state.v2_value:
            raise RotationError("mint first")
        # Sibling keys only. Live alias still points at v1.
        for store in ("ember", "proton"):
            self.vault.write(store, self.state.v2_name, self.state.v2_value)
            if self.state.v1_value:
                self.vault.write(store, self.state.v1_name, self.state.v1_value)
        self._note(
            "dual_write",
            True,
            wrote=["ember/" + self.state.v2_name, "proton/" + self.state.v2_name],
            live_alias_untouched=True,
            old_still_valid=self.issuer.accept(self.state.v1_value or ""),
        )

    def verify_new(self) -> None:
        token = self.state.v2_value
        if not token or not self.issuer.accept(token):
            self._note("verify_new", False, reason="issuer rejected v2")
            raise RotationError("v2 failed issuer probe — abort, old key still live")
        self._note("verify_new", True, issuer_accepts_v2=True, issuer_accepts_v1=self.issuer.accept(self.state.v1_value or ""))

    def cutover(self) -> None:
        # Alias flip only.
        for store in ("ember", "proton"):
            if self.state.v1_value:
                self.vault.write(store, self.state.previous_name, self.state.v1_value)
            self.vault.alias(store, self.secret_id, self.state.v2_name)
        self.state.live_points_to = "v2"
        self._note(
            "cutover",
            True,
            live_alias=self.secret_id,
            now_points_to=self.state.v2_name,
            previous_kept=self.state.previous_name,
        )

    def verify_consumers(self) -> None:
        live = self.vault.resolve("ember", self.secret_id)
        if not live or not self.consumer_probe(live):
            # automatic rollback
            for store in ("ember", "proton"):
                self.vault.alias(store, self.secret_id, self.state.v1_name)
            self.state.live_points_to = "v1"
            self._note("verify_consumers", False, rolled_back_to="v1")
            raise RotationError("consumer probe failed — rolled live alias back to v1")
        self._note("verify_consumers", True, consumer_saw_fp=fp(live))

    def retire_old(self) -> None:
        if self.state.live_points_to != "v2":
            raise RotationError("refuse to retire v1 while live alias is not on v2")
        if self.state.v1_value:
            self.issuer.disable(self.state.v1_value)
        self.state.retired.append("v1")
        self._note(
            "retire_old",
            True,
            issuer_disabled_v1=True,
            v1_still_in_vault_as=self.state.previous_name,
            v1_no_longer_authenticates=not self.issuer.accept(self.state.v1_value or ""),
        )

    def reconcile_stores(self) -> None:
        live_e = self.vault.resolve("ember", self.secret_id)
        live_p = self.vault.resolve("proton", self.secret_id)
        if live_e != live_p:
            # Proton follows ember, never the other way around after a proven cutover.
            if live_e:
                self.vault.alias("proton", self.secret_id, self.state.v2_name)
                self.vault.write("proton", self.state.v2_name, live_e)
            live_p = self.vault.resolve("proton", self.secret_id)
        ok = live_e == live_p and live_e == self.state.v2_value
        self._note(
            "reconcile_stores",
            ok,
            ember_fp=fp(live_e) if live_e else None,
            proton_fp=fp(live_p) if live_p else None,
            in_sync=ok,
        )
        if not ok:
            raise RotationError("stores still drifted after reconcile")

    def run(self) -> int:
        for phase in PHASES:
            getattr(self, phase)()
        print("\nROTATION COMPLETE")
        print(json.dumps({
            "secret_id": self.secret_id,
            "live_points_to": self.state.live_points_to,
            "v1_fp": fp(self.state.v1_value) if self.state.v1_value else None,
            "v2_fp": fp(self.state.v2_value) if self.state.v2_value else None,
            "retired": self.state.retired,
            "stores": self.vault.drift(self.secret_id),
        }, indent=2))
        return 0


def seed_demo(vault: TwoStoreVault, secret_id: str) -> str:
    """Reproduce today's drift: ember has the real token, Proton has a stale password."""
    live = "tok_" + secrets.token_hex(16)
    stale = "stale_password_" + secrets.token_hex(4)
    vault.write("ember", secret_id, live)
    vault.write("proton", secret_id, stale)
    return live


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Dual-key rotation — old key stays until new is proven")
    p.add_argument("--demo", action="store_true", help="run a two-store drifted rotation end to end")
    p.add_argument("--secret-id", default="technitium")
    p.add_argument("--stores-dir", default="")
    p.add_argument("--fail-verify", action="store_true", help="demo a failed consumer probe + automatic rollback")
    args = p.parse_args(argv)

    root = Path(args.stores_dir) if args.stores_dir else Path("/tmp/key-rotation-demo")
    if args.demo:
        if root.exists():
            # keep the dir but reset children
            pass
        vault = TwoStoreVault(root)
        live = seed_demo(vault, args.secret_id)
        issuer = Issuer()
        issuer.valid.add(live)
        print("SEEDED DRIFT (today's Technitium miss)")
        print(json.dumps(vault.drift(args.secret_id), indent=2))
        print(f"old key stays valid until retire: fp={fp(live)}\n")

        def probe(token: str) -> bool:
            if args.fail_verify:
                return False
            return issuer.accept(token)

        rot = Rotator(args.secret_id, vault, issuer, consumer_probe=probe)
        try:
            return rot.run()
        except RotationError as e:
            print(f"\nABORTED: {e}")
            print("old key still serving:" , issuer.accept(live))
            return 2
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
