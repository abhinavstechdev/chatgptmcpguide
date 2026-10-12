import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express, { Request, Response } from "express";
import { z } from "zod";

const TEMPLATE_URI = "ui://widget/tasks.html";

// HTML widget code implementing MCP Apps postMessage bridge
const widgetHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Task Board</title>
  <style>
    :root {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #0d0d0d;
      background: #ffffff;
    }
    body { margin: 0; padding: 16px; box-sizing: border-box; }
    .card { border: 1px solid #e5e5e5; border-radius: 12px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
    .title { font-weight: 600; font-size: 16px; }
    ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
    li { display: flex; align-items: center; justify-content: space-between; padding: 8px 12px; background: #f9f9f9; border-radius: 8px; }
    .badge { font-size: 11px; padding: 2px 6px; border-radius: 4px; font-weight: 500; }
    .badge-high { background: #fee2e2; color: #dc2626; }
    .badge-normal { background: #e0f2fe; color: #0284c7; }
    button { cursor: pointer; border: none; background: #10a37f; color: white; border-radius: 6px; padding: 6px 12px; font-weight: 500; }
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="title" id="board-title">Sprint Tasks</div>
      <button id="refresh-btn">Refresh</button>
    </div>
    <ul id="task-list">Loading tasks...</ul>
  </div>

  <script type="module">
    const listEl = document.getElementById("board-title");
    const taskList = document.getElementById("task-list");
    const refreshBtn = document.getElementById("refresh-btn");

    let rpcId = 1;
    const pending = new Map();

    function sendRequest(method, params) {
      const id = rpcId++;
      window.parent.postMessage({ jsonrpc: "2.0", id, method, params }, "*");
      return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
    }

    function renderTasks(tasks) {
      if (!tasks || !tasks.length) {
        taskList.innerHTML = "<li>No tasks found</li>";
        return;
      }
      taskList.innerHTML = tasks.map(t => \`
        <li>
          <span>\${t.title}</span>
          <span class="badge \${t.priority === 'HIGH' ? 'badge-high' : 'badge-normal'}">\${t.priority}</span>
        </li>
      \`).join("");
    }

    // Handle MCP Apps host messages
    window.addEventListener("message", (event) => {
      if (event.source !== window.parent) return;
      const data = event.data;
      if (!data || data.jsonrpc !== "2.0") return;

      if (typeof data.id === "number" && pending.has(data.id)) {
        const { resolve, reject } = pending.get(data.id);
        pending.delete(data.id);
        if (data.error) reject(data.error);
        else resolve(data.result);
        return;
      }

      if (data.method === "ui/notifications/tool-result") {
        const structured = data.params?.structuredContent;
        if (structured?.tasks) renderTasks(structured.tasks);
      }
    }, { passive: true });

    // Refresh calls the data tool via host bridge
    refreshBtn.addEventListener("click", async () => {
      refreshBtn.disabled = true;
      try {
        const res = await sendRequest("tools/call", {
          name: "fetch_tasks",
          arguments: { filter: "all" }
        });
        if (res?.structuredContent?.tasks) renderTasks(res.structuredContent.tasks);
      } catch (err) {
        console.error("Refresh failed:", err);
      } finally {
        refreshBtn.disabled = false;
      }
    });

    // Notify host that UI is initialized
    window.parent.postMessage({ jsonrpc: "2.0", method: "ui/notifications/initialized" }, "*");
  </script>
</body>
</html>`.trim();

// Create MCP Server instance
const server = new McpServer(
  {
    name: "Acme Tasks Server",
    version: "1.0.0"
  },
  {
    capabilities: {
      tools: {},
      resources: {}
    }
  }
);

// Register MCP Apps UI Resource
server.registerResource(
  "tasks-widget",
  TEMPLATE_URI,
  {},
  async () => ({
    contents: [
      {
        uri: TEMPLATE_URI,
        mimeType: "text/html;profile=mcp-app",
        text: widgetHtml,
        _meta: {
          ui: { prefersBorder: true }
        }
      }
    ]
  })
);

// In-memory mock storage
const mockTasks = [
  { id: "T-101", title: "Implement OAuth PKCE flow", priority: "HIGH", status: "IN_PROGRESS" },
  { id: "T-102", title: "Optimize metadata schema", priority: "NORMAL", status: "TODO" },
  { id: "T-103", title: "Add MCP Apps postMessage tests", priority: "HIGH", status: "DONE" }
];

// 1. DATA TOOL: decoupled data query tool (No UI output template)
server.registerTool(
  "fetch_tasks",
  {
    title: "Fetch Tasks",
    description: "Fetch tasks filtered by status or priority. Returns raw structured task items.",
    inputSchema: {
      filter: z.enum(["all", "active", "completed"]).default("all")
    },
    outputSchema: {
      tasks: z.array(z.object({
        id: z.string(),
        title: z.string(),
        priority: z.string(),
        status: z.string()
      }))
    },
    _meta: {
      "openai/toolInvocation/invoking": "Retrieving sprint tasks…",
      "openai/toolInvocation/invoked": "Sprint tasks retrieved.",
      readOnlyHint: true,
      openWorldHint: false,
      destructiveHint: false
    }
  },
  async ({ filter }) => {
    return {
      structuredContent: { tasks: mockTasks },
      content: [
        {
          type: "text",
          text: `Found ${mockTasks.length} tasks matching filter: ${filter}`
        }
      ]
    };
  }
);

// 2. RENDER TOOL: decoupled presentation tool (Owns UI template)
server.registerTool(
  "render_task_board",
  {
    title: "Render Task Board",
    description: "Render interactive UI task board in ChatGPT. Must pass structured task items from fetch_tasks.",
    inputSchema: {
      tasks: z.array(z.object({
        id: z.string(),
        title: z.string(),
        priority: z.string(),
        status: z.string()
      }))
    },
    outputSchema: {
      tasks: z.array(z.any())
    },
    _meta: {
      ui: { resourceUri: TEMPLATE_URI },
      "openai/toolInvocation/invoking": "Rendering task board…",
      "openai/toolInvocation/invoked": "Task board rendered.",
      readOnlyHint: true,
      openWorldHint: false,
      destructiveHint: false
    }
  },
  async ({ tasks }) => {
    return {
      structuredContent: { tasks },
      content: [
        {
          type: "text",
          text: `Rendered task board displaying ${tasks.length} items.`
        }
      ]
    };
  }
);

// Express HTTP transport server
const app = express();
const port = process.env.PORT || 3000;

// OAuth Protected Resource discovery endpoint (RFC 9728)
app.get("/.well-known/oauth-protected-resource", (_req: Request, res: Response) => {
  res.json({
    resource: `https://api.example.com`,
    authorization_servers: ["https://auth.example.com"],
    scopes_supported: ["tasks:read", "tasks:write"]
  });
});

let transport: SSEServerTransport;

app.get("/mcp/sse", async (req: Request, res: Response) => {
  transport = new SSEServerTransport("/mcp/messages", res);
  await server.connect(transport);
});

app.post("/mcp/messages", async (req: Request, res: Response) => {
  if (transport) {
    await transport.handlePostMessage(req, res);
  } else {
    res.status(400).send("No active SSE session");
  }
});

app.listen(port, () => {
  console.log(`MCP server running at http://localhost:${port}`);
});
