// Exercise the exact predicate used by the learner explorer, including negative errors.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('assets/academy/module-2/course.js','utf8');
const body=source.match(/function exceedsAbsoluteLimit\(value, limit\)\{[^}]+\}/)[0];
const predicate=vm.runInNewContext('('+body+')');
const cases=[[.5,.5,false],[.6,.5,true],[-.6,.5,true],[-.5,.5,false],[.3,.30000000000000004,false],[.5,.499999,true],[.5,.500001,false]];
for(const [value,limit,expected] of cases)assert.equal(predicate(value,limit),expected,`${value} at ${limit}`);
console.log('PASS: '+cases.length+' absolute-error boundary cases');
