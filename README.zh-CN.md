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
  <a href="#-开始使用">开始使用</a> &nbsp;·&nbsp;
  <a href="#-sherrys-picks">Sherry's Picks</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">使用指南（英文）</a>
</p>

*A palate for ideas, a palette for slides.*

**palate** 是一个为科研工作者打磨 PPT 的 Skill。它不止于美化版面，更着眼于梳理复杂的研究内容，让演讲者思路更清晰，也让听众更容易理解。

**从手头的材料开始就好。** 已有的 PPT、粗略的文字或提纲，甚至一篇论文，都可以直接交给 **palate**。不必先做成 PPT：既可以打磨已有 PPT，也可以把文字或论文组织成新的汇报 PPT。

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

### 02 | 提供现有材料

可以上传 PPT 或论文，也可以直接粘贴文字、提纲和零散想法。在 Codex 中按手头的材料提出请求：

| 现有材料 | 请求示例 |
| :--- | :--- |
| 已有 PPT | `$palate 帮我打磨这份汇报 PPT。` |
| 文字、笔记或提纲 | `$palate 根据这些笔记制作汇报 PPT。` |
| 论文或手稿 | `$palate 根据这篇论文制作科研汇报 PPT。` |


如使用网页版 ChatGPT Work，输入 `@` 并从菜单中选中已安装的 **palate**，再附上材料并发送相应请求即可。

### 03 | 让 **palate** 了解你的汇报需求

提出请求后，**palate** 会了解以下四方面信息：

- **汇报场景：** 是组会、教学分享(tutorial)，还是对外汇报？
- **时长：** 预计讲多少分钟？
- **屏幕比例：** 汇报现场的屏幕更接近 4:3 还是 16:9？如不确定，palate会保留PPT原比例，或默认按 16:9 设计新PPT。
- **技术细节：** 希望保留多少技术细节？拿不准时，可以交给 **palate** 判断。

以上信息既可以单选，也可以用自己的话直接回答。新建 PPT 时，若尚未指定输出 PowerPoint 还是 Keynote，**palate** 也会一并确认。

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; 语言

本 README 提供 **English、简体中文、日本語和 한국어** 四个版本，可通过页面顶部的链接切换。

没有翻译要求时，已有 PPT 会保留原来的语言；新建 PPT 则按已说明的语言或源材料的语言制作，意图不明确时会先确认。翻译时，**palate** 会保留数值、单位和科学含义。

如果专业术语的几种合理译法可能实质改变科学含义，**palate** 会先向你确认，再应用译法。

## <img src="assets/icons/compass.svg" width="22" height="22" align="bottom" alt="">&nbsp; Sherry's Picks

面对"**cherry-pick**"的演讲者，听时保持审慎；用上 **Sherry's Picks**，讲时更有底气。

研究证据不挑着讲，呈现方式却可以用心选。**palate** 从整体到细节，按以下四个阶段打磨 PPT。

### <img src="assets/icons/users-round.svg" width="22" height="22" align="top" alt="">&nbsp; 01 | 知人察境

<sub><em>先辨听众，再定讲法。</em></sub>

做汇报和说话一样，先要看看对面坐着谁。同行听得懂的三言两语，换个场合，也许就得从头讲起。若只顾把自己知道的都摆出来，难免成了自说自话。

听众是谁？对研究已有多少了解？这场汇报最希望他们记住什么？

**palate** 会结合听众、目的和场合，确定整体的表达方式与视觉方向。学术会议、组会和公众讲座各有侧重，设计也应随之调整。

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/git-branch.svg" width="22" height="22" align="top" alt="">&nbsp; 02 | 顺理成章

<sub><em>让论述有起承，让结论有来处。</em></sub>

几页各自精彩的幻灯片，未必能构成一场好汇报。观点之间需要联系，推理也需要有自然的展开顺序。

**palate** 会通看整套 PPT，找出贯穿其中的核心论点，再审视内容结构。必要时调整页序、重组章节，或改变引入观点的方式，让每一部分在整场汇报中都有清楚的位置。

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/align-left.svg" width="22" height="22" align="top" alt="">&nbsp; 03 | 凝练文字

<sub><em>把复杂的研究讲明白。</em></sub>

PPT 不是论文的缩印本。满页的文字看似周全，听众若忙着低头细读，便无暇抬头听讲。

**palate** 会逐页梳理**文字**，删去重复的表述，调整信息密度，让每页要传达的重点更清楚。

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/palette.svg" width="22" height="22" align="top" alt="">&nbsp; 04 | 细琢形色

<sub><em>形式有章法，美感有分寸。</em></sub>

最后，**palate** 会细看**图表、字体、对齐、留白与配色**。

需要重新配色时，**palate** 会参考精选配色库，根据内容和图表需要表达的区别选择颜色，同时保留原有科研图中的颜色含义。详见[配色指南（英文）](references/refine-the-visuals.md#give-color-a-consistent-purpose)。

图形用来传达信息，统一的格式则让整套 PPT 保持连贯。在此基础上，再按每页的内容调整布局与呈现，让整体协调、细节妥帖，而不显得千篇一律。

## <img src="assets/icons/files.svg" width="22" height="22" align="bottom" alt="">&nbsp; 文件格式与运行要求

**palate** 共用一套设计标准，PowerPoint 和 Keynote 分别走各自的原生流程。修改已有 PPT 时，除非指定其他交付格式，否则保留原稿格式；Keynote 原稿无需经过 PowerPoint。

| 原稿 | **palate** 会提供什么 |
| :--- | :--- |
| PowerPoint（`.pptx`） | 一份新的可编辑 `.pptx`，在 PowerPoint 中完成最终检查。 |
| Keynote（`.key`） | 在 Mac 的 Keynote 中，通过当前支持的操作制作新的原生 `.key` 候选稿。 |
| 文字、笔记、提纲、论文或手稿 | 使用可用的原生制作工具，按约定应用制作新的汇报 PPT。 |

从文字或论文新建 PPT，需要能在约定应用中制作页面的工具，附带的保留式编辑工具本身不能完成这一过程。工具不可用时，**palate** 可以先整理结构与逐页内容，并注明文件制作尚未完成。

已有 PPT 无法打开时，**palate** 会请求兼容的可编辑副本。Keynote 处理需要允许所需的 Mac 自动化访问。如果交付使用的应用不可用，**palate** 会将该应用内的工作保留为待完成状态，并说明交接方式和尚需完成的检查。

Python 工具需要 Python 3.11+；`.pptx` 检查使用 `lxml`，图片分辨率诊断使用 Pillow。有可用的捆绑运行时时，会优先使用。附带的 Windows PowerPoint 渲染器只是特定平台的一种预览方式，Keynote 和其他 PowerPoint 环境无需强制使用。**palate** 会在实际交付使用的应用中检查结果，并说明缺少的工具或尚未完成的检查。安装 Skill 不会同时安装 PowerPoint 或 Keynote，也不代表已获得应用访问权限。

安装针对实际处理文件的运行环境，这可能不是聊天时使用的设备。网页版不会自动获得本地 PowerPoint 或 Keynote 的访问权限；缺少必需的原生检查时，修改后的文件仍会标为候选稿。[安装指南（英文）](docs/installation.md)和[ChatGPT Work 指南（英文）](docs/chatgpt-work.md)分别说明了设置方法与验证步骤。


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
