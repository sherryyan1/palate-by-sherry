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
  <a href="#설치하고-사용하기">설치하고 사용하기</a> &nbsp;·&nbsp;
  <a href="#-sherrys-picks">Sherry's Picks</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">사용 안내(영문)</a>
</p>

*A palate for ideas, a palette for slides.*

**palate**는 연구 발표 자료를 다듬어 주는 스킬입니다. 복잡한 연구 내용도 듣는 사람이 흐름을 쉽게 따라갈 수 있도록 구성부터 디자인까지 함께 살펴봅니다.

**지금 만들어 둔 발표 자료를 그대로 올리면 됩니다.** 글이 많아도, 슬라이드마다 디자인이 달라도 괜찮습니다. 아직 만드는 중인 자료도 상관없습니다. 미리 정리하거나 보기 좋게 꾸며 놓을 필요는 없습니다.

**palate**는 먼저 누구를 대상으로 하는 발표인지, 무엇을 전달하고 싶은지, 발표 시간은 얼마나 되는지 확인합니다. 그에 맞춰 내용의 흐름을 다시 잡고 강조할 부분을 정한 뒤, 슬라이드마다 배치와 정보의 우선순위를 다듬어 연구의 근거와 분석, 결론이 더 명확하게 드러나도록 합니다.

학회 발표, 연구실 미팅, 강의는 필요한 설명의 깊이부터 다릅니다. 그래서 정해진 템플릿을 적용하기보다는 발표 목적과 상황에 맞게 구성합니다. 이 과정에서 **palate**는 연구 데이터를 임의로 수정하거나 결론의 본래 의미를 바꾸지 않으며, 결과 해석에 영향을 주는 가정, 적용 조건, 불확실성을 생략하지 않습니다.

작업이 끝나면 **직접 수정할 수 있는 발표 자료**와 함께, 어떤 부분을 바꾸고 확인했는지, 추가로 확인이 필요한 사항은 무엇인지 정리한 짧은 보고서를 받을 수 있습니다.

## <img src="assets/icons/square-terminal.svg" width="22" height="22" align="bottom" alt="">&nbsp; 설치하고 사용하기

### 01 | **palate** 설치하기

사용할 환경에 맞게 설정하세요.

| 사용 환경 | 설정 방법 |
| :--- | :--- |
| Codex | 아래 요청으로 스킬을 설치합니다. |
| ChatGPT Work(웹) | [별도 안내](docs/chatgpt-work.md)에 따라 비공개 플러그인을 만듭니다. **실험 단계입니다. 브라우저에서 설치하는 과정과 발표 자료를 처음부터 끝까지 편집하는 과정은 모두 테스트하지 않았습니다.** |

Codex를 열고 다음 요청을 붙여 넣으세요. Codex가 실행 환경과 필요한 도구를 확인하고 설치를 진행합니다.

```text
https://github.com/sherryyan1/palate-by-sherry 에서 Codex 스킬 palate를 설치해 주세요.

Codex가 실행되는 환경을 확인하고 docs/installation.md에 따라 설치한 뒤 $palate를 사용할 수 있는지 확인해 주세요. 이미 설치되어 있다면 교체하기 전에 물어봐 주세요.
```

ChatGPT Work(웹)에서는 [별도 안내](docs/chatgpt-work.md)에 따라 사용 가능한 Plugin Creator에서 이 저장소를 바탕으로 비공개 **palate** 플러그인을 만듭니다. 사용할 수 있는 기능은 계정과 워크스페이스에 따라 다릅니다. `@` 선택 목록에서 **palate**를 선택할 수 있고 실행에 필요한 파일 전체를 읽을 수 있는지 확인하기 전까지는 설정을 보류하며, 완료하지 못한 내용을 안내합니다. 로컬 Codex에 설치한 스킬은 자동으로 동기화되지 않습니다.

### 02 | 발표 자료 올리기

지금 있는 발표 자료를 첨부하세요. 글이 많거나 디자인이 제각각이어도, 아직 만드는 중이어도 괜찮습니다.

**Codex:** 다음과 같이 요청하세요.

```text
$palate 이 발표 자료를 다듬어 주세요.
```

**ChatGPT Work(웹):** 입력창에 `@`를 입력하고 목록에서 **palate**를 선택한 뒤 요청하세요. `@palate`라는 글자만 입력하면 플러그인이 선택되지 않습니다.

```text
이 발표 자료를 다듬어 주세요.
```

### 03 | **palate**에 발표 계획 알려주기

요청을 보내면 **palate**가 어떤 발표를 준비하는지 묻습니다.

- **발표 상황:** 연구실 미팅, 튜토리얼, 외부 발표 중 어떤 자리에서 발표하나요?
- **발표 시간:** 발표 시간은 몇 분인가요?
- **설명의 깊이:** 기술적인 내용은 얼마나 자세히 설명할까요? **palate**에 맡겨도 됩니다.

제시된 선택지에서 고르거나 자유롭게 답해 주세요. 이미 알려주신 내용은 다시 묻지 않습니다.

Codex 스킬의 설치 대상은 Codex가 실행되는 Windows, macOS, Linux 환경입니다. 채팅에 쓰는 기기와 Codex가 실제로 실행되는 컴퓨터나 원격 환경은 다를 수 있습니다. iOS나 iPadOS에 직접 설치하는 과정은 이 안내에 포함되지 않습니다. 추가 권한을 허용하거나 설정을 직접 바꾸거나 Codex를 재시작해야 하면 Codex가 해당 단계에서 안내합니다. 수동으로 설정하려면 [설치 안내](docs/installation.md)를 참고하세요.

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; 지원 언어

이 README는 **English, 简体中文, 日本語, 한국어**로 제공됩니다. 페이지 상단의 링크로 언어를 바꿀 수 있습니다.

번역을 요청하지 않으면 **palate**는 발표 자료의 원래 언어를 유지합니다. 번역할 때도 수치, 단위, 과학적 의미를 보존합니다. 전문 용어에 여러 번역이 가능하고 선택에 따라 과학적 의미가 달라질 수 있으면, 임의로 정하지 않고 어떤 번역을 쓸지 묻습니다.

## <img src="assets/icons/compass.svg" width="22" height="22" align="bottom" alt="">&nbsp; Sherry's Picks

유리한 근거만 골라 제시하는 발표라면 비판적으로 들어야 합니다. 발표를 준비할 때는 **Sherry's Picks**로 구성과 표현을 다듬고 자신 있게 전달하세요.

**Sherry's Picks**는 어떤 근거를 보여줄지 골라내는 일이 아니라, 그 근거를 어떻게 전달할지 신중하게 결정하는 일입니다. **palate**는 네 가지 원칙에 따라 발표 자료의 큰 틀부터 세부 요소까지 다듬습니다.

### <img src="assets/icons/users-round.svg" width="22" height="22" align="top" alt="">&nbsp; 01 | 청중과 상황에 맞추기

<sub><em>누가 듣는 발표인지 먼저 생각합니다.</em></sub>

좋은 디자인은 발표가 이루어지는 상황을 이해하는 데서 시작합니다. 누가 듣는지, 청중이 이미 무엇을 알고 있는지, 발표가 끝난 뒤 무엇을 이해하고 기억해야 하는지 살펴봅니다.

**palate**는 청중과 목적, 발표 환경에 맞춰 전체적인 디자인 방향을 정합니다. 학회 발표와 연구실 미팅, 대중 강연은 어울리는 방식이 서로 다릅니다. 모든 발표에 통하는 하나의 디자인은 없습니다.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/git-branch.svg" width="22" height="22" align="top" alt="">&nbsp; 02 | 이야기의 흐름 잡기

<sub><em>논리를 자연스럽게 따라갈 수 있도록 구성합니다.</em></sub>

잘 만든 슬라이드를 모은다고 발표 자료가 저절로 좋아지지는 않습니다. 내용이 서로 이어지고 논리가 자연스럽게 전개되어야 합니다.

**palate**는 발표 자료 전체를 살펴 핵심 논지를 파악하고 구성을 다시 검토합니다. 필요하면 슬라이드 순서를 바꾸고 섹션을 재구성하거나 개념을 소개하는 방식을 조정해 전체 흐름 속에서 각 부분의 역할이 분명하도록 합니다.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/align-left.svg" width="22" height="22" align="top" alt="">&nbsp; 03 | 핵심이 드러나게 다듬기

<sub><em>복잡한 내용도 명료하게 전달합니다.</em></sub>

무엇을 남기고 무엇을 풀어 설명하며 어디를 더 쉽게 표현할지 판단해야 메시지가 명확해집니다.

**palate**는 슬라이드를 한 장씩 살피며 빽빽한 글을 다듬고 중복을 줄여 핵심이 잘 드러나도록 합니다. 복잡한 연구를 쉽게 풀어 쓰면서도 과학적 정확성을 유지하고 의미의 미묘한 차이나 중요한 불확실성이 사라지지 않도록 합니다.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/palette.svg" width="22" height="22" align="top" alt="">&nbsp; 04 | 시각적 완성도 높이기

<sub><em>작은 요소도 전달하려는 내용에 맞춥니다.</em></sub>

마지막으로 **palate**는 그림, 서체, 정렬, 간격, 색상 등 시각적 요소를 다듬습니다.

그림은 장식에 그치지 않고 내용을 전달해야 합니다. 서식을 일관되게 맞춰 슬라이드 전체에 통일감을 주되, 각 슬라이드의 내용에 따라 배치와 표현에 변화를 줍니다. 그 결과, 고정된 템플릿에 맞춘 듯한 인상 없이도 전체가 자연스럽게 어우러지는, 완성도 높고 전문적인 발표 자료가 됩니다.

## <img src="assets/icons/files.svg" width="22" height="22" align="bottom" alt="">&nbsp; 파일 형식과 실행 환경

**palate**는 하나의 디자인 기준을 사용하되, PowerPoint와 Keynote는 각각 해당 앱에서 편집하고 검토합니다. 다른 결과물 형식을 요청하지 않으면 원본 형식을 유지합니다. Keynote 발표 자료를 PowerPoint로 변환할 필요는 없습니다.

| 원본 | 받는 파일 |
| :--- | :--- |
| PowerPoint (`.pptx`) | 새 편집 가능 `.pptx` 파일. 최종 검토는 PowerPoint에서 진행합니다. |
| Keynote (`.key`) | Mac의 Keynote에서 지원하는 작업을 적용한 새 네이티브 `.key` 후보본. |

원본을 열 수 없으면 **palate**가 호환되는 편집 가능 사본을 요청합니다. Keynote 작업에는 현재 실행 중인 에이전트가 앱을 제어할 수 있도록 Mac의 자동화 권한을 허용해야 합니다. 결과물을 사용할 앱에 접근할 수 없으면 해당 작업과 검토를 미완료로 기록하고, 이어서 진행할 방법을 안내합니다.

포함된 Keynote 네이티브 작업 흐름은 **실험 단계이며, 아직 Mac에서 직접 테스트하지 않았습니다**. macOS와 Keynote가 필요하며, 자동 편집은 기존 텍스트 상자와 도형의 배치 및 글자 스타일에 한정됩니다. 그 밖의 변경에는 사용 가능한 네이티브 편집 도구가 필요하며, 도구가 없으면 해당 변경은 보류합니다. 지원 범위와 검토 항목은 [Keynote 작업 흐름](references/keynote-workflow.md)을 참고하세요. 다른 형식의 결과물을 요청하거나 변환 방식을 선택한 경우에만 파일을 변환하고, 변환 과정에서 생긴 차이도 별도로 확인합니다.

Python 도구에는 Python 3.11 이상이 필요합니다. `.pptx` 검사에는 `lxml`, 이미지 해상도 진단에는 Pillow를 사용하며, 사용 가능한 번들 런타임을 우선합니다. 포함된 Windows PowerPoint 렌더러는 해당 환경에서 쓸 수 있는 미리보기 도구 중 하나입니다. Keynote나 다른 PowerPoint 환경에서 반드시 거칠 필요는 없습니다. 최종 검토는 결과물을 실제로 사용할 앱에서 진행합니다. 스킬을 설치해도 앱이 함께 설치되거나 앱 접근 권한이 주어지지는 않습니다.

ChatGPT Work(웹)에서 사용해도 로컬 앱을 자동으로 제어할 수 있게 되는 것은 아닙니다. 결과물을 사용할 앱에서 검토할 수 없으면 미완료 검토 항목을 밝히고 후보본으로 전달합니다.

**palate**는 원본을 보존하고 결과물을 새 파일에 저장합니다. 파일을 처리하는 곳은 사용 중인 실행 환경에 따라 로컬 컴퓨터일 수도, 클라우드일 수도 있습니다. ChatGPT에 올린 파일은 선택한 워크스페이스에서 처리됩니다. 연구 파일을 다른 서비스로 보내기 전에 **palate**가 허락을 구합니다. 이 스킬은 여러 장으로 구성된 발표 자료를 다루며 한 페이지짜리 월간 보고서는 지원 범위에 포함되지 않습니다.

## <img src="assets/icons/book-open.svg" width="22" height="22" align="bottom" alt="">&nbsp; 상세 문서

다음 문서는 영어로 제공됩니다.

- [사용법](docs/usage.md)
- [설치와 실행 환경](docs/installation.md)
- [ChatGPT Work(웹) 설정과 사용법](docs/chatgpt-work.md)
- [설명을 구성하는 방식](references/communication-design.md)
- [디자인 체계](references/design-system.md)
- [Keynote 작업 흐름](references/keynote-workflow.md)
- [연구 내용 보존 원칙](references/scientific-fidelity.md)
- [변환 계획](references/transform-plan.md)
- [검증](docs/validation.md)
