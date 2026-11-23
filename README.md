# FastMCP-Dev

A hands-on project for learning [FastMCP](https://gofastmcp.com/) by building a
local, read-only hardware reporting server and connecting it to LLM clients.

## What is in this repo?

- [`server.py`](./server.py) exposes `add_numbers` and `get_hardware_report` as
  MCP tools.
- [`.mcp.json`](./.mcp.json) configures the tools for VS Code's Copilot agent.
- [`.github/agents/hardware-report.agent.md`](./.github/agents/hardware-report.agent.md)
  defines a reusable Copilot custom agent that calls the hardware tool and
  explains its results.

The hardware tool reads CPU, memory, uptime, and disk usage. It does not change
your system. CPU usage is sampled over half a second and can vary between calls.

## 1. Set up and try the server

This project uses [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run fastmcp dev inspector server.py
```

In the Inspector, select `get_hardware_report` and run it. Its optional
`disk_path` argument defaults to the current working directory. Try
`add_numbers` with `first = 2` and `second = 3` as a simpler example.

## 2. Connect the server to VS Code Copilot

The repo includes a workspace-root [`.mcp.json`](./.mcp.json) configuration. In
VS Code:

1. Open this repository as your workspace and select **Copilot** as the session
   target in Chat.
2. If workspace MCP configuration is not enabled, enable
   `chat.mcp.workspaceRootConfig.enabled` in Settings.
3. Use **MCP: List Servers** from the Command Palette, start
   `fastmcpLearning`, and approve the server if prompted.
4. In the Agent picker, select **Hardware Reporter**. Ask it to report current
   CPU, memory, and disk usage.

Expand the tool call in the chat to confirm that Copilot actually called
`get_hardware_report`. The MCP server runs locally, but the report is still sent
to the LLM client you're using.

If VS Code does not load the workspace config, use **MCP: Add Server** from the
Command Palette and configure a local stdio server with command `uv` and
arguments `run`, `fastmcp`, `run`, `server.py`. See the [VS Code MCP server
guide](https://code.visualstudio.com/docs/agent-customization/mcp-servers) for
other configuration scopes and troubleshooting.

## How the Copilot agent works

The custom agent profile in `.github/agents/hardware-report.agent.md` gives
Copilot a focused role and access to `fastmcpLearning/get_hardware_report`.
Copilot calls the local MCP server, receives its structured result, and
summarizes it for you. No separate OpenAI SDK script or API key is needed:
Copilot uses the model configured in your VS Code session.

The MCP server runs locally, but its report is provided to the selected LLM.
Avoid requesting a report if those machine details should not be shared with
that model provider.

## Learning path

1. Tools, type hints, and tool schemas.
2. Custom agents: give an LLM a focused role and access to selected MCP tools
   (current).
3. Resources: expose a system summary for clients to read.
4. Prompts: create reusable report instructions.
5. Clients and transports: compare stdio with HTTP.
6. Production basics: configuration, errors, and authentication.
