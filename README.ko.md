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
  <a href="references/design-system.md">디자인 원칙(영문)</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">사용 안내(영문)</a>
</p>

*A palate for ideas, a palette for slides.*

**palate**는 연구 발표 자료를 다듬어 주는 Codex 스킬입니다. 복잡한 연구 내용도 듣는 사람이 흐름을 쉽게 따라갈 수 있도록 구성부터 디자인까지 함께 살펴봅니다.

**지금 만들어 둔 발표 자료를 그대로 올리면 됩니다.** 글이 많아도, 슬라이드마다 디자인이 달라도 괜찮습니다. 아직 만드는 중인 자료도 상관없습니다. 미리 정리하거나 보기 좋게 꾸며 놓을 필요는 없습니다.

**palate**는 먼저 누구를 대상으로 하는 발표인지, 무엇을 전달하고 싶은지, 발표 시간은 얼마나 되는지 확인합니다. 그에 맞춰 내용의 흐름을 다시 잡고 강조할 부분을 정한 뒤, 슬라이드마다 배치와 정보의 우선순위를 다듬어 연구의 근거와 분석, 결론이 더 명확하게 드러나도록 합니다.

학회 발표, 연구실 미팅, 강의는 필요한 설명의 깊이부터 다릅니다. 그래서 정해진 템플릿을 적용하기보다는 발표 목적과 상황에 맞게 구성합니다. 이 과정에서 **palate**는 연구 데이터를 임의로 수정하거나 결론의 본래 의미를 바꾸지 않으며, 결과 해석에 영향을 주는 가정, 적용 조건, 불확실성을 생략하지 않습니다.

작업이 끝나면 **직접 수정할 수 있는 발표 자료**와 함께, 어떤 부분을 바꾸고 확인했는지, 추가로 확인이 필요한 사항은 무엇인지 정리한 짧은 보고서를 받을 수 있습니다.

## <img src="assets/icons/square-terminal.svg" width="22" height="22" align="bottom" alt="">&nbsp; 설치하고 사용하기

### 01 | **palate** 설치하기

Codex를 열고 다음 요청을 붙여 넣으세요. Codex가 실행 환경과 필요한 도구를 확인하고 설치를 진행합니다.

```text
https://github.com/sherryyan1/palate-by-sherry 에서 Codex 스킬 palate를 설치해 주세요.

Codex가 실행되는 환경을 확인하고 docs/installation.md에 따라 설치한 뒤 $palate를 사용할 수 있는지 확인해 주세요. 이미 설치되어 있다면 교체하기 전에 물어봐 주세요.
```

### 02 | 발표 자료 올리기

지금 있는 발표 자료를 첨부하세요. 글이 많거나 디자인이 제각각이어도, 아직 만드는 중이어도 괜찮습니다.

```text
$palate 이 발표 자료를 다듬어 주세요.
```

### 03 | 발표 조건 알려주기

청중, 발표 시간, 필요한 설명의 깊이가 정해져 있다면 처음에 알려주세요. 상세한 기획서가 필요한 것은 아닙니다. **palate**는 이미 받은 정보를 활용하고, 디자인 판단에 영향을 주는 빠진 내용만 묻습니다. 설명의 깊이를 맡기면 자료와 발표 조건을 살펴보고 판단합니다. 다른 요청 방법은 [사용 안내](docs/usage.md)에서 확인할 수 있습니다.

설치 대상은 Codex가 실행되는 Windows, macOS, Linux 환경입니다. 채팅에 쓰는 기기와 Codex가 실제로 실행되는 컴퓨터나 원격 환경은 다를 수 있습니다. iOS나 iPadOS에 직접 설치하는 과정은 이 안내에 포함되지 않습니다. 추가 권한을 허용하거나 설정을 직접 바꾸거나 Codex를 재시작해야 하면 Codex가 해당 단계에서 안내합니다. 수동으로 설정하려면 [설치 안내](docs/installation.md)를 참고하세요.

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; 지원 언어

이 README는 **English, 简体中文, 日本語, 한국어**로 제공됩니다. 페이지 상단의 링크로 언어를 바꿀 수 있습니다.

번역을 요청하지 않으면 **palate**는 발표 자료의 원래 언어를 유지합니다. 번역할 때도 수치, 단위, 과학적 의미를 보존합니다. 전문 용어에 여러 번역이 가능하고 선택에 따라 과학적 의미가 달라질 수 있으면, 임의로 정하지 않고 어떤 번역을 쓸지 묻습니다.

## <img src="assets/icons/compass.svg" width="22" height="22" align="bottom" alt="">&nbsp; 디자인 원칙

### <img src="assets/icons/users-round.svg" width="22" height="22" align="top" alt="">&nbsp; 01 | 청중에서 출발하기

<sub><em>청중이 무엇을 이해해야 할까요?</em></sub>

튜토리얼에서는 원리를 단계적으로 풀어야 할 수 있고, 연구실 미팅에서는 토론에 필요한 방법과 불확실성을 보여주어야 할 수 있습니다. **palate**는 발표 상황에 맞춰 설명의 깊이를 조절합니다.

발표 시간은 설명의 **깊이와 진행 속도**를 정하는 기준입니다. 시간만으로 슬라이드 수를 정하지는 않으며, 보충 내용은 필요에 따라 발표자 노트나 부록에 둡니다.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/chart-no-axes-combined.svg" width="22" height="22" align="top" alt="">&nbsp; 02 | 근거와 논리 드러내기

<sub><em>근거와 논리의 흐름을 어떻게 더 쉽게 보여줄 수 있을까요?</em></sub>

**palate**는 정보의 중요도를 정리하고, 비교가 타당한 결과는 척도를 맞춰 보여줍니다. 방법은 논리를 따라갈 수 있는 순서로 배치하고, 결과는 이를 뒷받침하는 근거와 해석에 필요한 조건 가까이에 둡니다.

여백, 청록색 강조, 섹션과 설명의 진행을 보여주는 표시는 관계와 순서를 전달하기 위한 도구입니다. 모든 슬라이드에 똑같이 넣지는 않습니다.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/shield-check.svg" width="22" height="22" align="top" alt="">&nbsp; 03 | 연구의 과학적 의미 지키기

<sub><em>디자인을 바꾸더라도 무엇은 그대로여야 할까요?</em></sub>

**palate**는 데이터, 수치, 단위, 수식, 라벨, 범례, 불확실성, 해석상의 한계와 참고문헌을 보존합니다. 기존 객체는 도구가 지원하는 범위에서 개별 편집이 가능한 상태로 유지하고, 재구성의 정확성을 검증할 수 없는 복잡한 그림은 원형을 유지합니다.

### <img src="assets/icons/package-check.svg" width="22" height="22" align="top" alt="">&nbsp; 받을 수 있는 결과물

도구와 파일 형식이 지원하는 범위에서 새로 저장한 편집 가능한 발표 자료와 변경 내용, 완료한 검토, 남은 한계를 정리한 짧은 보고서를 받습니다. **palate**는 과학적 내용, 편집 가능 여부, 실제 화면에서의 표시를 각각 검토합니다. 꼭 필요한 검토를 마치지 못하면 남은 작업을 밝히고, 최종본 대신 추가 확인이 필요한 후보본으로 전달합니다.

## <img src="assets/icons/files.svg" width="22" height="22" align="bottom" alt="">&nbsp; 파일 형식과 실행 환경

**palate**는 PowerPoint와 Keynote에 같은 디자인 원칙을 적용합니다. 원본 형식에 따라 필요한 파일과 최종 검토를 마칠 수 있는 환경이 달라집니다.

| 원본 | 받는 파일 |
| :--- | :--- |
| PowerPoint (`.pptx`) | 원본과 대조한 새 편집 가능 `.pptx` 파일. |
| Keynote (`.key`) | 내보낸 `.pptx`와 PDF로 만든 새 편집 가능 `.pptx`. `.key`는 Mac의 Keynote에서 저장·검토를 마친 뒤 제공합니다. |

원본을 열 수 없으면 **palate**가 호환되는 편집 가능 사본을 요청합니다. 최종 발표 앱을 이용할 수 없으면 남은 검토를 안내합니다. **palate**가 Mac의 Keynote를 이용할 수 없으면 PowerPoint와 PDF 내보내기 파일을 제공하고 Mac에서 저장·검토를 마쳐 주세요.

Windows에서 **palate**는 `.pptx` 파일을 준비할 수 있지만 Keynote의 `.key` 파일을 직접 편집할 수는 없습니다. Keynote 형식으로 받으려면 Mac의 Keynote에서 저장과 최종 검토를 마쳐야 합니다. 그전까지는 `.pptx` 파일을 제공하며, **palate**는 남은 Keynote 작업을 보고서에 기록합니다. 자세한 절차는 [Keynote 작업 흐름](references/keynote-workflow.md)을 참고하세요.

포함된 스크립트를 실행하려면 Python 3.11 이상, `lxml`, Pillow가 필요합니다. 사용할 수 있는 번들 런타임이 있으면 **palate**가 이를 우선 사용합니다. 포함된 Windows용 미리보기 렌더러에는 Microsoft PowerPoint가 필요합니다. 본문 수정이나 번역, 새 슬라이드 작성, 편집 가능한 객체의 재구성에는 사용 가능한 프레젠테이션 편집 도구가 필요합니다. 해당 도구를 이용할 수 없으면 **palate**가 결과물에 어떤 제약이 있는지 설명합니다.

**palate**는 원본을 보존하고 결과물을 새 파일에 저장합니다. 파일을 처리하는 곳은 Codex 실행 환경에 따라 로컬 컴퓨터일 수도, 클라우드일 수도 있습니다. 연구 파일을 다른 서비스로 보내기 전에 **palate**가 허락을 구합니다. 이 스킬은 여러 장으로 구성된 발표 자료를 다루며 한 페이지짜리 월간 보고서는 지원 범위에 포함되지 않습니다.

## <img src="assets/icons/book-open.svg" width="22" height="22" align="bottom" alt="">&nbsp; 상세 문서

다음 문서는 영어로 제공됩니다.

- [사용법](docs/usage.md)
- [설치와 실행 환경](docs/installation.md)
- [설명을 구성하는 방식](references/communication-design.md)
- [디자인 체계](references/design-system.md)
- [Keynote 작업 흐름](references/keynote-workflow.md)
- [연구 내용 보존 원칙](references/scientific-fidelity.md)
- [변환 계획](references/transform-plan.md)
- [검증](docs/validation.md)
