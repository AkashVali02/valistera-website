/**
 * Cloudflare D1 adapter for OperationsController.
 * Requires D1 binding and migration 0001_tasks.sql.
 * No DB is provisioned by this file.
 */
const columns = "id, agent, action, payload_json, state, created_at, updated_at, attempts, result_json, error, approval_json";
function decode(row) {
  if (!row) return null;
  return {
    id: row.id, agent: row.agent, action: row.action,
    payload: JSON.parse(row.payload_json), state: row.state,
    createdAt: row.created_at, updatedAt: row.updated_at,
    attempts: row.attempts,
    result: row.result_json === null ? null : JSON.parse(row.result_json),
    error: row.error,
    approval: row.approval_json === null ? null : JSON.parse(row.approval_json)
  };
}
export class D1TaskStore {
  constructor(db) {
    if (!db || typeof db.prepare !== "function") throw new TypeError("D1 binding required");
    this.db = db;
  }
  async insertIfAbsent(task) {
    const result = await this.db.prepare(
      "INSERT OR IGNORE INTO ai_tasks (" + columns + ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    ).bind(
      task.id, task.agent, task.action, JSON.stringify(task.payload),
      task.state, task.createdAt, task.updatedAt, task.attempts,
      task.result === null ? null : JSON.stringify(task.result),
      task.error, task.approval === null ? null : JSON.stringify(task.approval)
    ).run();
    return result.meta?.changes === 1;
  }
  async get(id) {
    const row = await this.db.prepare("SELECT " + columns + " FROM ai_tasks WHERE id = ?").bind(id).first();
    return decode(row);
  }
  async claim(id, at) {
    // Conditional UPDATE is atomic in SQLite: only one worker can win.
    const result = await this.db.prepare(
      "UPDATE ai_tasks SET state = 'running', attempts = attempts + 1, updated_at = ? WHERE id = ? AND state = 'queued'"
    ).bind(at, id).run();
    if (result.meta?.changes !== 1) return null;
    return this.get(id);
  }
  async save(task) {
    if (task.state !== "completed" && task.state !== "failed") {
      throw new Error("unsupported_state_transition");
    }
    // Guard against overwriting a task already finalized by another worker.
    const result = await this.db.prepare(
      "UPDATE ai_tasks SET state = ?, result_json = ?, error = ?, updated_at = ? WHERE id = ? AND state = 'running'"
    ).bind(
      task.state, task.result === null ? null : JSON.stringify(task.result),
      task.error, task.updatedAt, task.id
    ).run();
    if (result.meta?.changes !== 1) throw new Error("state_conflict");
  }
}
