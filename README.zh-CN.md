<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 640px)" srcset="docs/media/palate-dark-mobile.svg">
  <source media="(max-width: 640px)" srcset="docs/media/palate-light-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/media/palate-dark.svg">
  <img src="docs/media/palate-light.svg" alt="palate by Sherry — Good research deserves good taste." width="1200">
</picture>

<!-- language-navigation -->
<p align="center">
  <a href="README.md" lang="en">English</a> &nbsp;·&nbsp;
  <a href="README.zh-CN.md" lang="zh-CN">简体中文</a> &nbsp;·&nbsp;
  <a href="README.ja.md" lang="ja">日本語</a> &nbsp;·&nbsp;
  <a href="README.ko.md" lang="ko">한국어</a>
</p>
<!-- /language-navigation -->

<p align="center">
  <a href="#快速开始">快速开始</a> &nbsp;·&nbsp;
  <a href="references/design-system.md">设计原则（英文）</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">使用指南（英文）</a>
</p>

**palate** 是一个按 Sherry 风格优化科研演示文稿的 Codex 技能。它根据听众背景、汇报目的和可用时间，判断哪些内容需要解释、证据应如何展开，再调整幻灯片的结构与视觉层次，让听众更容易跟上研究思路。整个过程保留研究的原意，以及理解结论所需的限定条件。

A palate for ideas, a palette for slides.

## 快速开始

在仓库根目录运行以下命令，安装依赖和技能：

```powershell
python -m pip install -r requirements.txt
python scripts/package_skill.py --output dist/palate.zip --install "$env:USERPROFILE\.codex\skills\palate"
```

附上幻灯片，然后提出请求：

```text
用 palate 帮我润色这份科研汇报。
```

你也可以用 `$palate` 显式调用技能。无需先写一份完整的设计需求：palate 会沿用你已提供的信息，只补充询问会影响设计的背景。如果你希望由它决定技术细节的深度，它会先检查原稿，再结合听众和时长作出判断。你也可以一开始就说明汇报场景、听众、时间和期望深度；[使用指南（英文）](docs/usage.md)解释了这些信息如何影响设计。

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; 语言

本 README 提供 **English、简体中文、日本語和 한국어** 四个版本。你可以通过页面顶部的链接切换语言。

除非你要求翻译，否则演示文稿会保留原来的语言。

如果需要翻译，palate 会在保留数值、单位和科学含义的前提下，帮助你翻译内容。遇到有多种译法的专业术语时，palate 会向你确认，不会自行猜测。

## 如何判断一套幻灯片需要怎样的调整

设计首先考虑听众需要理解什么。教学型分享可能需要分步解释一个机制，研究组讨论则可能需要把方法、假设和不确定性放在便于核查的位置。可用时间决定这些解释能在报告中展开到什么程度，也帮助判断哪些补充材料适合放入备注或附录；时长本身不对应固定页数。

清晰的层次、青绿色强调色和证据周围的留白，用来呈现内容之间的关系。需要比较的结果采用可比的尺度，方法按清楚的顺序展开，结论与支撑它的证据及限定条件放在一起。对于较长的论证，可以在合适的位置使用章节箭头和分部标记，帮助听众掌握进度。

palate 保留数据、单位、公式、标签、图例、不确定性、限定条件和参考文献。在工具支持的范围内，现有原生对象继续保持可编辑；无法验证重建是否准确的复杂图件则予以保留。

你会收到一份另存为新文件的可编辑演示文稿，以及简要说明修改内容、已完成检查和剩余限制的报告。palate 分别核对内容、可编辑性和外观。如果有必需的检查无法完成，它会说明待完成的工作，并将文稿标为候选版本。

## 文件格式与运行要求

palate 对 PowerPoint 和 Keynote 采用相同的设计原则。原稿格式决定它需要哪些文件，以及最终检查应在哪个应用中完成。

| 原稿格式 | palate 会做什么 | 何时需要你协助 |
| :--- | :--- | :--- |
| PowerPoint | 优化兼容且可编辑的文稿，在工具支持的范围内保留对象的可编辑性，并将结果与原稿核对。 | 如果原稿无法打开，请提供兼容的可编辑副本。如果 palate 无法访问交付使用的应用，它会指导你完成余下的检查。 |
| Keynote | 设计前将导出的 PowerPoint 副本与原稿及 PDF 视觉参考比对，再优化一份新的 PowerPoint 副本，并指导最终的 Keynote 检查。 | 如果 palate 无法访问 Mac 上的 Keynote，请提供 PowerPoint 和 PDF 导出文件，并在 Mac 上完成原生格式的保存与检查。 |

在 Windows 上，palate 可以准备 PowerPoint 副本，但无法编辑原生 `.key` 文件。如果它无法访问 Mac 上的 Keynote，会指导你完成导出及最终的保存与检查，并在报告中说明尚未完成的原生 Keynote 步骤。[Keynote 工作流程（英文）](references/keynote-workflow.md)说明了具体操作，以及完成原生 Keynote 交付前必需的检查。

附带脚本需要 Python 3.11+、`lxml` 和 Pillow；如果环境已有捆绑的运行时，palate 会优先使用。使用附带的 Windows 幻灯片预览功能，需要安装 Microsoft PowerPoint。翻译或改写文字、新建幻灯片以及重建可编辑对象，需要可用的演示文稿编辑工具。缺少相应工具时，palate 会说明交付结果受到哪些限制。

原稿保持不变，输出另存为新文件。未经明确授权，研究文件不会上传，而是保留在本地；研究文件及相关任务材料不纳入版本控制。此技能面向多页演示文稿，单页月度进展汇报不在其适用范围内。

## 文档与参考

以下详细文档及运行时说明目前均为英文。

- [使用、安装与运行要求](docs/usage.md)
- [设计系统](references/design-system.md)
- [Keynote 工作流程](references/keynote-workflow.md)
- [科学内容保真](references/scientific-fidelity.md)
- [转换计划](references/transform-plan.md)
- [验证方法](docs/validation.md)
