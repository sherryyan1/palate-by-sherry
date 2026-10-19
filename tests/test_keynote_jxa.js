// JXA boundary regressions with deterministic application stubs; not native validation.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const code = fs.readFileSync(require('node:path').join(__dirname, '../scripts/keynote_native.js'), 'utf8');
function check(request, options = {}) {
    let closed = 0, saved = 0;
    const appleError = () => { throw new Error('PRIVATE CONTENT (-1743)'); };
    const inventory = {width: 960, height: 540, slides: [{slide: 1, skipped: false, notes: '',
        counts: {iwork_items: 0, text_items: 0, shapes: 0, images: 0, tables: 0, charts: 0, lines: 0, movies: 0, audio_clips: 0},
        text_items: [], shapes: [], tables: []}]};
    const slide = {skipped: () => false, presenterNotes: () => ''};
    for (const k of ['iWorkItems','textItems','shapes','images','tables','charts','lines','movies','audioClips','groups']) slide[k] = () => [];
    slide.iworkItems = () => [];
    slide.iWorkItems = undefined;
    Object.defineProperty(slide.iworkItems, 'length', {value: options.itemCount || 0});
    const doc = {file: () => ({toString: () => '/scratch/inspection.key'}), width: () => 960, height: () => 540,
        slides: options.inventoryError ? appleError : () => [slide],
        save: () => { saved++; if(options.saveError) appleError(); },
        close: () => { closed++; if(options.closeError) appleError(); }};
    const app = {version: () => '13.1', documents: options.accessError ? appleError : () => [doc],
        count: collection => { assert.equal(collection, slide.iworkItems); return options.itemCount || 0; },
        open: () => doc, export: options.exportError ? appleError : () => {}};
    const $ = value => ({stringByDeletingLastPathComponent: '/scratch', lastPathComponent: String(value).split('/').pop()});
    $.NSString = {stringWithContentsOfFileEncodingError: () => JSON.stringify(request)};
    $.NSFileManager = {defaultManager: {fileExistsAtPath: () => true}};
    const context = vm.createContext({$, ObjC: {import() {}, unwrap: x => x}, Path: x => x,
        Application: name => { if(options.bundleError && name === 'com.apple.iWork.Keynote') appleError(); return app; }});
    vm.runInContext(code, context);
    if(request.command === 'apply') request.expected_inventory = inventory;
    const result = JSON.parse(context.run(['/scratch/request.json']));
    assert(!JSON.stringify(result).includes('PRIVATE'));
    return {result, closed, saved};
}
assert.equal(check({command:'probe'}).result.document_count, 1);
assert.equal(check({command:'probe'}, {bundleError:true}).result.status, 'ok');
assert.equal(check({command:'probe'}, {accessError:true}).result.error.stage, 'document-access');
const inspect = {command:'inspect', document:'/scratch/inspection.key', pdf:'/scratch/preview.pdf'};
assert.equal(check(inspect).result.status, 'ok');
assert.equal(check(inspect, {exportError:true}).result.error.stage, 'export');
assert.equal(check(inspect, {closeError:true}).result.error.stage, 'close');
assert.equal(check(inspect, {inventoryError:true, closeError:true}).result.error.stage, 'inventory-slides');
assert.equal(check({...inspect, command:'apply', operations:[]}, {saveError:true}).result.error.stage, 'save');
assert.equal(check(inspect, {itemCount:2}).result.inventory.slides[0].counts.iwork_items, 2);
assert.deepEqual(Array.from(vm.runInNewContext('(' + code.match(/function pointCoordinates\(value\) \{[\s\S]*?\n\}/)[0] + ')({x:94,y:203})')), [94,203]);
console.log('10 JXA boundary regression checks passed (stubbed, not live).');
