/* Fixed JXA adapter. Experimental: bounded single-slide smoke test passed on macOS 27.0.1 / Keynote 13.1.
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
        if (!["inspect", "apply"].includes(request.command)) throw new Error("Unknown native operation");
        // JXA Apple event modifiers are a final argument, not an application method.
        // This path is a freshly created private copy, never the user's source.
        nativeStage = "open";
        let opened = keynote.open(Path(request.document), {timeout: 120});
        if (Array.isArray(opened)) opened = opened[0];
        if (!opened) throw new Error("Keynote did not open the copy");
        // Do not assume the app returned the requested document. Claim ownership
        // only after its actual file path matches the newly created scratch copy.
        // A mismatch is deliberately not closed, because it may be unrelated.
        nativeStage = "document-identity";
        if (opened.file().toString() !== request.document) throw new Error("Keynote returned a different document");
        owned = opened;
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
    return value.map(function (part) {
        const hex = Math.round(part / 257).toString(16).toUpperCase();
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
