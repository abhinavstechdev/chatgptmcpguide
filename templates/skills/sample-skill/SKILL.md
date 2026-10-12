---
name: task-triage
description: >-
  Triage new task items, assign priority levels, and generate structured
  sprint updates using Acme Task Manager MCP tools.
---

# Task Triage Workflow

Use this skill when the user asks to review new backlog items, reorganize tasks, or prepare sprint summaries.

## Procedure

1. **Query Unassigned Tasks:**
   Call the `fetch_tasks` tool with argument `filter: "active"` to retrieve all pending tasks.

2. **Analyze and Prioritize:**
   Review each task against current sprint milestones:
   - Mark blockers or security defects as `HIGH`.
   - Mark standard feature work as `NORMAL`.

3. **Render the Board:**
   Call the `render_task_board` tool, providing the structured list of tasks to render the interactive UI board for the user.

4. **Summarize for User:**
   Provide a brief 2-3 sentence markdown summary highlighting high-priority items and any recommended assignments.
