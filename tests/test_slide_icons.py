"""Check offline icon provenance, inert SVG content and runtime-package boundaries."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("slide_icon_packager", ROOT / "scripts/package_skill.py")
packager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(packager)
ICON_DIRECTORY = "assets/slide-icons/"
UPSTREAM_COMMIT = "1ef60af944de207e0d5176905a0759ba12e6ee8d"
# SHA-256 of the exact downloads from the pinned official Lucide commit.
UPSTREAM_HASHES = {
    "sun.svg": "a3955c8b0425fcc5c9ba12d2bdd77fe53b2cd5dd05e7742a56f342e996fb2ef8",
    "solar-panel.svg": "05acf7dc98497c7a57f6d4bf2a7b33436b8787cd7b0d374de350d7c2f703073d",
    "battery-charging.svg": "6a95bf102235d7070121bb8eb21a4836fa7ea9f0dbe8327eadbdf94253acdcbd",
    "house.svg": "28216c479005731ef5e382e7d8627eda2b129b019eb1f3d9de9f5915576d448e",
    "factory.svg": "5482b8d73276e072a951f4c1be530d31efa584c8d1a7affbeec22a560f0d5cc0",
    "network.svg": "626be730feea1e5ea7539fbf78b4a3fcb927ce5d7dc43364f2216908672ac792",
    "boxes.svg": "7e301f6c38337389f5a96675d14cb9d8ef8a613329e99c3dfcf7c635bdd1faae",
    "cpu.svg": "ec83bb69ec029d367d749afc445b39c8e95891ebf99b0400652677c2b149b99c",
    "cloud-rain.svg": "4230ba9d28d0a02c088ec0b21079b63aed9f2b7ee8493588adf34ee144bc307b",
    "wheat.svg": "d18be93cdd1ea09f28e66c69c04927c5f919c09a3bc6d7553ebb1fc85a5b828d",
    "coins.svg": "bcfec9236fd10d0aadbf90951f61dd31ec7cedc72dd38d2639f95c2b8437b9f1",
    "sliders-horizontal.svg": "e43a00e5eb684e6cbb61083bed2528d7a3fa5f265693eb2b5f314cd432aa65f4",
    "dna.svg": "fb1e39ad72394a4090aaaeb620fc8057d72e3df9497cbbbd26247ba57e747431",
    "microscope.svg": "72fab65c4fdd0a7d784485dc7aaa8bf8c4fba9a4dc9ae38a6538e58bdd8b5f42",
    "LICENSE": "b495047bd93a9b06913511076f504daba17d5bbeb3e0650f3bb53a4220329c57",
}


class SlideIconTests(unittest.TestCase):
    def test_assets_are_unmodified_pinned_upstream_downloads(self):
        directory = ROOT / ICON_DIRECTORY
        self.assertEqual({file.name for file in directory.iterdir()}, set(UPSTREAM_HASHES) | {"NOTICE.md"})
        for name, checksum in UPSTREAM_HASHES.items():
            with self.subTest(asset=name):
                self.assertEqual(hashlib.sha256((directory / name).read_bytes()).hexdigest(), checksum)
        notice = (directory / "NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("https://github.com/lucide-icons/lucide/tree/" + UPSTREAM_COMMIT + "/icons", notice)
        self.assertIn("[LICENSE](LICENSE)", notice)

    def test_svg_files_are_real_static_geometry_without_active_or_external_content(self):
        namespace = "{http://www.w3.org/2000/svg}"
        shape_attributes = {
            "path": {"d"}, "circle": {"cx", "cy", "r"},
            "rect": {"x", "y", "width", "height", "rx", "ry"},
        }
        root_attributes = {
            "width": "24", "height": "24", "viewBox": "0 0 24 24", "fill": "none",
            "stroke": "currentColor", "stroke-width": "2",
            "stroke-linecap": "round", "stroke-linejoin": "round",
        }
        for file in sorted((ROOT / ICON_DIRECTORY).glob("*.svg")):
            with self.subTest(asset=file.name):
                data = file.read_bytes()
                self.assertNotIn(b"<!DOCTYPE", data.upper())
                self.assertNotIn(b"<!ENTITY", data.upper())
                root = ET.fromstring(data)
                self.assertEqual(root.tag, namespace + "svg")
                self.assertEqual(root.attrib, root_attributes)
                self.assertGreater(len(root), 0, "An empty placeholder is not an icon")
                for element in root.iter():
                    self.assertFalse((element.text or "").strip(), "Icons must not contain hidden or visible text")
                    if element is root:
                        continue
                    tag = element.tag.removeprefix(namespace)
                    self.assertIn(tag, shape_attributes)
                    self.assertTrue(element.tag.startswith(namespace))
                    self.assertTrue(set(element.attrib).issubset(shape_attributes[tag]))
                    self.assertGreater(len(element.attrib), 0)
                    self.assertEqual(len(element), 0)
                    for value in element.attrib.values():
                        self.assertNotIn("url(", value.lower())
                        self.assertNotIn(":", value)
                        self.assertNotIn("#", value)

    def test_runtime_package_contains_only_reviewed_assets_and_full_license(self):
        expected = {ICON_DIRECTORY + name for name in set(UPSTREAM_HASHES) | {"NOTICE.md"}}
        expected |= {"assets/closing-backgrounds/NOTICE.md",
                     "assets/closing-backgrounds/coastal-panorama.png",
                     "assets/closing-backgrounds/transmission-tower.png",
                     "assets/closing-backgrounds/solar-diagonal.png"}
        allowed = {name for name in packager.FILES if name.startswith("assets/")}
        self.assertEqual(allowed, expected)
        temporary_root = ROOT / "analysis/local-only/test-temp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="palate-slide-icons-", dir=temporary_root) as temporary:
            folder = Path(temporary)
            source = folder / "source"
            for name in packager.FILES:
                target = source / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / name).read_bytes())
            for name in ("assets/slide-icons/unreviewed.svg", "assets/slide-icons/private-notes.md", "assets/icons/sun.svg",
                         "assets/closing-backgrounds/unreviewed.png", "assets/closure_slide/reference.pptx"):
                target = source / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("Synthetic unreviewed material", encoding="utf-8")
            archive_path = folder / "palate.zip"
            with patch.object(packager, "ROOT", source):
                manifest = packager.build(archive_path)
            with zipfile.ZipFile(archive_path) as archive:
                assets = {name.removeprefix("palate/") for name in archive.namelist() if name.startswith("palate/assets/")}
                self.assertEqual(assets, expected)
                for name in expected:
                    self.assertEqual(archive.read("palate/" + name), (ROOT / name).read_bytes())
                    self.assertEqual(manifest["files"][name], hashlib.sha256(archive.read("palate/" + name)).hexdigest())


if __name__ == "__main__":
    unittest.main()
