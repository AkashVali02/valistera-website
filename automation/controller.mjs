import { validateTask } from "./policy.mjs";

/**
 * Durable controller core. Storage and tool adapters are injected.
 * Store MUST implement atomic insertIfAbsent and claim operations, and
 * durable save/get; production must use transactional storage (e.g. D1).
 * No network calls or secrets are contained in this module.
 */
export class OperationsController {
  constructor({ store, handlers = {}, now = () => new Date().toISOString() }) {
    if (!store || typeof store.insertIfAbsent !== "function" || typeof store.claim !== "function" ||
        typeof store.get !== "function" || typeof store.save !== "function") {
      throw new TypeError("Transactional task store required");
    }
    this.store = store;
    this.handlers = handlers;
    this.now = now;
  }

  async submit(task) {
    const decision = validateTask(task);
    if (!decision.ok && decision.error !== "approval_required") {
      return { accepted: false, error: decision.error };
    }
    // Never trust approval objects from an unauthenticated public request.
    // The submission layer MUST validate approval provenance separately.
    const record = {
      id: task.id, agent: task.agent, action: task.action,
      payload: task.payload ?? {},
      state: decision.ok ? "queued" : "awaiting_approval",
      createdAt: this.now(), updatedAt: this.now(),
      attempts: 0, result: null, error: null,
      approval: task.approval ?? null
    };
    const inserted = await this.store.insertIfAbsent(record);
    if (!inserted) return { accepted: true, duplicate: true, task: await this.store.get(task.id) };
    return { accepted: true, duplicate: false, task: record };
  }

  async run(id) {
    // claim MUST atomically transition queued -> running; only one worker wins.
    const task = await this.store.claim(id, this.now());
    if (!task) return { executed: false, reason: "not_claimable" };
    const handler = this.handlers[task.agent + "." + task.action];
    if (typeof handler !== "function") {
      await this.store.save({ ...task, state: "failed", error: "handler_unavailable", updatedAt: this.now() });
      return { executed: false, reason: "handler_unavailable" };
    }
    try {
      const result = await handler(task.payload, { taskId: task.id });
      // External handlers must implement their own idempotency by taskId.
      const completed = { ...task, state: "completed", result: result ?? null, error: null, updatedAt: this.now() };
      await this.store.save(completed);
      return { executed: true, task: completed };
    } catch {
      const failed = { ...task, state: "failed", error: "handler_failed", updatedAt: this.now() };
      await this.store.save(failed);
      return { executed: false, reason: "handler_failed" };
    }
  }
}

/** Local tests only; not safe for distributed production workers. */
export class MemoryTaskStore {
  constructor() { this.records = new Map(); }
  async insertIfAbsent(record) {
    if (this.records.has(record.id)) return false;
    this.records.set(record.id, structuredClone(record));
    return true;
  }
  async get(id) { return structuredClone(this.records.get(id) ?? null); }
  async claim(id, at) {
    const current = this.records.get(id);
    if (!current || current.state !== "queued") return null;
    const next = { ...current, state: "running", attempts: current.attempts + 1, updatedAt: at };
    this.records.set(id, next);
    return structuredClone(next);
  }
  async save(record) { this.records.set(record.id, structuredClone(record)); }
}
