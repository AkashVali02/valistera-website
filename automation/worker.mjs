import { OperationsController } from "./controller.mjs";
import { D1TaskStore } from "./d1-store.mjs";

/**
 * Private staging Worker skeleton. No handlers are registered, so this Worker
 * CANNOT publish, send messages, or perform CRM writes.
 * Bind AI_TASKS (D1) and OPS_API_TOKEN (secret) before use.
 */
const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" }
});
async function equalSecret(received, expected) {
  if (!received || !expected) return false;
  const encoder = new TextEncoder();
  const [a,b] = await Promise.all([received,expected].map(x=>crypto.subtle.digest("SHA-256",encoder.encode(x))));
  const x=new Uint8Array(a),y=new Uint8Array(b);
  let difference=0;
  for(let i=0;i<x.length;i++) difference|=x[i]^y[i];
  return difference===0;
}
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/health" && request.method === "GET") {
      return json({ service:"valistera-ai-operations", status:"staging", deployed:true });
    }
    if (!env.AI_TASKS || !env.OPS_API_TOKEN) return json({error:"not_configured"},503);
    const authorization = request.headers.get("authorization") || "";
    if (!authorization.startsWith("Bearer ") ||
        !await equalSecret(authorization.slice(7), env.OPS_API_TOKEN)) {
      return json({error:"unauthorized"},401);
    }
    const store = new D1TaskStore(env.AI_TASKS);
    const controller = new OperationsController({store});
    if (url.pathname === "/tasks" && request.method === "POST") {
      if (!request.headers.get("content-type")?.toLowerCase().startsWith("application/json")) return json({error:"invalid_content_type"},415);
      const length=Number(request.headers.get("content-length") || 0);
      if(length>16384) return json({error:"payload_too_large"},413);
      let task;
      try {
        const raw=await request.text();
        if(raw.length>16384) return json({error:"payload_too_large"},413);
        task=JSON.parse(raw);
      } catch { return json({error:"invalid_json"},400); }
      // Never accept public approval evidence; approvals require a separate
      // signed, authenticated approval workflow not yet implemented.
      if(task && typeof task==="object") task.approval=undefined;
      const result=await controller.submit(task);
      return json(result.accepted ? {accepted:true,id:result.task.id,state:result.task.state,duplicate:result.duplicate} : {error:result.error},result.accepted?202:400);
    }
    if (url.pathname.startsWith("/tasks/") && request.method === "GET") {
      const id=url.pathname.slice("/tasks/".length);
      if(!/^[a-zA-Z0-9_-]{4,80}$/.test(id)) return json({error:"invalid_id"},400);
      const task=await store.get(id);
      if(!task) return json({error:"not_found"},404);
      // Never expose payloads, results, or approval objects in status API.
      return json({id:task.id,agent:task.agent,action:task.action,state:task.state,createdAt:task.createdAt,updatedAt:task.updatedAt,attempts:task.attempts,error:task.error});
    }
    return json({error:"not_found"},404);
  }
};
