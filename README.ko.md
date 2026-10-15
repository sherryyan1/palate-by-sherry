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

**palate**는 Sherry의 스타일로 연구 발표 자료를 다듬는 Codex 스킬입니다. 청중과 발표 목적, 주어진 시간에 맞춰 설명의 흐름을 잡고, 근거와 논리를 따라가기 쉽게 슬라이드를 구성합니다. 이 과정에서 연구의 의미와 해석에 필요한 조건을 보존합니다.

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

발표 조건을 처음부터 알려주어도 되고, 이 한 문장으로 시작해도 됩니다. palate는 이미 제공한 정보를 활용하고, 디자인 결정에 필요한 내용만 추가로 묻습니다. 설명의 깊이를 맡기면 먼저 슬라이드를 살펴본 뒤 발표에 필요한 설명 수준을 정합니다. 스킬을 명시적으로 호출하려면 `$palate`를 사용할 수 있습니다. 어떤 정보가 발표 방향을 결정하는지는 [사용 안내](docs/usage.md)에서 확인할 수 있습니다.

## 안내문·대화·슬라이드의 언어

이 안내문의 언어와 대화에 사용할 언어, 슬라이드의 언어는 각각 정할 수 있습니다. 한국어로 안내를 읽고 대화하면서 영어 학회 발표 자료를 요청해도 됩니다.

```text
palate로 이 발표 자료를 다듬어 주세요. 설명은 한국어로, 학회 발표 슬라이드는 영어로 작성해 주세요.
```

번역을 명시적으로 요청하지 않으면 슬라이드는 원문의 언어를 유지합니다. 기존 객체의 배치와 서식을 조정하는 보조 스크립트는 본문을 번역하지 않습니다. 번역이나 내용 재구성에는 편집 가능한 텍스트와 도표를 생성·수정할 수 있는 별도의 작성 도구를 사용하고, 원문의 과학적 의미, 수치, 단위와 해석상의 한계가 유지되는지 검토합니다. 상세 사용 안내와 기술 문서는 영어로 제공됩니다.

## 슬라이드를 다듬는 방식

디자인은 청중이 무엇을 이해해야 하는지에서 출발합니다. 튜토리얼에서는 작동 원리를 단계적으로 풀어야 할 수 있고, 연구 회의에서는 토론할 수 있도록 방법과 불확실성을 함께 보여주어야 할 수 있습니다. 발표 시간은 현장에서 어디까지 설명할지, 어떤 보충 자료를 발표자 노트나 부록에 둘지 판단하는 기준입니다. 시간만으로 슬라이드 수를 정하지는 않습니다.

명확한 시각적 위계, 청록색 강조, 근거 주변의 여백과 간격으로 정보의 관계를 드러냅니다. 결과를 비교할 때는 비교 가능한 척도를 사용하고, 방법은 순서가 보이도록 구성합니다. 결과를 뒷받침하는 근거와 해석에 필요한 조건은 해당 결과 가까이에 둡니다. 긴 설명에서는 내용에 맞는 섹션 안내 화살표와 개념별 진행 표시로 청중이 현재 위치를 파악하도록 돕습니다.

palate는 데이터, 단위, 수식, 라벨, 불확실성, 해석상의 한계와 참고문헌을 보존합니다. 기존 객체는 도구가 지원하는 범위에서 개별 편집이 가능한 상태로 유지하고, 재구성의 정확성을 검증할 수 없는 복잡한 그림은 원형을 유지합니다. 결과물은 새 파일로 저장한 편집 가능한 발표 자료와 간결한 변경 보고서입니다. 보고서에는 변경 내용, 수행한 검사와 남은 한계를 밝히며, 내용 보존·편집 가능 여부·렌더링 결과는 각각 검토합니다.

## 파일 형식과 실행 환경

PowerPoint와 Keynote에는 같은 디자인 원칙을 적용하지만, 준비와 최종 검토 절차는 다릅니다.

| 원본 | 준비 | 최종 검토 |
| :--- | :--- | :--- |
| PowerPoint | 지원되는 편집 가능 파일을 검사합니다. 기존 객체를 보존하고, 변경 범위가 크면 편집 가능한 객체를 생성하는 작성 도구를 사용합니다. | 최종 발표에 사용할 애플리케이션에서 내용, 화면 표시와 편집 가능 여부를 확인합니다. |
| Keynote | PowerPoint 사본과 검토용 PDF를 내보냅니다. 디자인을 바꾸기 전에 내보낸 파일을 원본과 비교합니다. | 결과물을 Keynote에서 열고 저장한 뒤 변환 결과, 글꼴, 객체의 편집 가능 여부와 필요한 재생 동작을 확인합니다. |

내보내기 설정과 변환 검토 절차는 [Keynote 작업 흐름](references/keynote-workflow.md)에 설명되어 있습니다. Windows에서는 PowerPoint 형식의 중간 결과물을 준비할 수 있습니다. Keynote 형식의 최종 결과물을 제공하려면 Mac의 Keynote에서 최종 파일을 저장하고 검토해야 합니다. 이 절차를 실제로 수행하기 전까지 Keynote 검토는 미완료 상태로 남습니다.

포함된 스크립트에는 Python 3.11 이상, `lxml`, Pillow가 필요합니다. 번들 런타임을 사용할 수 있다면 이를 우선 사용합니다. Windows용 미리보기 렌더러에는 Microsoft PowerPoint가 필요하며, 새 슬라이드를 만들거나 기존 슬라이드를 재구성하려면 편집 가능한 프레젠테이션을 작성할 수 있는 도구가 필요합니다.

원본은 보존하고 결과물은 새 파일에 저장합니다. 연구 파일은 사용자가 업로드를 명시적으로 허용하지 않는 한 로컬에만 둡니다. 이 스킬은 여러 장으로 구성된 발표 자료를 다루며, 한 페이지짜리 월간 보고서는 지원 범위에 포함되지 않습니다.

## 상세 문서

다음 문서는 영어로 제공됩니다.

- [사용법·설치·실행 환경](docs/usage.md)
- [디자인 체계](references/design-system.md)
- [Keynote 작업 흐름](references/keynote-workflow.md)
- [연구 내용 보존 원칙](references/scientific-fidelity.md)
- [변환 계획](references/transform-plan.md)
- [검증](docs/validation.md)
