// Deterministic authoring semantics, not native Keynote compatibility evidence.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const c=vm.createContext({ObjC:{import(){}},Path:x=>x});
vm.runInContext(fs.readFileSync(require('node:path').join(__dirname,'../scripts/keynote_native.js'),'utf8'),c);
function collection(initial=[]) {const a=initial;const fn=()=>a;fn.push=o=>{a.push(o);fn[a.length-1]=o;};a.forEach((o,i)=>fn[i]=o);return fn;}
function object(v={}) {let text=v.objectText||'';const o={};for(const k of ['position','width','height']) {let value;Object.defineProperty(o,k,{get:()=>()=>value,set:v=>{value=v;}});}const rich=()=>text;Object.defineProperty(o,'objectText',{get:()=>rich,set:v=>{text=v;}});return o;}
const slide={textItems:collection(),shapes:collection(),tables:collection(),charts:collection(),images:collection()};
const doc={slides:collection([slide]),width:()=>1280,height:()=>720};
const app={TextItem:object,Shape:object,Image:object};
c.authorOperations(doc,app,[{action:'add_text',slide:1,text:'Original',bounds:[20,20,400,60],size:32,color:'182C32'},{action:'set_text',slide:1,kind:'text_item',index:1,text:'Changed'}],'edit');
assert.equal(slide.textItems[0].objectText(),'Changed');
assert.deepEqual(JSON.parse(JSON.stringify(slide.textItems[0].position())),{x:20,y:20});
assert.equal(slide.textItems[0].objectText.size,32);
assert.throws(()=>c.authorOperations(doc,app,[{action:'add_text',slide:1,text:'Overflow',bounds:[1200,20,400,60]}],'edit'));
assert.throws(()=>c.authorOperations(doc,app,[{action:'set_text',slide:1,kind:'text_item',index:99,text:'Missing'}],'edit'));
assert.throws(()=>c.authorOperations(doc,app,[{action:'delete_slide',slide:1}],'edit'));
c.authorOperations(doc,app,[{action:'set_slide',slide:1,notes:'Exact notes',skipped:true}],'edit');
assert.equal(slide.presenterNotes,'Exact notes');assert.equal(slide.skipped,true);
console.log('Authoring boundary and text/metadata checks passed (stubbed, not live).');
// A move must conserve all slide content and use the expected permutation.
c.inventory=d=>({slides:d.rows.map((name,i)=>({slide:i+1,name}))});
const moving={rows:['Evidence','Summary','Closing','Appendix'],slides:collection([{}, {}, {}, {}])};
c.moveAuthorSlide=(d,from,before)=>{const item=d.rows.splice(from-1,1)[0];d.rows.splice(before-1-(from<before?1:0),0,item);};
c.authorOperations(moving,app,[{action:'move_slide',slide:4,before:2}],'edit');
assert.deepEqual(moving.rows,['Evidence','Appendix','Summary','Closing']);
c.moveAuthorSlide=d=>{d.rows.splice(1,1);};
assert.throws(()=>c.authorOperations(moving,app,[{action:'move_slide',slide:4,before:2}],'edit'),/Move changed slide content or order/);
assert.equal(c.colorFromNative([0.0941023901104927,0.1725337654352188,0.19606317579746246]),'182C32');
assert.equal(c.colorFromNative([6168,11308,12850]),'182C32');
assert.equal(c.colorFromNative([1,1,1]),'FFFFFF');
assert.throws(()=>c.colorFromNative([NaN,0,0]));
assert.throws(()=>c.colorFromNative([-1,0,0]));
assert.throws(()=>c.colorFromNative([65536,0,0]));

assert.doesNotThrow(()=>c.validateTextFrame([64,50,1100,80],[64,50,1100,52],'fit'));
assert.throws(()=>c.validateTextFrame([64,50,1100,80],[64,50,1100,52],'fixed'));
assert.throws(()=>c.validateTextFrame([64,50,1100,80],[64,50,1100,81],'fit'));
assert.throws(()=>c.validateTextFrame([64,50,1100,80],[64,64,1100,52],'fit'));
