import assert from "node:assert/strict";
import { test } from "node:test";
import { validateTask } from "./policy.mjs";

const base = { id:"task_1001", agent:"marketing", action:"draft_post", payload:{topic:"Annex 1"} };
test("allows non-publishing draft",()=>assert.equal(validateTask(base).ok,true));
test("rejects unknown action",()=>assert.equal(validateTask({...base,action:"send_email"}).error,"unsupported_action"));
test("requires approval for publishing",()=>assert.equal(validateTask({...base,action:"publish_post"}).error,"approval_required"));
test("rejects approval for a different task",()=>assert.equal(validateTask({...base,action:"publish_post",approval:{status:"approved",approvedBy:"owner",approvedAt:"2026-11-04T00:00:00Z",taskId:"task_other",action:"publish_post"}}).error,"approval_required"));
test("accepts correctly scoped approval",()=>assert.equal(validateTask({...base,action:"publish_post",approval:{status:"approved",approvedBy:"owner",approvedAt:"2026-11-04T00:00:00Z",taskId:"task_1001",action:"publish_post"}}).ok,true));
test("never automates GMP approval",()=>assert.equal(validateTask({id:"task_1002",agent:"quality",action:"approve_gmp_record",approval:{status:"approved",approvedBy:"owner",approvedAt:"2026-11-04T00:00:00Z",taskId:"task_1002",action:"approve_gmp_record"}}).error,"human_only"));
test("rejects invalid identifiers",()=>assert.equal(validateTask({...base,id:"!"}).error,"invalid_id"));
