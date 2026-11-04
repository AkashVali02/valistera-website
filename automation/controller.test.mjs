import assert from "node:assert/strict";
import { test } from "node:test";
import { OperationsController, MemoryTaskStore } from "./controller.mjs";

const base = { id:"lead_0001", agent:"sales", action:"qualify_lead", payload:{ source:"website" } };
test("submits and executes a task once", async () => {
  const store = new MemoryTaskStore();
  let calls = 0;
  const c = new OperationsController({store,handlers:{"sales.qualify_lead":async () => {calls++;return { qualified:false };}}});
  assert.equal((await c.submit(base)).duplicate,false);
  assert.equal((await c.submit(base)).duplicate,true);
  assert.equal((await c.run(base.id)).executed,true);
  assert.equal((await c.run(base.id)).executed,false);
  assert.equal(calls,1);
  assert.equal((await store.get(base.id)).state,"completed");
});
test("unverified approval never enables publishing",async()=>{
  const store=new MemoryTaskStore();
  const c=new OperationsController({store});
  const task={id:"post_0001",agent:"marketing",action:"publish_post",approval:{status:"approved",approvedBy:"owner",approvedAt:"2026-11-04T00:00:00Z",taskId:"post_0001",action:"publish_post"}};
  assert.equal((await c.submit(task)).task.state,"awaiting_approval");
  assert.equal((await c.run(task.id)).reason,"not_claimable");
});
test("verified approval permits queuing but not execution without adapter",async()=>{
  const store=new MemoryTaskStore();
  const c=new OperationsController({store,verifyApproval:async()=>true});
  const task={id:"post_0002",agent:"marketing",action:"publish_post",approval:{status:"approved",approvedBy:"owner",approvedAt:"2026-11-04T00:00:00Z",taskId:"post_0002",action:"publish_post"}};
  assert.equal((await c.submit(task)).task.state,"queued");
  assert.equal((await c.run(task.id)).reason,"handler_unavailable");
});
test("handler failure records a redacted failure",async()=>{
  const store=new MemoryTaskStore();
  const c=new OperationsController({store,handlers:{"sales.qualify_lead":async()=>{throw Error("sensitive data");}}});
  await c.submit(base);
  assert.equal((await c.run(base.id)).reason,"handler_failed");
  assert.equal((await store.get(base.id)).error,"handler_failed");
});
test("never permits human GMP record approval",async()=>{
  const c=new OperationsController({store:new MemoryTaskStore(),verifyApproval:async()=>true});
  const task={id:"gmp_0001",agent:"quality",action:"approve_gmp_record",approval:{status:"approved",approvedBy:"owner",approvedAt:"2026-11-04T00:00:00Z",taskId:"gmp_0001",action:"approve_gmp_record"}};
  assert.equal((await c.submit(task)).error,"human_only");
});
