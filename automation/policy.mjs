/**
 * ValiStera AI Operations Platform — policy gate (Node 20+, no dependencies).
 * This module validates task requests before an external orchestration engine
 * schedules or executes them. It does NOT execute external actions.
 */
export const AGENTS = Object.freeze({
  sales: ["research_prospects", "qualify_lead", "draft_outreach", "create_crm_contact"],
  marketing: ["draft_post", "design_brief", "publish_post"],
  website: ["audit_site", "draft_code_change", "open_pull_request", "deploy_production"],
  backend: ["inspect_worker", "draft_integration", "deploy_worker"],
  academy: ["draft_lesson", "review_assessment", "publish_course"],
  quality: ["review_gmp_content", "draft_sop", "approve_gmp_record"]
});
export const RESTRICTED = new Set([
  "publish_post", "create_crm_contact", "deploy_production",
  "deploy_worker", "publish_course", "approve_gmp_record"
]);
export const NEVER_AUTOMATE = new Set(["approve_gmp_record"]);
export function validateTask(task) {
  if (!task || typeof task !== "object" || Array.isArray(task)) return { ok:false, error:"invalid_task" };
  const { id, agent, action, payload, approval } = task;
  if (typeof id !== "string" || !/^[a-zA-Z0-9_-]{4,80}$/.test(id)) return { ok:false, error:"invalid_id" };
  if (!Object.hasOwn(AGENTS, agent) || !AGENTS[agent].includes(action)) return { ok:false, error:"unsupported_action" };
  if (payload !== undefined && (typeof payload !== "object" || payload === null || Array.isArray(payload))) return { ok:false, error:"invalid_payload" };
  if (NEVER_AUTOMATE.has(action)) return { ok:false, error:"human_only" };
  if (RESTRICTED.has(action) && !(approval?.status === "approved" && typeof approval.approvedBy === "string" && approval.approvedBy.trim() && typeof approval.approvedAt === "string" && !Number.isNaN(Date.parse(approval.approvedAt)) && approval.taskId === id && approval.action === action)) {
    return { ok:false, error:"approval_required" };
  }
  return { ok:true, execution:"not_implemented", approvalRequired:RESTRICTED.has(action) };
}
