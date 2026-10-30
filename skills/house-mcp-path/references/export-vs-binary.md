# Export vs binary

ember-mcp can contain herdr_pane_read / send_text / send_keys / pane_run
while this Grok session only lists herdr__pane_list and herdr__agent_*.

That is not a failed build. That is mcpproxy not exporting Ember pane tools
on $HOUSE_MCP_URL to this client.

Check in order
1. strings or tool list on /usr/local/bin/ember-mcp (date stamp)
2. search_connected_tools in THIS chat
3. If 1 has it and 2 does not, fix allowlist / adapter, do not rebuild again
