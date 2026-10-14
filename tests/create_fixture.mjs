// Synthetic, nonresearch integration fixture authored with the bundled presentation SDK.
// Usage: node create_fixture.mjs <artifact-module> <presentation-skill-dir> <python> <task-dir>
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [modulePath, presentationSkill, python, taskDir] = process.argv.slice(2);
if (!taskDir) throw new Error('Supply artifact module, presentation skill, Python and task directory');
process.env.RUNTIME_NODE_MODULES ??= path.resolve(path.dirname(modulePath), '../../..');
const { Presentation, PresentationFile } = await import(pathToFileURL(path.resolve(modulePath)).href);
const { finalizePresentation, applyPresentationChartFont } = await import(pathToFileURL(path.join(presentationSkill, 'container_tools/artifact_tool_utils.mjs')).href);
const workspaceDir = path.resolve(taskDir);
const buildDir = path.join(workspaceDir, 'build');
const finalPath = path.join(workspaceDir, 'outputs', 'synthetic-source.pptx');
await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(path.dirname(finalPath), { recursive: true });
if (await fs.stat(finalPath).catch(() => null)) throw new Error('Fixture exists; choose a new task directory');

const deck = Presentation.create({ slideSize: { width: 960, height: 540 } });
deck.theme.defaultFont = 'Arial';
function text(slide, name, content, box, size = 20, color = '#172B30', bold = false) {
  const shape = slide.shapes.add({ name, geometry: 'textbox', position: box, fill: 'none', line: { fill: 'none', width: 0 } });
  shape.text = content;
  shape.text.style = { fontFamily: 'Arial', fontSize: size, color, bold };
  return shape;
}
const a = deck.slides.add();
a.background.fill = '#FFFFFF';
text(a, 'title', 'Synthetic concentration comparison (1/2)', { left: 48, top: 36, width: 860, height: 58 }, 28, '#172B30', true);
const chart = a.charts.add('bar', {
  position: { left: 48, top: 125, width: 470, height: 305 },
  categories: ['Day 1', 'Day 2', 'Day 3'],
  series: [{ name: 'Series A', values: [12, 14, 13], fill: '#217A80' }, { name: 'Series B', values: [8, 9, 10], fill: '#B77932' }],
  hasLegend: true,
  legend: { position: 'bottom' },
  barOptions: { direction: 'column', grouping: 'clustered' },
  yAxis: { title: 'Concentration (mg/L)', minimumScale: 0, maximumScale: 16 },
  dataLabels: { showValue: true },
});
applyPresentationChartFont(chart, { fontFamily: 'Arial' });
text(a, 'explanation', 'Series A exceeds Series B on each simulated day.\n\nThese are synthetic point values. No uncertainty estimates or scientific conclusions are implied.', { left: 544, top: 138, width: 345, height: 282 }, 22);
text(a, 'reference', 'Source: synthetic integration fixture. Values in mg/L; no real research data.', { left: 48, top: 475, width: 850, height: 32 }, 14, '#58686C');
a.speakerNotes.text = 'Synthetic test only. Preserve categories Day 1–3, Series A/B, mg/L and all six values. No research claims.';

const b = deck.slides.add();
b.background.fill = '#FFFFFF';
text(b, 'title', 'Synthetic values and process (2/2)', { left: 48, top: 36, width: 860, height: 58 }, 28, '#172B30', true);
const table = b.tables.add({ rows: 4, columns: 3, left: 48, top: 128, width: 520, height: 220,
  values: [['Day', 'Series A (mg/L)', 'Series B (mg/L)'], ['1', '12', '8'], ['2', '14', '9'], ['3', '13', '10']] });
table.cells.block({ row: 0, column: 0, rowCount: 4, columnCount: 3 }).assign({ textStyle: { fontFamily: 'Arial', fontSize: 20, color: '#172B30' } });
table.cells.block({ row: 0, column: 0, rowCount: 1, columnCount: 3 }).assign({ fill: '#DDEFF0', textStyle: { bold: true } });
text(b, 'process-input', 'Synthetic input', { left: 624, top: 151, width: 230, height: 48 }, 21);
b.shapes.add({ name: 'process-arrow', geometry: 'downArrow', position: { left: 710, top: 212, width: 36, height: 64 }, fill: '#7CBEC1', line: { fill: 'none', width: 0 } });
text(b, 'process-output', 'Tabulated values', { left: 624, top: 294, width: 240, height: 48 }, 21);
text(b, 'caveat', 'All values are simulated. Native table and diagram labels remain editable.', { left: 48, top: 405, width: 850, height: 42 }, 20);
text(b, 'reference', 'Source: synthetic integration fixture. No real research data.', { left: 48, top: 475, width: 850, height: 32 }, 14, '#58686C');
b.speakerNotes.text = 'Synthetic test only. Table values match slide 1 exactly. The arrow describes fixture data flow, not a scientific causal mechanism.';
const candidatePath = path.join(buildDir, 'authoring-draft.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidatePath);
const result = await finalizePresentation({
  workspaceDir, candidatePath, finalPath, pythonExecutable: python,
  integrityValidatorPath: path.join(presentationSkill, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(presentationSkill, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '9144000,5143500', '--require-native-table-slide', '2'],
  explicitTotalSlideCount: 2, requiredNativeTableOwnerSlides: [2], requiredNativeChartOwnerSlides: [1],
  // New synthetic chart has literal data, not a source workbook/formula lineage.
  materializeLiteralChartWorkbooks: true,
  fontPolicy: { basis: 'design', families: ['Arial'] }, verifyArtifactToolImport: true,
  receiptPath: path.join(buildDir, 'authoring-validation.json'),
});
console.log(JSON.stringify({ fixture: finalPath, status: result.status ?? 'finalized' }));
