/* Fixed JXA adapter. Experimental: JavaScript syntax checked, not run on macOS.
 * Never evaluate request text as code. Open and close only the private copy named
 * by the Python orchestrator; do not save, close, activate or quit other documents.
 */
ObjC.import("Foundation");

function run(argv) {
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
    const keynote = Application("com.apple.iWork.Keynote");
    let owned = null;
    try {
        const version = String(keynote.version());
        if (request.command === "probe") {
            return JSON.stringify({schema_version: 1, status: "ok", keynote_version: version});
        }
        if (!["inspect", "apply"].includes(request.command)) throw new Error("Unknown native operation");
        // JXA Apple event modifiers are a final argument, not an application method.
        // This path is a freshly created private copy, never the user's source.
        let opened = keynote.open(Path(request.document), {timeout: 120});
        if (Array.isArray(opened)) opened = opened[0];
        if (!opened) throw new Error("Keynote did not open the copy");
        // Do not assume the app returned the requested document. Claim ownership
        // only after its actual file path matches the newly created scratch copy.
        // A mismatch is deliberately not closed, because it may be unrelated.
        if (opened.file().toString() !== request.document) throw new Error("Keynote returned a different document");
        owned = opened;
        const before = inventory(owned);
        if (request.command === "apply") {
            if (JSON.stringify(before) !== JSON.stringify(request.expected_inventory)) throw new Error("Source inventory changed");
            request.operations.forEach(function (operation) {
                const slide = owned.slides[operation.slide - 1];
                const object = operation.object_kind === "text_item" ? slide.textItems[operation.object_index - 1] : slide.shapes[operation.object_index - 1];
                if (operation.action === "geometry") {
                    object.position = operation.bounds_points.slice(0, 2);
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
            owned.save({}, {timeout: 120});
        }
        // Inspection makes no edits; reuse its complete inventory. Apply still
        // collects the saved result independently of the expected-before guard.
        const after = request.command === "apply" ? inventory(owned) : before;
        if (request.pdf) {
            keynote.export(owned, {to: Path(request.pdf), as: "PDF", withProperties: {skippedSlides: true}}, {timeout: 120});
        }
        return JSON.stringify({schema_version: 1, status: "ok", keynote_version: version, inventory: after});
    } finally {
        if (owned) {
            // A timed-out Apple event may leave the owned copy open. Python retains
            // its scratch folder on failure and never force-quits the application.
            owned.close({saving: "no"}, {timeout: 15});
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

function textObject(object, index) {
    const position = object.position();
    const text = String(object.objectText());
    let style = {font_size_pt: null, font_family: null, color: null};
    let uniform = true;
    if (text.length) {
        if (text.length > 200000) throw new Error("Text exceeds inventory limit");
        // Resolve whole collection properties in three Apple events, rather than
        // sending three events per character. Never sample only part of the text.
        const sizes = object.objectText.characters.size();
        const fonts = object.objectText.characters.font();
        const colors = object.objectText.characters.color();
        if (!Array.isArray(sizes) || !Array.isArray(fonts) || !Array.isArray(colors) || !sizes.length || sizes.length !== fonts.length || sizes.length !== colors.length) throw new Error("Complete character styling inventory unavailable");
        style = {font_size_pt: Number(sizes[0]), font_family: String(fonts[0]), color: colorFromNative(colors[0])};
        uniform = sizes.every(function (size) { return Number(size) === style.font_size_pt; }) &&
            fonts.every(function (font) { return String(font) === style.font_family; }) &&
            colors.every(function (color) { return colorFromNative(color) === style.color; });
    }
    return {index: index, text: text, locked: Boolean(object.locked()),
        bounds_points: [Number(position[0]), Number(position[1]), Number(object.width()), Number(object.height())],
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

function inventory(document) {
    const slides = document.slides();
    if (!slides.length || slides.length > 10000) throw new Error("Unsupported slide count");
    return {width: Number(document.width()), height: Number(document.height()), slides: slides.map(function (slide, index) {
        const textItems = slide.textItems();
        const shapes = slide.shapes();
        const tables = slide.tables();
        return {slide: index + 1, skipped: Boolean(slide.skipped()), notes: String(slide.presenterNotes()),
            counts: {iwork_items: slide.iWorkItems().length, text_items: textItems.length, shapes: shapes.length,
                images: slide.images().length, tables: tables.length, charts: slide.charts().length,
                lines: slide.lines().length, movies: slide.movies().length, audio_clips: slide.audioClips().length},
            text_items: textItems.map(function (object, offset) { return textObject(object, offset + 1); }),
            shapes: shapes.map(function (object, offset) { return textObject(object, offset + 1); }),
            tables: tables.map(function (table, offset) { return tableInventory(table, offset + 1); })};
    })};
}
