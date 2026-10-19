/* Fixed JXA adapter. Bounded multi-slide fixtures passed on macOS 27.0.1 / Keynote 13.1.
 * Never evaluate request text as code. Open and close only the private copy named
 * by the Python orchestrator; do not save, close, activate or quit other documents.
 */
ObjC.import("Foundation");

let nativeStage = "request";

function run(argv) {
    try {
        return executeRequest(argv);
    } catch (error) {
        // Never return application error text: it can contain document contents.
        const match = String(error).match(/\((-?\d+)\)\s*$/);
        const code = Number(error.errorNumber || (match ? match[1] : 0));
        return JSON.stringify({schema_version: 1, status: "error",
            error: {stage: nativeStage, code: Number.isFinite(code) ? code : 0}});
    }
}

function executeRequest(argv) {
    if (argv.length !== 1) throw new Error("One private request path is required");
    const raw = $.NSString.stringWithContentsOfFileEncodingError(argv[0], $.NSUTF8StringEncoding, null);
    if (!raw) throw new Error("Cannot read request");
    const request = JSON.parse(ObjC.unwrap(raw));
    const requestDirectory = ObjC.unwrap($(argv[0]).stringByDeletingLastPathComponent);
    if (request.command !== "probe") {
        const documentDirectory = ObjC.unwrap($(request.document).stringByDeletingLastPathComponent);
        const documentName = ObjC.unwrap($(request.document).lastPathComponent);
        if (documentDirectory !== requestDirectory || !["inspection.key", "candidate.key"].includes(documentName)) throw new Error("Only the owned scratch copy may be opened");
        if (request.pdf && ObjC.unwrap($(request.pdf).stringByDeletingLastPathComponent) !== requestDirectory) throw new Error("Export must remain in the owned scratch directory");
    }
    nativeStage = "application-resolution";
    // Bundle lookup may be unavailable in a restricted Launch Services session.
    // A fixed installed path is a fallback, never a shell command or request code.
    let keynote;
    try {
        keynote = Application("com.apple.iWork.Keynote");
        keynote.version();
    } catch (error) {
        const path = "/Applications/Keynote.app";
        if (!$.NSFileManager.defaultManager.fileExistsAtPath(path)) throw error;
        keynote = Application(path);
    }
    let owned = null;
    let operationComplete = false;
    try {
        nativeStage = "application-access";
        const version = String(keynote.version());
        if (request.command === "probe") {
            // Version alone can be read from bundle metadata with no Apple-event access.
            // Resolve a live scripting collection to establish actual automation access.
            nativeStage = "document-access";
            const documentCount = keynote.documents().length;
            return JSON.stringify({schema_version: 1, status: "ok", keynote_version: version,
                document_count: documentCount});
        }
        if (!["inspect", "apply", "author"].includes(request.command)) throw new Error("Unknown native operation");
        // JXA Apple event modifiers are a final argument, not an application method.
        // This path is a freshly created private copy, never the user's source.
        nativeStage = "open";
        let opened;
        if (request.command === "author" && request.mode === "create") {
            nativeStage = "create-document";
            opened = keynote.Document().make();
            owned = opened; // This handle was created by this request, not selected globally.
            opened.save({in: Path(request.document)}, {timeout: 120});
        } else opened = keynote.open(Path(request.document), {timeout: 120});
        if (Array.isArray(opened)) opened = opened[0];
        if (!opened) throw new Error("Keynote did not open the copy");
        // Do not assume the app returned the requested document. Claim ownership
        // only after its actual file path matches the newly created scratch copy.
        // A mismatch is deliberately not closed, because it may be unrelated.
        nativeStage = "document-identity";
        if (opened.file().toString() !== request.document) throw new Error("Keynote returned a different document");
        owned = opened;
        if (request.command === "author") {
            nativeStage = "author";
            authorOperations(owned, keynote, request.operations, request.mode);
            nativeStage = "save-author";
            owned.save({}, {timeout: 120});
        }
        nativeStage = "inventory";
        const before = inventory(owned, keynote);
        if (request.command === "apply") {
            if (JSON.stringify(before) !== JSON.stringify(request.expected_inventory)) throw new Error("Source inventory changed");
            nativeStage = "modify";
            request.operations.forEach(function (operation) {
                const slide = owned.slides[operation.slide - 1];
                const object = operation.object_kind === "text_item" ? slide.textItems[operation.object_index - 1] : slide.shapes[operation.object_index - 1];
                if (operation.action === "geometry") {
                    object.position = {x: operation.bounds_points[0], y: operation.bounds_points[1]};
                    // Shape geometry is position-only; do not reassign dimensions.
                    if (operation.object_kind === "text_item") {
                        object.width = operation.bounds_points[2];
                        object.height = operation.bounds_points[3];
                    }
                } else if (operation.action === "text_style") {
                    const style = operation.style;
                    if (Object.prototype.hasOwnProperty.call(style, "font_size_pt")) object.objectText.size = style.font_size_pt;
                    if (Object.prototype.hasOwnProperty.call(style, "font_family")) object.objectText.font = style.font_family;
                    if (Object.prototype.hasOwnProperty.call(style, "color")) object.objectText.color = colorToNative(style.color);
                } else throw new Error("Unsupported native action");
            });
            nativeStage = "save";
            owned.save({}, {timeout: 120});
        }
        nativeStage = "inventory-after";
        const after = inventory(owned, keynote);
        if (request.pdf) {
            nativeStage = "export";
            keynote.export(owned, {to: Path(request.pdf), as: "PDF", withProperties: {skippedSlides: true}}, {timeout: 120});
        }
        operationComplete = true;
        return JSON.stringify({schema_version: 1, status: "ok", keynote_version: version, inventory: after});
    } finally {
        if (owned) {
            // A timed-out Apple event may leave the owned copy open. Python retains
            // its scratch folder on failure and never force-quits the application.
            const previousStage = nativeStage;
            try {
                nativeStage = "close";
                owned.close({saving: "no"}, {timeout: 15});
                nativeStage = previousStage;
            } catch (error) {
                if (operationComplete) throw error;
                nativeStage = previousStage;
            }
        }
    }
}

function colorToNative(hex) {
    return [0, 2, 4].map(function (offset) { return parseInt(hex.slice(offset, offset + 2), 16) * 257; });
}

function colorFromNative(value) {
    if (!Array.isArray(value) || value.length !== 3) throw new Error("Unsupported text color");
    if (value.some(function(part) { return typeof part !== "number" || !Number.isFinite(part) || part < 0 || part > 65535; })) throw new Error("Invalid text color component");
    // Keynote 13.1 JXA reads normalized floats although its dictionary and
    // write interface use 16-bit RGB. Retain compatibility with integer reads.
    const scale = value.every(function(part) { return part <= 1; }) ? 255 : 1 / 257;
    return value.map(function (part) {
        const hex = Math.round(part * scale).toString(16).toUpperCase();
        return hex.length === 1 ? "0" + hex : hex;
    }).join("");
}

function nativeRead(stage, read) {
    nativeStage = stage;
    return read();
}

function pointCoordinates(value) {
    // JXA decodes the Apple-event point as {x, y}; some bridges return a list.
    const point = Array.isArray(value) ? value : [value.x, value.y];
    if (point.length !== 2 || point.some(function (v) { return typeof v !== "number" || !Number.isFinite(v); })) {
        throw new Error("Invalid native point");
    }
    return point;
}

function textObject(object, index) {
    const position = pointCoordinates(nativeRead("inventory-position", function () { return object.position(); }));
    const text = String(nativeRead("inventory-text", function () { return object.objectText(); }));
    let style = {font_size_pt: null, font_family: null, color: null};
    let uniform = true;
    if (text.length) {
        if (text.length > 200000) throw new Error("Text exceeds inventory limit");
        // Resolve whole collection properties in three Apple events, rather than
        // sending three events per character. Never sample only part of the text.
        const sizes = nativeRead("inventory-character-sizes", function () { return object.objectText.characters.size(); });
        const fonts = nativeRead("inventory-character-fonts", function () { return object.objectText.characters.font(); });
        const colors = nativeRead("inventory-character-colors", function () { return object.objectText.characters.color(); });
        if (!Array.isArray(sizes) || !Array.isArray(fonts) || !Array.isArray(colors) || !sizes.length || sizes.length !== fonts.length || sizes.length !== colors.length) throw new Error("Complete character styling inventory unavailable");
        style = {font_size_pt: Number(sizes[0]), font_family: String(fonts[0]), color: colorFromNative(colors[0])};
        uniform = sizes.every(function (size) { return Number(size) === style.font_size_pt; }) &&
            fonts.every(function (font) { return String(font) === style.font_family; }) &&
            colors.every(function (color) { return colorFromNative(color) === style.color; });
    }
    return {index: index, text: text, locked: Boolean(nativeRead("inventory-locked", function () { return object.locked(); })),
        bounds_points: [Number(position[0]), Number(position[1]), Number(nativeRead("inventory-object-width", function () { return object.width(); })), Number(nativeRead("inventory-object-height", function () { return object.height(); }))],
        style: style, uniform_style: uniform};
}

function tableInventory(table, index) {
    const cells = table.cells();
    if (cells.length > 100000) throw new Error("Table exceeds inventory limit");
    return {index: index, rows: Number(table.rowCount()), columns: Number(table.columnCount()),
        cells: cells.map(function (cell) {
            // Values and formulas are compared as exposed by Keynote. Charts and
            // unexposed equation/build internals still require native review.
            const value = cell.value();
            return {name: String(cell.name()), value: value === null || value === undefined ? null : String(value), formula: String(cell.formula() || "")};
        })};
}

function inventory(document, keynote) {
    const slides = nativeRead("inventory-slides", function () { return document.slides(); });
    if (!slides.length || slides.length > 10000) throw new Error("Unsupported slide count");
    return {width: Number(nativeRead("inventory-canvas-width", function () { return document.width(); })), height: Number(nativeRead("inventory-canvas-height", function () { return document.height(); })), slides: slides.map(function (slide, index) {
        const textItems = nativeRead("inventory-textitems", function () { return slide.textItems(); });
        const shapes = nativeRead("inventory-shapes", function () { return slide.shapes(); });
        const tables = nativeRead("inventory-tables", function () { return slide.tables(); });
        // JXA normalizes the dictionary name "iWork item" to iworkItems.
        // The capital-W spelling is not a valid collection specifier.
        // Concrete collections can overlap, so summing them would double-count.
        const itemCount = nativeRead("inventory-iworkitems", function () { return keynote.count(slide.iworkItems); });
        const counts = {text_items: textItems.length, shapes: shapes.length, tables: tables.length,
            images: nativeRead("inventory-images", function () { return slide.images(); }).length,
            charts: nativeRead("inventory-charts", function () { return slide.charts(); }).length,
            lines: nativeRead("inventory-lines", function () { return slide.lines(); }).length,
            movies: nativeRead("inventory-movies", function () { return slide.movies(); }).length,
            audio_clips: nativeRead("inventory-audioclips", function () { return slide.audioClips(); }).length};
        return {slide: index + 1, skipped: Boolean(nativeRead("inventory-skipped", function () { return slide.skipped(); })), notes: String(nativeRead("inventory-notes", function () { return slide.presenterNotes(); })),
            counts: {iwork_items: itemCount, text_items: counts.text_items, shapes: counts.shapes,
                images: counts.images, tables: counts.tables, charts: counts.charts,
                lines: counts.lines, movies: counts.movies, audio_clips: counts.audio_clips},
            text_items: textItems.map(function (object, offset) { return textObject(object, offset + 1); }),
            shapes: shapes.map(function (object, offset) { return textObject(object, offset + 1); }),
            tables: tables.map(function (table, offset) { return tableInventory(table, offset + 1); })};
    })};
}

// Declarative content-changing path. Python validates the complete spec before dispatch.
function authorOperations(doc, app, operations, mode) {
    if (mode === "create") {
        // Keep a temporary initial slide until the first requested slide exists.
        const initial = doc.slides();
        const firstAdd = operations.findIndex(function(o) { return o.action === "add_slide"; });
        if (firstAdd < 0) throw new Error("A new deck needs a slide");
        // Remove defaults only after creation to avoid deleting the final slide.
        addAuthorSlide(doc, app, operations[firstAdd]);
        initial.forEach(function(s) { app.delete(s); });
        operations = operations.slice(); operations.splice(firstAdd, 1);
    }
    operations.forEach(function(op, index) {
        nativeStage = "author-" + op.action + "-" + index;
        let slide = op.slide ? doc.slides[op.slide - 1] : null;
        if (op.slide && (op.slide > doc.slides().length)) throw new Error("Slide selector out of range");
        if (op.action === "set_canvas") { doc.width = op.width; doc.height = op.height; return; }
        if (op.action === "add_slide") { addAuthorSlide(doc, app, op); return; }
        if (op.action === "delete_slide") {
            if (doc.slides().length <= 1) throw new Error("Cannot delete the last slide");
            app.delete(slide); return;
        }
        if (op.action === "duplicate_slide") { app.duplicate(slide); return; }
        if (op.action === "move_slide") {
            if (op.before > doc.slides().length || op.before === op.slide) throw new Error("Invalid move target");
            const previous = inventory(doc, app).slides;
            moveAuthorSlide(doc, op.slide, op.before);
            const current = inventory(doc, app).slides;
            const expected = previous.slice();
            const moved = expected.splice(op.slide - 1, 1)[0];
            expected.splice(op.before - 1 - (op.slide < op.before ? 1 : 0), 0, moved);
            function content(s) { const copy = Object.assign({}, s); delete copy.slide; return JSON.stringify(copy); }
            if (current.length !== previous.length || current.some(function(s, i) { return content(s) !== content(expected[i]); })) throw new Error("Move changed slide content or order");
            return;
        }
        if (op.action === "set_slide") { setAuthorSlide(doc, slide, op); return; }
        let object;
        if (op.action === "set_text") {
            const items = op.kind === "shape" ? slide.shapes : slide.textItems;
            if (op.index > items().length) throw new Error("Text selector out of range");
            object = items[op.index - 1]; object.objectText = op.text;
        } else if (op.action === "add_text" || op.action === "add_shape") {
            object = op.action === "add_text" ? app.TextItem({objectText: op.text}) : app.Shape({objectText: op.text});
            if (op.action === "add_text") slide.textItems.push(object); else slide.shapes.push(object);
        } else if (op.action === "add_table") {
            object = app.Table({rowCount: op.cells.length, columnCount: op.cells[0].length, headerRowCount: 0, headerColumnCount: 0});
            slide.tables.push(object);
            op.cells.forEach(function(row, ri) { row.forEach(function(v, ci) { object.rows[ri].cells[ci].value = v; }); });
        } else if (op.action === "set_cell") {
            if (op.index > slide.tables().length) throw new Error("Table selector out of range");
            object = slide.tables[op.index-1];
            if (op.row > object.rowCount() || op.column > object.columnCount()) throw new Error("Cell selector out of range");
            object.rows[op.row-1].cells[op.column-1].value = op.value; return;
        } else if (op.action === "add_chart") {
            app.addChart(slide, {rowNames: op.rows, columnNames: op.columns, data: op.data, type: op.chart_type, groupBy: "chart row"});
            object = slide.charts[slide.charts().length - 1];
        } else if (op.action === "add_image") {
            object = app.Image({file: Path(op.path)}); slide.images.push(object);
        } else throw new Error("Unsupported authoring operation");
        // Text styling and resizing can reflow or recenter an object in Keynote.
        // Apply the requested position last, after its size has settled.
        if (op.font) object.objectText.font=op.font;
        if (op.size) object.objectText.size=op.size;
        if (op.color) object.objectText.color=colorToNative(op.color);
        if (op.bounds) {
            const b = op.bounds;
            if (b[0]+b[2] > doc.width() || b[1]+b[3] > doc.height()) throw new Error("Object outside canvas");
            object.width=b[2]; object.height=b[3]; object.position = {x:b[0], y:b[1]};
            if (op.action === "add_text") {
                const actual = object.position();
                validateTextFrame(b, [Number(actual.x), Number(actual.y), Number(object.width()), Number(object.height())], op.height_mode || "fixed");
            }
        }
    });
}
function setAuthorSlide(doc, slide, op) {
    if (op.layout) slide.baseLayout = doc.slideLayouts.byName(op.layout);
    if (Object.prototype.hasOwnProperty.call(op, "notes")) slide.presenterNotes=op.notes;
    if (Object.prototype.hasOwnProperty.call(op, "skipped")) slide.skipped=op.skipped;
}
function addAuthorSlide(doc, app, op) {
    const slide=app.Slide(); doc.slides.push(slide);
    slide.titleShowing=false; slide.bodyShowing=false;
    setAuthorSlide(doc, slide, op);
    // Fresh slides without a requested layout must not inherit an extra subtitle
    // placeholder that overlaps content in the editor, even if absent in exports.
    if (!op.layout) slide.iworkItems().forEach(function(item) { app.delete(item); });
    return slide;
}

// JXA's object destination replaces the target slide. A fixed AppleScript
// command expresses a before-insertion location without evaluating request text.
function moveAuthorSlide(doc, from, before) {
    const id = String(doc.id());
    if (!/^[A-Za-z0-9-]+$/.test(id) || !Number.isInteger(from) || !Number.isInteger(before)) throw new Error("Invalid native move selector");
    const source = 'tell application "Keynote"\ntell document id "' + id + '"\nmove slide ' + from + ' to before slide ' + before + '\nend tell\nend tell';
    const script = $.NSAppleScript.alloc.initWithSource(source);
    const error = Ref();
    const result = script.executeAndReturnError(error);
    if (!result) throw new Error("Native before-insertion move failed");
}

function validateTextFrame(expected, actual, mode) {
    if (actual.some(function(v) { return !Number.isFinite(v); }) || actual[0] !== expected[0] || actual[1] !== expected[1] || actual[2] !== expected[2]) throw new Error("Text frame position or width mismatch");
    if (mode === "fit" ? actual[3] <= 0 || actual[3] > expected[3] : actual[3] !== expected[3]) throw new Error("Text frame height mismatch");
}
