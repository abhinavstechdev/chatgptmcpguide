"""
Production FastMCP Server with MCP Apps UI for ChatGPT and Codex.
Demonstrates decoupled data and render tools, tool invocation hints,
and RFC 9728 OAuth resource discovery.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional

TEMPLATE_URI = "ui://widget/tasks.html"

mcp = FastMCP("Acme Tasks Server")

WIDGET_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Task Board</title>
  <style>
    :root {
      font-family: system-ui, -apple-system, sans-serif;
      color: #111827;
      background: #f9fafb;
    }
    body { margin: 0; padding: 12px; }
    .box { background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; }
    .title { font-size: 15px; font-weight: 600; margin-bottom: 8px; }
    .item { padding: 6px 8px; background: #f3f4f6; margin-bottom: 6px; border-radius: 4px; display: flex; justify-content: space-between; }
  </style>
</head>
<body>
  <div class="box">
    <div class="title">Tasks</div>
    <div id="content">Waiting for task data...</div>
  </div>
  <script type="module">
    window.addEventListener("message", (event) => {
      if (event.source !== window.parent) return;
      const msg = event.data;
      if (msg?.method === "ui/notifications/tool-result") {
        const tasks = msg.params?.structuredContent?.tasks || [];
        const el = document.getElementById("content");
        if (!tasks.length) {
          el.innerHTML = "No tasks";
        } else {
          el.innerHTML = tasks.map(t => `<div class="item"><span>${t.title}</span><b>${t.status}</b></div>`).join("");
        }
      }
    }, { passive: true });
    window.parent.postMessage({ jsonrpc: "2.0", method: "ui/notifications/initialized" }, "*");
  </script>
</body>
</html>
""".strip()

# Register UI resource
@mcp.resource(TEMPLATE_URI, mime_type="text/html;profile=mcp-app")
def get_task_widget() -> str:
    return WIDGET_HTML

class TaskItem(BaseModel):
    id: str
    title: str
    status: str
    priority: str

class TaskListOutput(BaseModel):
    tasks: List[TaskItem]

MOCK_TASKS = [
    TaskItem(id="T-1", title="Setup FastMCP Endpoint", status="DONE", priority="HIGH"),
    TaskItem(id="T-2", title="Configure OAuth discovery", status="IN_PROGRESS", priority="HIGH"),
    TaskItem(id="T-3", title="Test in ChatGPT Work", status="TODO", priority="NORMAL")
]

# 1. Data Tool: no UI resource, returns structured data for model intelligence
@mcp.tool(
    name="get_tasks",
    description="Fetch list of sprint tasks. Returns structured task objects."
)
def get_tasks(filter: str = "all") -> TaskListOutput:
    """Retrieve tasks with filtering."""
    return TaskListOutput(tasks=MOCK_TASKS)

# 2. Render Tool: owns UI template and receives structured data
@mcp.tool(
    name="render_tasks",
    description="Render interactive task UI in ChatGPT. Pass tasks obtained from get_tasks."
)
def render_tasks(tasks: List[TaskItem]) -> TaskListOutput:
    """Renders the task widget with final data."""
    return TaskListOutput(tasks=tasks)

if __name__ == "__main__":
    # Run with SSE transport on port 8000
    mcp.run(transport="sse")
