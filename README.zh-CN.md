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
  <a href="#开始使用">开始使用</a> &nbsp;·&nbsp;
  <a href="#-sherrys-picks">Sherry's Picks</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">使用指南（英文）</a>
</p>

*A palate for ideas, a palette for slides.*

**palate** 是一个为科研工作者打磨 PPT 的 Skill。它不止于美化版面，更着眼于梳理复杂的研究内容，让演讲者思路更清晰，也让听众更容易理解。

**把现有的 PPT 直接交给palate即可。** 哪怕内容繁杂、排版凌乱，甚至还没做完，都可以直接上传。

**palate** 会先了解汇报面向谁、希望讲清什么，以及有多少时间，再据此安排内容的详略与先后。学术会议、组会和大众演讲各有侧重，设计自然不必拘于一式。

**palate** 不会擅自改动数据或改变结论原意，也不会为了精简页面，略去影响结果解读的假设、适用条件与不确定性。

完成后，**palate** 会提供一份**可继续编辑的 PPT**，并附上简短的修改说明，交代主要改动、完成的检查，以及尚待确认的地方。

## <img src="assets/icons/square-terminal.svg" width="22" height="22" align="bottom" alt="">&nbsp; 开始使用

### 01 | 安装 **palate**

先选择使用环境。两种入口共用同一套设计规则。

| 使用环境 | 如何开始 |
| :--- | :--- |
| Codex | 使用下方的安装请求。 |
| 网页版 ChatGPT Work | 按照[私有插件设置指南（英文）](docs/chatgpt-work.md)操作。此入口仍处于实验阶段，尚未实测网页版安装和完整的 PPT 处理流程。 |

使用 Codex 时，粘贴以下请求：

```text
请从 https://github.com/sherryyan1/palate-by-sherry 安装 palate Codex Skill。

检查 Codex 实际运行的环境，按照仓库中的 docs/installation.md 完成安装，并确认可以调用 $palate。如果已安装 palate，请先询问我是否替换。
```

Codex 会根据当前环境安装 **palate**，并检查是否可以正常使用。如需额外设置，会给出相应提示。[安装指南（英文）](docs/installation.md)提供了具体操作。

网页版通过 Plugin Creator 设置私有插件，能否使用取决于账号和工作区权限。只有在 `@` 菜单中能选到 **palate**，并确认它可以读取完整的运行文件后，才算安装完成。本地 Codex 中已安装的 Skill 不会自动同步过去。

### 02 | 上传 PPT

直接附上现有的 PPT。文字太多、排版不统一或尚未完成，都可以从这里开始。在 Codex 中提出请求：

```text
$palate 帮我打磨这份汇报 PPT。
```

使用网页版 ChatGPT Work 时，输入 `@` 并从菜单中选中已安装的 **palate**，再发送「帮我打磨这份汇报 PPT」。

### 03 | 让 **palate** 了解你的汇报需求

提出请求后，**palate** 会了解以下三方面信息：

- **汇报场景：** 是组会、教学分享，还是对外汇报？
- **时长：** 预计讲多少分钟？
- **技术细节：** 希望保留多少技术细节？也可以交给 **palate** 判断。

可以选择建议选项，也可以用自己的话回答。已经说明的信息，**palate** 不会重复询问。

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; 语言

本 README 提供 **English、简体中文、日本語和 한국어** 四个版本，可通过页面顶部的链接切换。

没有翻译要求时，**palate** 会保留 PPT 原来的语言。翻译时，它会保留数值、单位和科学含义。

如果专业术语的几种合理译法可能实质改变科学含义，**palate** 会先向你确认，再应用译法。

## <img src="assets/icons/compass.svg" width="22" height="22" align="bottom" alt="">&nbsp; Sherry's Picks

面对"**cherry-pick**"的演讲者，听时保持审慎；用上 **Sherry's Picks**，讲时更有底气。

研究证据不挑着讲，呈现方式却可以用心选。**palate** 从整体到细节，按以下四个阶段打磨 PPT。

### <img src="assets/icons/users-round.svg" width="22" height="22" align="top" alt="">&nbsp; 01 | 知人察境

<sub><em>从听众的理解出发。</em></sub>

设计先从汇报场合开始。听众是谁？对研究已有多少了解？这场汇报最希望他们记住什么？

**palate** 会结合听众、目的和场合，确定整体的表达方式与视觉方向。学术会议、组会和公众讲座各有侧重，设计也应随之调整。

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/git-branch.svg" width="22" height="22" align="top" alt="">&nbsp; 02 | 理清脉络

<sub><em>让听众跟得上论述。</em></sub>

几页各自精彩的幻灯片，未必能构成一场好汇报。观点之间需要联系，推理也需要有自然的展开顺序。

**palate** 会通看整套 PPT，找出贯穿其中的核心论点，再审视内容结构。必要时调整页序、重组章节，或改变引入观点的方式，让每一部分在整场汇报中都有清楚的位置。

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/align-left.svg" width="22" height="22" align="top" alt="">&nbsp; 03 | 提炼要义

<sub><em>把复杂的研究讲明白。</em></sub>

清楚的表达，来自对内容的判断：哪些信息必须留下，哪些需要解释，哪些可以说得更直接。

**palate** 会逐页梳理文字，删去重复，调整信息密度，让每页要传达的重点更清楚。精简是为了让复杂研究更容易理解，同时保留必要的科学细节、限定条件和不确定性。

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/palette.svg" width="22" height="22" align="top" alt="">&nbsp; 04 | 细琢形色

<sub><em>每一处细节，都要有用意。</em></sub>

最后，**palate** 会细看图表、字体、对齐、留白与配色。

图形用来传达信息，统一的格式则让整套 PPT 保持连贯。在此基础上，再按每页的内容调整布局与呈现，让整体协调、细节妥帖，而不显得千篇一律。

## <img src="assets/icons/files.svg" width="22" height="22" align="bottom" alt="">&nbsp; 文件格式与运行要求

**palate** 共用一套设计标准，PowerPoint 和 Keynote 分别走各自的原生流程。未指定其他交付格式时，保留原稿格式；Keynote 原稿无需经过 PowerPoint。

| 原稿 | **palate** 会提供什么 |
| :--- | :--- |
| PowerPoint（`.pptx`） | 一份新的可编辑 `.pptx`，在 PowerPoint 中完成最终检查。 |
| Keynote（`.key`） | 在 Mac 的 Keynote 中，通过当前支持的操作制作新的原生 `.key` 候选稿。 |

原稿无法打开时，**palate** 会请求兼容的可编辑副本。Keynote 处理需要允许所需的 Mac 自动化访问。如果交付使用的应用不可用，**palate** 会将该应用内的工作保留为待完成状态，并说明交接方式和尚需完成的检查。

附带的 Keynote 原生流程目前为**实验性功能，尚未在 Mac 上实测**，需要 macOS、Keynote，以及允许实际执行任务的进程控制该应用的权限。自动编辑仅覆盖现有文本框和形状的位置、文字样式；其他修改需要可用的原生编辑方式，否则保持待完成状态。[Keynote 指南（英文）](references/keynote-workflow.md)列出了操作范围和检查要求。只有明确选择转换方案或要求其他交付格式时，才会采用格式转换，并单独核对转换损失。

Python 工具需要 Python 3.11+；`.pptx` 检查使用 `lxml`，图片分辨率诊断使用 Pillow。有可用的捆绑运行时时，会优先使用。附带的 Windows PowerPoint 渲染器只是特定平台的一种预览方式，Keynote 和其他 PowerPoint 环境无需强制使用。**palate** 会在实际交付使用的应用中检查结果，并说明缺少的工具或尚未完成的检查。安装 Skill 不会同时安装 PowerPoint 或 Keynote，也不代表已获得应用访问权限。

安装针对实际处理文件的运行环境，这可能不是聊天时使用的设备。网页版不会自动获得本地 PowerPoint 或 Keynote 的访问权限；缺少必需的原生检查时，修改后的文件仍会标为候选稿。[安装指南（英文）](docs/installation.md)和[ChatGPT Work 指南（英文）](docs/chatgpt-work.md)分别说明了设置方法与验证步骤。

文件保存和处理的位置由所选运行环境决定，上传到 ChatGPT 的文件会在所选工作区中处理。**palate** 保留原稿，将修改结果另存为新文件；向其他服务发送研究文件前会先询问。此 Skill 面向多页汇报 PPT，单页月度进展汇报不在适用范围内。

## <img src="assets/icons/book-open.svg" width="22" height="22" align="bottom" alt="">&nbsp; 文档与参考

以下文档均为英文。

- [安装与环境检查](docs/installation.md)
- [网页版 ChatGPT Work 设置，实验阶段](docs/chatgpt-work.md)
- [使用方法与汇报需求](docs/usage.md)
- [沟通设计](references/communication-design.md)
- [设计系统](references/design-system.md)
- [Keynote 工作流程](references/keynote-workflow.md)
- [科学保真](references/scientific-fidelity.md)
- [变换计划](references/transform-plan.md)
- [验证](docs/validation.md)
