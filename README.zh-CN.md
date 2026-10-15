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

## README、对话与幻灯片的语言

这三种语言可以分别选择。阅读某个语言版本的 README，不会自动改变对话或幻灯片的语言。例如，你可以阅读韩文 README、用韩语沟通，同时要求输出英文幻灯片。阅读中文版也不意味着原稿会自动翻译成中文；没有明确的翻译要求时，保留原稿语言。

如果需要改写或翻译幻灯片文字，请在请求中说明。这类内容变更需要使用原生演示文稿创作工具，并核对科学含义、术语、数值、单位、限定条件和引用。用于保留现有对象的辅助脚本负责位置与样式调整，不承担翻译。

## 如何判断一套幻灯片需要怎样的调整

设计首先考虑听众需要理解什么。教学型分享可能需要分步解释一个机制，研究组讨论则可能需要把方法、假设和不确定性放在便于核查的位置。可用时间决定这些解释能在报告中展开到什么程度，也帮助判断哪些补充材料适合放入备注或附录；时长本身不对应固定页数。

清晰的层次、青绿色强调色和证据周围的留白，用来呈现内容之间的关系。需要比较的结果采用可比的尺度，方法按清楚的顺序展开，结论与支撑它的证据及限定条件放在一起。对于较长的论证，可以在合适的位置使用章节箭头和分部标记，帮助听众掌握进度。

palate 保留数据、单位、公式、标签、图例、不确定性、限定条件和参考文献。在工具支持的范围内，现有原生对象继续保持可编辑；无法验证重建是否准确的复杂图件则予以保留。交付结果包括一份新保存的可编辑演示文稿，以及简要说明修改内容、已完成检查和剩余限制的报告。内容准确性、可编辑性和最终渲染效果分别核验。

## 文件格式与运行要求

PowerPoint 和 Keynote 共用设计原则，但文件准备和最终检查的要求不同。

| 原稿格式 | 设计前的准备 | 最终检查 |
| :--- | :--- | :--- |
| PowerPoint | 检查兼容且可编辑的演示文稿；保留现有原生对象，较大的改动使用原生创作工具完成。 | 在实际交付使用的应用中检查内容、外观和可编辑性。 |
| Keynote | 导出 PowerPoint 副本和 PDF 视觉参考，先与原稿比对，再开始设计。 | 在 Keynote 中打开并另存结果，检查转换、字体和原生对象的可编辑性；若含动画、转场或音视频，还需检查播放。 |

[Keynote 工作流程（英文）](references/keynote-workflow.md)说明了导出设置和转换检查。Windows 可以准备和修改用于交换的 PowerPoint 文件；原生 Keynote 成品需要在 Mac 的 Keynote 中保存并完成检查。只有这些步骤实际完成后，才能视为完成原生 Keynote 交付；否则，报告中会将相应工作标为待完成。

附带脚本需要 Python 3.11+、`lxml` 和 Pillow。如果环境已有捆绑的运行时，应优先使用。附带的 Windows 预览渲染脚本需要 Microsoft PowerPoint；新建或重建幻灯片则需要可用的原生演示文稿创作工具。

原稿保持不变，输出另存为新文件。未经明确授权，研究文件不会上传，而是保留在本地；研究文件及相关任务材料不纳入版本控制。此技能面向多页演示文稿，单页月度进展汇报不在其适用范围内。

## 文档与参考

以下详细文档及运行时说明目前均为英文。

- [使用、安装与运行要求](docs/usage.md)
- [设计系统](references/design-system.md)
- [Keynote 工作流程](references/keynote-workflow.md)
- [科学内容保真](references/scientific-fidelity.md)
- [转换计划](references/transform-plan.md)
- [验证方法](docs/validation.md)
