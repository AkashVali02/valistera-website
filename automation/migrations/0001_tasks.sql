-- ValiStera AI Operations Platform — D1 task store (draft)
-- Apply only to a dedicated staging database after review.
CREATE TABLE IF NOT EXISTS ai_tasks (
  id TEXT PRIMARY KEY,
  agent TEXT NOT NULL,
  action TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  state TEXT NOT NULL CHECK (state IN ('awaiting_approval','queued','running','completed','failed')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  result_json TEXT,
  error TEXT,
  approval_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_ai_tasks_state_created ON ai_tasks(state, created_at);
