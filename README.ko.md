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
  <a href="#빠른-시작">시작하기</a> &nbsp;·&nbsp;
  <a href="references/design-system.md">디자인 원칙(영문)</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">사용 안내(영문)</a>
</p>

**palate**는 Sherry의 스타일로 연구 발표 자료를 다듬는 Codex 스킬입니다. 청중과 발표 목적, 주어진 시간에 맞춰 설명의 흐름을 잡고 근거와 논리를 따라가기 쉽게 슬라이드를 구성합니다. 이 과정에서 연구의 의미와 해석에 필요한 조건을 보존합니다.

A palate for ideas, a palette for slides.

## 빠른 시작

저장소의 루트 디렉터리에서 필요한 패키지와 스킬을 설치합니다.

```powershell
python -m pip install -r requirements.txt
python scripts/package_skill.py --output dist/palate.zip --install "$env:USERPROFILE\.codex\skills\palate"
```

슬라이드를 첨부하고 다음과 같이 요청합니다.

```text
palate로 이 슬라이드를 다듬어 주세요.
```

발표 조건을 처음부터 알려주어도 되고 이 한 문장으로 시작해도 됩니다. palate는 이미 제공한 정보를 활용하고 디자인 결정에 필요한 내용만 추가로 묻습니다. 설명의 깊이를 맡기면 먼저 슬라이드를 살펴본 뒤 발표에 필요한 설명 수준을 정합니다. 스킬을 명시적으로 호출하려면 `$palate`를 사용할 수 있습니다. 어떤 정보가 발표 방향을 결정하는지는 [사용 안내](docs/usage.md)에서 확인할 수 있습니다.

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; 지원 언어

이 README는 **English, 简体中文, 日本語, 한국어**로 제공됩니다. 페이지 상단의 링크로 언어를 바꿀 수 있습니다.

번역을 요청하지 않으면 발표 자료는 원문의 언어를 유지합니다.

번역을 요청하면 palate가 수치, 단위와 과학적 의미를 보존하면서 내용의 번역을 돕습니다. 전문 용어를 여러 방식으로 번역할 수 있으면 임의로 정하지 않고 사용자에게 확인합니다.

## 슬라이드를 다듬는 방식

디자인은 청중이 무엇을 이해해야 하는지에서 출발합니다. 튜토리얼에서는 작동 원리를 단계적으로 풀어야 할 수 있고 연구 회의에서는 토론할 수 있도록 방법과 불확실성을 함께 보여주어야 할 수 있습니다. 발표 시간은 현장에서 어디까지 설명할지, 어떤 보충 자료를 발표자 노트나 부록에 둘지 판단하는 기준입니다. 시간만으로 슬라이드 수를 정하지는 않습니다.

명확한 시각적 위계, 청록색 강조, 근거 주변의 여백과 간격으로 정보의 관계를 드러냅니다. 결과를 비교할 때는 비교 가능한 척도를 사용하고 방법은 순서가 보이도록 구성합니다. 결과를 뒷받침하는 근거와 해석에 필요한 조건은 해당 결과 가까이에 둡니다. 긴 설명에서는 내용에 맞는 섹션 안내 화살표와 개념별 진행 표시로 청중이 현재 위치를 파악하도록 돕습니다.

palate는 데이터, 수치, 단위, 수식, 라벨, 범례, 불확실성, 해석상의 한계와 참고문헌을 보존합니다. 기존 객체는 도구가 지원하는 범위에서 개별 편집이 가능한 상태로 유지하고 재구성의 정확성을 검증할 수 없는 복잡한 그림은 원형을 유지합니다. 새 파일로 저장한 편집 가능한 발표 자료와 변경 내용, 확인 결과, 남은 한계를 담은 간결한 보고서를 받을 수 있습니다. palate는 내용이 보존되었는지, 객체를 편집할 수 있는지, 실제 화면에서 어떻게 보이는지를 각각 검토합니다. 필요한 검토를 완료할 수 없으면 남은 작업을 보고서에 밝히고 발표 자료에 후보본임을 표시합니다.

## 파일 형식과 실행 환경

palate는 PowerPoint와 Keynote에 같은 디자인 원칙을 적용합니다. 원본 형식에 따라 필요한 파일과 최종 검토를 마칠 수 있는 환경이 달라집니다.

| 원본 | palate가 하는 일 | 사용자 도움이 필요한 경우 |
| :--- | :--- | :--- |
| PowerPoint | 호환되는 편집 가능 파일을 다듬고 도구가 지원하는 범위에서 객체를 편집 가능한 상태로 유지합니다. 결과물을 원본과 대조합니다. | 원본을 열 수 없으면 palate가 호환되는 편집 가능 사본을 요청합니다. 최종 발표에 사용할 애플리케이션을 palate가 이용할 수 없으면 사용자가 남은 검토를 진행하도록 안내합니다. |
| Keynote | 디자인을 바꾸기 전에 PowerPoint로 내보낸 파일을 원본 및 화면 비교용 PDF와 대조합니다. 이어서 새 PowerPoint 사본을 다듬고 Keynote에서의 최종 검토를 안내합니다. | palate가 Mac의 Keynote를 이용할 수 없으면 PowerPoint와 PDF로 내보낸 파일을 요청하고, 사용자가 Mac의 Keynote에서 `.key` 형식으로 저장하고 검토하도록 안내합니다. |

Windows에서 palate는 PowerPoint 사본을 준비할 수 있지만 Keynote의 `.key` 파일을 직접 편집할 수는 없습니다. Mac의 Keynote를 이용할 수 없으면 내보내기와 최종 파일의 저장·검토 과정을 안내하고, 남은 작업을 보고서에 기록합니다. [Keynote 작업 흐름](references/keynote-workflow.md)에서 구체적인 절차와 Keynote 형식으로 결과물을 제공하기 전에 마쳐야 할 검토를 확인할 수 있습니다.

포함된 스크립트를 실행하려면 Python 3.11 이상, `lxml`, Pillow가 필요합니다. 사용할 수 있는 번들 런타임이 있으면 palate가 이를 우선 사용합니다. 포함된 Windows용 미리보기 렌더러에는 Microsoft PowerPoint가 필요합니다. 본문 수정이나 번역, 새 슬라이드 작성, 편집 가능한 객체의 재구성에는 사용 가능한 프레젠테이션 편집 도구가 필요합니다. 해당 도구를 이용할 수 없으면 palate가 결과물에 어떤 제약이 있는지 설명합니다.

원본은 보존하고 결과물은 새 파일에 저장합니다. 연구 파일은 사용자가 업로드를 명시적으로 허용하지 않는 한 로컬에만 둡니다. 이 스킬은 여러 장으로 구성된 발표 자료를 다루며 한 페이지짜리 월간 보고서는 지원 범위에 포함되지 않습니다.

## 상세 문서

다음 문서는 영어로 제공됩니다.

- [사용법·설치·실행 환경](docs/usage.md)
- [디자인 체계](references/design-system.md)
- [Keynote 작업 흐름](references/keynote-workflow.md)
- [연구 내용 보존 원칙](references/scientific-fidelity.md)
- [변환 계획](references/transform-plan.md)
- [검증](docs/validation.md)
