"""Python safety/contract tests use mocked native responses, not a Mac fixture.

Opt in to the separate real integration test on macOS with a private fixture and
an actual source-reviewed plan: PALATE_KEYNOTE_FIXTURE and PALATE_KEYNOTE_PLAN.
The integration test never fabricates scientific or native review pass records.
"""
import copy
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("keynote_native", ROOT / "scripts/keynote_native.py")
native = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(native)


def inventory():
    item = {"index": 1, "text": "Evidence and uncertainty", "locked": False,
            "bounds_points": [20, 30, 300, 50], "style": {"font_size_pt": 24, "font_family": "Helvetica", "color": "172D32"},
            "uniform_style": True}
    return {"width": 960, "height": 540, "slides": [
        {"slide": 1, "skipped": False, "notes": "n=6; 25 °C; DOI 10.0000/example", "counts": {"iwork_items": 4, "text_items": 1, "shapes": 1, "charts": 1, "images": 0, "tables": 1, "lines": 0, "movies": 0, "audio_clips": 0},
         "text_items": [item], "shapes": [dict(copy.deepcopy(item), text="", bounds_points=[10, 10, 20, 20])],
         "tables": [{"index": 1, "rows": 1, "columns": 1, "cells": [{"name": "A1", "value": "72.4", "formula": ""}]}]}]}


# Execute the unchanged JXA run/inventory functions with controlled host objects.
# This exercises JavaScript control flow, not Apple events or Mac compatibility.
NODE_JXA_HARNESS = r"""
const fs = require("node:fs");
const path = require("node:path").posix;
const vm = require("node:vm");
const fixture = JSON.parse(fs.readFileSync(0, "utf8"));
const events = [];
function collection(items) {
    const result = () => items;
    items.forEach((item, index) => { result[index] = item; });
    return result;
}
function textObject(item) {
    const object = {locked: () => item.locked};
    for (const [name, read, write] of [
        ["position", () => item.bounds_points.slice(0, 2), value => item.bounds_points.splice(0, 2, ...value)],
        ["width", () => item.bounds_points[2], value => { item.bounds_points[2] = value; }],
        ["height", () => item.bounds_points[3], value => { item.bounds_points[3] = value; }]
    ]) Object.defineProperty(object, name, {get: () => read, set: write});
    object.objectText = () => item.text;
    object.objectText.characters = {
        size: () => [item.style.font_size_pt], font: () => [item.style.font_family],
        color: () => [[0, 2, 4].map(offset => parseInt(item.style.color.slice(offset, offset + 2), 16) * 257)]
    };
    return object;
}
const slides = fixture.inventory.slides.map(slide => {
    const mock = {skipped: () => slide.skipped, presenterNotes: () => slide.notes,
        textItems: collection(slide.text_items.map(textObject)), shapes: collection(slide.shapes.map(textObject)),
        tables: collection(slide.tables.map(table => ({rowCount: () => table.rows, columnCount: () => table.columns,
            cells: collection(table.cells.map(cell => ({name: () => cell.name, value: () => cell.value, formula: () => cell.formula})))})))};
    for (const [method, key] of Object.entries({iWorkItems: "iwork_items", images: "images", charts: "charts", lines: "lines", movies: "movies", audioClips: "audio_clips"})) {
        mock[method] = collection(Array(slide.counts[key]).fill({}));
    }
    return mock;
});
const document = {file: () => fixture.opened_path || fixture.request.document,
    width: () => fixture.inventory.width, height: () => fixture.inventory.height,
    slides: Object.assign(() => { events.push("inventory"); return slides; }, slides),
    save: () => events.push("save"), close: () => events.push("close")};
const dollar = value => ({stringByDeletingLastPathComponent: path.dirname(value), lastPathComponent: path.basename(value)});
dollar.NSString = {stringWithContentsOfFileEncodingError: () => JSON.stringify(fixture.request)};
dollar.NSUTF8StringEncoding = 4;
const context = {$: dollar, ObjC: {import: () => {}, unwrap: value => value}, Path: value => value,
    Application: () => ({version: () => "controlled-jxa-mock", open: () => { events.push("open"); return document; },
        export: () => events.push("export")})};
vm.createContext(context);
vm.runInContext(fixture.adapter_source || fs.readFileSync(process.argv[1], "utf8"), context);
let result = null, error = null;
try { result = JSON.parse(context.run(["/private/run/request.json"])); }
catch (caught) { error = caught.message; }
process.stdout.write(JSON.stringify({result, error, events}));
"""


@unittest.skipUnless(shutil.which("node"), "Controlled JavaScript adapter tests require Node; no Mac is simulated")
class KeynoteJavaScriptControlFlowTests(unittest.TestCase):
    def source_inventory(self):
        data = inventory()
        slide = data["slides"][0]
        # Match the native collector's field order and empty-text style contract.
        slide["counts"] = {key: slide["counts"][key] for key in (
            "iwork_items", "text_items", "shapes", "images", "tables", "charts", "lines", "movies", "audio_clips")}
        slide["shapes"][0]["style"] = {"font_size_pt": None, "font_family": None, "color": None}
        return data

    def run_adapter(self, request, **overrides):
        fixture = {"request": request, "inventory": self.source_inventory(), **overrides}
        result = subprocess.run([shutil.which("node"), "-e", NODE_JXA_HARNESS, str(native.SIDECAR)],
                                input=json.dumps(fixture), text=True, encoding="utf-8", capture_output=True,
                                check=True, timeout=15)
        return json.loads(result.stdout)

    def test_inspect_collects_one_complete_inventory_with_or_without_pdf(self):
        for pdf in (None, "/private/run/preview.pdf"):
            with self.subTest(pdf=pdf):
                result = self.run_adapter({"command": "inspect", "document": "/private/run/inspection.key", "pdf": pdf})
                self.assertIsNone(result["error"])
                self.assertEqual(result["result"]["inventory"], self.source_inventory())
                self.assertEqual(result["events"], ["open", "inventory"] + (["export"] if pdf else []) + ["close"])

    def test_apply_checks_before_and_collects_fresh_inventory_after_save(self):
        bounds = [40, 50, 300, 50]
        result = self.run_adapter({"command": "apply", "document": "/private/run/candidate.key",
                                   "expected_inventory": self.source_inventory(), "operations": [{"slide": 1,
                                   "object_kind": "text_item", "object_index": 1, "action": "geometry", "bounds_points": bounds}]})
        expected = self.source_inventory()
        expected["slides"][0]["text_items"][0]["bounds_points"] = bounds
        self.assertIsNone(result["error"])
        self.assertEqual(result["result"]["inventory"], expected)
        self.assertEqual(result["events"], ["open", "inventory", "save", "inventory", "close"])

    def test_apply_mismatch_fails_before_edits_and_closes_only_owned_copy(self):
        stale = self.source_inventory()
        stale["slides"][0]["notes"] = "Changed source note"
        result = self.run_adapter({"command": "apply", "document": "/private/run/candidate.key",
                                   "expected_inventory": stale, "operations": []})
        self.assertEqual(result["error"], "Source inventory changed")
        self.assertEqual(result["events"], ["open", "inventory", "close"])
        unrelated = self.run_adapter({"command": "inspect", "document": "/private/run/inspection.key"},
                                     opened_path="/private/unrelated.key")
        self.assertEqual(unrelated["error"], "Keynote returned a different document")
        self.assertEqual(unrelated["events"], ["open"])


class KeynoteNativeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.source = self.fixture("source.key")
        self.digest = native.source_identity(self.source)[1]
        self.original = self.source.read_bytes()

    def fixture(self, name, bundle=False):
        path = self.folder / name
        parts = {"Index/Document.iwa": b"synthetic document", "Index/Slide-1.iwa": b"synthetic slide", "Data/figure.png": b"synthetic scientific figure"}
        if bundle:
            for name, value in parts.items():
                member = path / name
                member.parent.mkdir(parents=True, exist_ok=True)
                member.write_bytes(value)
        else:
            with zipfile.ZipFile(path, "w") as archive:
                for name, value in parts.items():
                    archive.writestr(name, value)
        return path

    def plan(self, action="geometry", kind="text_item"):
        operation = {"slide": 1, "object_kind": kind, "object_index": 1,
                     "action": action, "reason": "Separate the existing heading from its evidence.", "rule_ids": []}
        operation.update({"bounds_points": [40, 50, 300, 50]} if action == "geometry" else {"style": {"font_size_pt": 28, "color": "217A80"}})
        return {"schema_version": 1, "source_sha256": self.digest, "inspection_sha256": native.canonical_hash(inventory()),
                "source_review": {"source_sha256": self.digest, "reviewed_slides": [1], "target_safety_status": "passed",
                                  "reviewer": "Synthetic test reviewer", "evidence": ["Synthetic test contract only; no Mac review"]},
                "operations": [operation]}

    def response(self, request, workspace, timeout=180):
        if request.get("pdf"):
            Path(request["pdf"]).write_bytes(b"%PDF-1.7\nsynthetic fixture reference")
        data = copy.deepcopy(request.get("expected_inventory", inventory()))
        if request["command"] == "apply":
            for operation in request["operations"]:
                objects = data["slides"][operation["slide"] - 1]["text_items" if operation["object_kind"] == "text_item" else "shapes"]
                item = objects[operation["object_index"] - 1]
                if operation["action"] == "geometry":
                    item["bounds_points"] = operation["bounds_points"]
                else:
                    item["style"].update(operation["style"])
        return {"schema_version": 1, "status": "ok", "keynote_version": "synthetic-test", "inventory": data}

    def inspection(self, source, pdf=None):
        return {"schema_version": 1, "source_sha256": native.source_identity(source)[1], "inventory": inventory(),
                "inspection_sha256": native.canonical_hash(inventory()), "keynote_version": "synthetic-test"}

    def test_wrong_os_probe_and_inspection_fail_without_copy_or_launch(self):
        with patch.object(native.platform, "system", return_value="Windows"), patch.object(native.subprocess, "run") as run, patch.object(native, "copy_new") as copied:
            result = native.probe()
            self.assertFalse(result["available"])
            self.assertEqual(result["adapter_status"], "experimental-mac-unverified")
            with self.assertRaisesRegex(ValueError, "macOS"):
                native.inspect_native(self.source)
            run.assert_not_called(); copied.assert_not_called()

    def test_credentials_unknown_legacy_and_misleading_extensions_are_excluded(self):
        header = b"-----BEGIN " + b"PRIVATE KEY-----\nsynthetic secret"
        for name, content in [("credential.key", header), ("text.key", b"not a presentation"), ("pdf.key", b"%PDF-1.7\n")]:
            path = self.folder / name; path.write_bytes(content)
            with self.assertRaises(ValueError):
                native.source_identity(path)
        with zipfile.ZipFile(self.folder / "legacy.key", "w") as archive:
            archive.writestr("index.apxl", "synthetic")
        with self.assertRaises(ValueError):
            native.source_identity(self.folder / "legacy.key")

    def test_native_inspection_opens_only_private_copy_and_preserves_source(self):
        seen = []
        def response(request, workspace):
            self.assertNotEqual(Path(request["document"]), self.source)
            self.assertTrue(Path(request["document"]).is_relative_to(workspace))
            seen.append(Path(request["document"]))
            return self.response(request, workspace)
        with patch.object(native, "require_native_environment"), patch.object(native, "invoke_native", side_effect=response):
            result = native.inspect_native(self.source, self.folder / "source.pdf")
        self.assertEqual(result["source_sha256"], self.digest)
        self.assertEqual(result["content_review"], "pending")
        self.assertEqual(self.source.read_bytes(), self.original)
        self.assertFalse(seen[0].exists())
        self.assertTrue((self.folder / "source.pdf").exists())

    def test_directory_bundle_inspection_and_copy_hash_preserve_all_members(self):
        bundle = self.fixture("bundle.key", bundle=True)
        original = native.source_identity(bundle)[1]
        with patch.object(native, "require_native_environment"), patch.object(native, "invoke_native", side_effect=self.response):
            result = native.inspect_native(bundle)
        self.assertEqual(result["source_sha256"], original)
        self.assertEqual(native.source_identity(bundle)[1], original)

    def test_plan_binds_full_source_hash_and_native_inventory_order(self):
        plan = self.plan()
        self.assertEqual(native.planned_inventory(self.digest, inventory(), plan)["slides"][0]["text_items"][0]["bounds_points"], [40, 50, 300, 50])
        for field in ("source_sha256", "inspection_sha256"):
            changed = copy.deepcopy(plan); changed[field] = "0" * 64
            with self.assertRaisesRegex(ValueError, "stale"):
                native.planned_inventory(self.digest, inventory(), changed)

    def test_unknown_fields_and_replacement_text_are_refused(self):
        for level in ("top", "operation", "style"):
            plan = self.plan("text_style")
            if level == "top": plan["context"] = {}
            elif level == "operation": plan["operations"][0]["text"] = "replace claim"
            else: plan["operations"][0]["style"]["text"] = "replace claim"
            with self.assertRaises(ValueError):
                native.planned_inventory(self.digest, inventory(), plan)

    def test_invalid_selector_type_bounds_and_actions_are_refused(self):
        for field, value in [("slide", True), ("slide", 0), ("object_index", 2), ("object_kind", "chart"), ("action", "rewrite")]:
            plan = self.plan(); plan["operations"][0][field] = value
            with self.assertRaises(ValueError): native.planned_inventory(self.digest, inventory(), plan)
        for bounds in ([0, 0, 0, 1], [-1, 0, 1, 1], [0, 0, 961, 1], [0, 0, float("nan"), 1], [True, 1, 1, 1], [0, 0, 1]):
            plan = self.plan(); plan["operations"][0]["bounds_points"] = bounds
            with self.assertRaises(ValueError): native.planned_inventory(self.digest, inventory(), plan)

    def test_shape_geometry_is_placement_only(self):
        plan = self.plan(kind="shape")
        with self.assertRaisesRegex(ValueError, "placement only"):
            native.planned_inventory(self.digest, inventory(), plan)
        plan["operations"][0]["bounds_points"] = [40, 50, 20, 20]
        native.planned_inventory(self.digest, inventory(), plan)

    def test_locked_mixed_and_math_targets_are_refused(self):
        for mutation in ({"locked": True}, {"uniform_style": False}, {"text": "ΔG = −RT ln K"}):
            data = inventory(); data["slides"][0]["text_items"][0].update(mutation)
            plan = self.plan("text_style"); plan["inspection_sha256"] = native.canonical_hash(data)
            with self.assertRaises(ValueError): native.planned_inventory(self.digest, data, plan)

    def test_text_styles_use_bounded_types_and_plain_hex(self):
        for style in ({"font_family": "Bad\nFont"}, {"color": "#217A80"}, {"bold": True}):
            plan = self.plan("text_style"); plan["operations"][0]["style"] = style
            with self.assertRaises(ValueError): native.planned_inventory(self.digest, inventory(), plan)

    def test_font_size_refuses_nonfinite_nonnumeric_and_out_of_range_values(self):
        for size in (0, -1, 0.5, 512.5, 10 ** 1000, True, False, "10.5", None,
                     float("nan"), float("inf"), -float("inf")):
            with self.subTest(size=repr(size)):
                plan = self.plan("text_style")
                plan["operations"][0]["style"] = {"font_size_pt": size}
                with self.assertRaisesRegex(ValueError, "finite number between 1 and 512"):
                    native.planned_inventory(self.digest, inventory(), plan)

    def test_integer_and_fractional_font_sizes_survive_planned_inventory_roundtrip(self):
        for size in (1, 1.0, 2.5, 10.5, 12, 16.0, 511.75, 512):
            with self.subTest(size=size):
                plan = self.plan("text_style")
                plan["operations"][0]["style"] = {"font_size_pt": size}
                source = inventory()
                expected = native.planned_inventory(self.digest, source, plan)
                actual = native.validate_inventory(json.loads(json.dumps(expected, allow_nan=False)))
                self.assertEqual(actual["slides"][0]["text_items"][0]["style"]["font_size_pt"], size)
                self.assertEqual(native.compare_inventory(expected, actual), [])
                self.assertEqual(source, inventory())

    def test_inventory_comparison_detects_rounded_fractional_font_size(self):
        plan = self.plan("text_style")
        plan["operations"][0]["style"] = {"font_size_pt": 10.5}
        expected = native.planned_inventory(self.digest, inventory(), plan)
        rounded = copy.deepcopy(expected)
        rounded["slides"][0]["text_items"][0]["style"]["font_size_pt"] = 10
        self.assertTrue(native.compare_inventory(expected, rounded))

    def test_source_review_requires_all_slides_actual_identity_and_evidence(self):
        for field, value in [("source_sha256", "0" * 64), ("reviewed_slides", []), ("reviewed_slides", [True]), ("reviewer", ""), ("evidence", []), ("target_safety_status", "pending")]:
            plan = self.plan(); plan["source_review"][field] = value
            with self.assertRaises(ValueError): native.planned_inventory(self.digest, inventory(), plan)

    def test_exposed_text_notes_table_flags_and_counts_change_fails_comparison(self):
        for key, value in [("notes", "modified"), ("skipped", True), ("counts", {}), ("tables", [])]:
            changed = inventory(); changed["slides"][0][key] = value
            self.assertTrue(native.compare_inventory(inventory(), changed))

    def test_existing_or_nested_output_paths_never_overwrite(self):
        with self.assertRaises(ValueError): native.fresh_paths(self.source)
        with self.assertRaises(ValueError): native.fresh_paths(self.folder / "same", self.folder / "same")
        with self.assertRaises(ValueError): native.fresh_paths(self.folder / "new.key", self.folder / "new.key" / "receipt.json")
        bundle = self.fixture("bundle.key", bundle=True)
        with self.assertRaises(ValueError): native.outputs_outside_sources([bundle], [bundle / "receipt.json"])
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_apply_writes_native_candidate_pdf_and_pending_receipt_without_conversion(self):
        plan = self.plan()
        expected = native.planned_inventory(self.digest, inventory(), plan)
        def inspect(source, pdf=None):
            result = self.inspection(source, pdf)
            if Path(source).name == "candidate.key": result["inventory"] = copy.deepcopy(expected)
            return result
        output, receipt, pdf = (self.folder / name for name in ("candidate.key", "receipt.json", "candidate.pdf"))
        with patch.object(native, "inspect_native", side_effect=inspect), patch.object(native, "invoke_native", side_effect=self.response):
            result = native.apply(self.source, plan, output, receipt, pdf)
        self.assertEqual(result["status"], "candidate")
        self.assertEqual(result["exposed_inventory_status"], "passed")
        self.assertEqual(result["playback_review"], "pending")
        self.assertEqual(output.read_bytes(), self.original)
        self.assertEqual(self.source.read_bytes(), self.original)
        self.assertTrue(pdf.read_bytes().startswith(b"%PDF-"))
        self.assertEqual(json.loads(receipt.read_text())["candidate_sha256"], native.source_identity(output)[1])

    def test_apply_inventory_mismatch_publishes_nothing_and_preserves_source(self):
        def response(request, workspace):
            result = self.response(request, workspace)
            result["inventory"]["slides"][0]["notes"] = "unexpected changed note"
            return result
        output, receipt, pdf = (self.folder / name for name in ("candidate.key", "receipt.json", "candidate.pdf"))
        with patch.object(native, "inspect_native", side_effect=self.inspection), patch.object(native, "invoke_native", side_effect=response):
            with self.assertRaisesRegex(ValueError, "inventory differs"):
                native.apply(self.source, self.plan(), output, receipt, pdf)
        self.assertFalse(any(path.exists() for path in (output, receipt, pdf)))
        self.assertEqual(self.source.read_bytes(), self.original)
        self.assertTrue(list(self.folder.glob("palate-keynote-*")))

    def test_save_reopen_mismatch_is_not_delivered(self):
        with patch.object(native, "inspect_native", side_effect=self.inspection), patch.object(native, "invoke_native", side_effect=self.response):
            with self.assertRaisesRegex(ValueError, "reopen"):
                native.apply(self.source, self.plan(), self.folder / "candidate.key", self.folder / "receipt.json", self.folder / "candidate.pdf")
        self.assertFalse((self.folder / "candidate.key").exists())

    def test_invalid_pdf_does_not_publish_any_requested_output(self):
        expected = native.planned_inventory(self.digest, inventory(), self.plan())
        def inspect(source, pdf=None):
            result = self.inspection(source, pdf)
            if Path(source).name == "candidate.key": result["inventory"] = expected
            return result
        def response(request, workspace):
            result = self.response(request, workspace)
            Path(request["pdf"]).write_bytes(b"invalid PDF")
            return result
        paths = [self.folder / name for name in ("candidate.key", "receipt.json", "candidate.pdf")]
        with patch.object(native, "inspect_native", side_effect=inspect), patch.object(native, "invoke_native", side_effect=response):
            with self.assertRaisesRegex(ValueError, "PDF reference"):
                native.apply(self.source, self.plan(), *paths)
        self.assertFalse(any(path.exists() for path in paths))

    def test_apply_publication_error_rolls_back_only_its_own_new_outputs(self):
        expected = native.planned_inventory(self.digest, inventory(), self.plan())
        def inspect(source, pdf=None):
            result = self.inspection(source, pdf)
            if Path(source).name == "candidate.key": result["inventory"] = expected
            return result
        paths = [self.folder / name for name in ("candidate.key", "receipt.json", "candidate.pdf")]
        untouched = self.folder / "untouched.txt"; untouched.write_text("retain existing user work")
        with patch.object(native, "inspect_native", side_effect=inspect), patch.object(native, "invoke_native", side_effect=self.response), patch.object(native, "save_json", side_effect=OSError("synthetic disk failure")):
            with self.assertRaises(OSError): native.apply(self.source, self.plan(), *paths)
        self.assertFalse(any(path.exists() for path in paths))
        self.assertEqual(untouched.read_text(), "retain existing user work")
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_native_subprocess_arguments_are_not_shell_interpolated(self):
        workspace = self.folder / "scratch $() quote ' \u65e5\u672c\u8a9e"; workspace.mkdir()
        request = {"command": "inspect", "document": "/private/copy $(echo forbidden).key"}
        completed = subprocess.CompletedProcess([], 0, json.dumps({"schema_version": 1, "status": "ok"}), "")
        with patch.object(native.platform, "system", return_value="Darwin"), patch.object(Path, "is_file", return_value=True), patch.object(native.subprocess, "run", return_value=completed) as run:
            native.invoke_native(request, workspace)
        arguments, keywords = run.call_args
        self.assertEqual(arguments[0], [str(Path("/usr/bin/osascript")), "-l", "JavaScript", str(native.SIDECAR), str(workspace / "request.json")])
        self.assertNotIn("shell", keywords)
        self.assertEqual(json.loads((workspace / "request.json").read_text()), request)

    def test_missing_osascript_and_native_error_json_timeout_are_safe(self):
        with patch.object(native.platform, "system", return_value="Darwin"), patch.object(Path, "is_file", return_value=False):
            with self.assertRaisesRegex(ValueError, "unavailable"): native.require_native_environment()
        for output in ("not json", json.dumps({"schema_version": 1, "status": "failed"})):
            work = Path(tempfile.mkdtemp(dir=self.folder))
            with patch.object(native.platform, "system", return_value="Darwin"), patch.object(Path, "is_file", return_value=True), patch.object(native.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, output, "")):
                with self.assertRaises(ValueError): native.invoke_native({"command": "probe"}, work)
        work = Path(tempfile.mkdtemp(dir=self.folder))
        with patch.object(native.platform, "system", return_value="Darwin"), patch.object(Path, "is_file", return_value=True), patch.object(native.subprocess, "run", side_effect=subprocess.TimeoutExpired("osascript", 180)):
            with self.assertRaisesRegex(ValueError, "timed out"): native.invoke_native({"command": "probe"}, work)

    def test_native_stderr_with_source_text_is_not_echoed(self):
        work = Path(tempfile.mkdtemp(dir=self.folder))
        with patch.object(native.platform, "system", return_value="Darwin"), patch.object(Path, "is_file", return_value=True), patch.object(native.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "private scientific text")):
            with self.assertRaises(ValueError) as caught: native.invoke_native({"command": "probe"}, work)
        self.assertNotIn("private scientific text", str(caught.exception))

    def final_review(self, candidate):
        return {"source_sha256": self.digest, "candidate_sha256": native.source_identity(candidate)[1], "reviewed_slides": [1],
                "native_application": "Keynote", "reviewer": "Synthetic test reviewer", "evidence": ["Synthetic fixture review record only"],
                "visual_status": "passed", "scientific_status": "passed", "editability_status": "passed", "playback_status": "passed",
                "protected_content_status": "passed", "remaining_issues": []}

    def validation_result(self, candidate):
        return {"schema_version": 1, "status": "candidate", "source_sha256": self.digest, "candidate_sha256": native.source_identity(candidate)[1], "slide_count": 1, "errors": []}

    def test_finalizer_refuses_stale_or_unreviewed_native_candidate(self):
        candidate = self.fixture("candidate.key")
        for field, value in [("candidate_sha256", "0" * 64), ("native_application", "PowerPoint"), ("visual_status", "pending"), ("playback_status", "pending"), ("protected_content_status", "pending"), ("remaining_issues", ["unverified chart"]), ("reviewed_slides", [])]:
            review = self.final_review(candidate); review[field] = value
            with patch.object(native, "validate", return_value=self.validation_result(candidate)):
                with self.assertRaises(ValueError): native.finalize(self.source, candidate, self.plan(), review, self.folder / "final.key", self.folder / "report.md")
        self.assertFalse((self.folder / "final.key").exists())

    def test_finalizer_marks_manual_judgments_as_recorded_and_copies_exact_bytes(self):
        candidate = self.fixture("candidate.key")
        output, report = self.folder / "final.key", self.folder / "report.md"
        with patch.object(native, "validate", return_value=self.validation_result(candidate)):
            result = native.finalize(self.source, candidate, self.plan(), self.final_review(candidate), output, report)
        self.assertEqual(result["status"], "finalized-as-reviewed")
        self.assertEqual(result["playback_review"], "passed_as_recorded")
        self.assertEqual(output.read_bytes(), candidate.read_bytes())
        self.assertIn("does not independently prove", report.read_text())
        self.assertTrue(Path(str(report) + ".validation.json").exists())

    def test_finalizer_publication_error_rolls_back_owned_final_and_report(self):
        candidate = self.fixture("candidate.key")
        output, report = self.folder / "final.key", self.folder / "report.md"
        with patch.object(native, "validate", return_value=self.validation_result(candidate)), patch.object(native, "save_json", side_effect=OSError("synthetic receipt failure")):
            with self.assertRaises(OSError): native.finalize(self.source, candidate, self.plan(), self.final_review(candidate), output, report)
        self.assertFalse(output.exists()); self.assertFalse(report.exists())
        self.assertEqual(candidate.read_bytes(), self.original)

    def test_incomplete_or_nonfinite_native_inventory_is_refused(self):
        for data in ({}, dict(inventory(), width=float("nan"))):
            with self.assertRaises(ValueError): native.validate_inventory(data)
        data = inventory(); del data["slides"][0]["notes"]
        with self.assertRaises(ValueError): native.validate_inventory(data)


@unittest.skipUnless(platform.system() == "Darwin" and os.environ.get("PALATE_KEYNOTE_FIXTURE") and os.environ.get("PALATE_KEYNOTE_PLAN"), "Requires a real Mac, Keynote and a private fixture with an actual source-reviewed plan")
class KeynoteMacIntegrationTests(unittest.TestCase):
    def test_native_fixture_inspect_apply_save_pdf_and_reopen(self):
        source = Path(os.environ["PALATE_KEYNOTE_FIXTURE"])
        plan = native.load_json(os.environ["PALATE_KEYNOTE_PLAN"])
        before = native.source_identity(source)[1]
        with tempfile.TemporaryDirectory(prefix="palate-live-keynote-") as directory:
            folder = Path(directory)
            inspection = native.inspect_native(source, folder / "source.pdf")
            self.assertEqual(inspection["source_sha256"], before)
            result = native.apply(source, plan, folder / "candidate.key", folder / "receipt.json", folder / "candidate.pdf")
            self.assertEqual(result["status"], "candidate")
            recheck = native.validate(source, folder / "candidate.key", plan)
            self.assertEqual(recheck["exposed_inventory_status"], "passed")
            self.assertEqual(recheck["visual_review"], "pending")
        self.assertEqual(native.source_identity(source)[1], before)


if __name__ == "__main__":
    unittest.main()
