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
  <a href="#はじめに">はじめに</a> &nbsp;·&nbsp;
  <a href="references/design-system.md">デザインの考え方（英語）</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">詳しい使い方（英語）</a>
</p>

**palate** は、研究発表のスライドを Sherry のスタイルに沿って整える Codex スキルです。聴衆、発表の目的、持ち時間を踏まえて必要な説明の深さを考え、データと論理のつながりを追いやすい構成に整えます。その際も、研究の科学的な意味や、結論を解釈するための条件を保ちます。

A palate for ideas, a palette for slides.

## はじめに

リポジトリのルートで、依存ライブラリとスキルをインストールします。

```powershell
python -m pip install -r requirements.txt
python scripts/package_skill.py --output dist/palate.zip --install "$env:USERPROFILE\.codex\skills\palate"
```

スライドを添付し、たとえば次の一文で依頼できます。

```text
palate でこの研究発表のスライドを整えてください。
```

最初から詳しい条件を伝えても、この一文から始めても構いません。palate はすでに伝えられた情報を使い、デザインの判断に必要な条件だけを確認します。説明の深さを任せた場合は、スライドの内容を確認してから、発表に必要な詳しさを判断します。スキルを明示して呼び出す場合は `$palate` を使えます。依頼時に決める項目は、[使い方ガイド](docs/usage.md)で説明しています。

## スライドをどう整えるか

出発点は、聴衆に何を理解してもらう必要があるかです。チュートリアルでは仕組みを段階的に説明することが有効でも、研究ミーティングでは議論に必要な手法や不確実性を見える形で残す必要があります。持ち時間に応じて、本編でどこまで説明を展開し、どの補足情報をノートや付録に置くかを判断します。時間だけからスライド枚数を機械的に決めることはしません。

情報の優先順位、ティールのアクセント、データの周囲の余白を使って、内容の関係を読み取りやすくします。比較する結果は尺度をそろえるなどして違いを見極めやすくし、手法は論理を追える順序で示します。結果の解釈は、その根拠や必要な限定条件の近くに置きます。長い説明では、内容に応じてセクションを示す矢印や分割した説明の進行を示す番号も使います。

データ、数値、単位、数式、ラベル、凡例、不確実性、限定条件、参考文献は保持します。ツールが対応する既存のテキストや図表は、編集できる状態を維持します。再構成の正しさを検証できない複雑な図は、そのまま残します。成果物は新しい編集可能なスライドファイルと、変更点、確認内容、残る制約をまとめた簡潔なレポートです。内容の正確さ、編集可能性、実際に表示した際の見え方は、それぞれ別に確認します。

## 言語の扱い

README の表示言語、会話に使う言語、スライドの言語は別々に扱います。日本語版 README を読んでも、スライドが自動的に日本語になることはありません。翻訳を明示的に依頼しない限り、スライドは元の言語を保ちます。

翻訳や内容の再構成が必要な場合は、編集可能なテキストや図表を作成・編集するワークフローを使い、科学的な意味が保たれているかを確認します。既存要素の配置や書式だけを調整する補助スクリプトは、本文を翻訳しません。詳細な使い方、実行手順、コードなどの文書は英語です。

## 対応形式と必要な環境

PowerPoint と Keynote には同じデザインの考え方を適用しますが、作業前の準備と最終確認の手順は異なります。

| 元の形式 | 作業前の準備 | 最終確認 |
| :--- | :--- | :--- |
| PowerPoint | 対応する編集可能なファイルを確認します。既存の要素を保持し、大きな変更には編集可能な要素を作成するワークフローを使います。 | 納品先のアプリケーションで、内容、見え方、編集可能性を確認します。 |
| Keynote | PowerPoint 形式のコピーと、見た目を比較するための PDF を書き出します。デザインを変更する前に、書き出したファイルを元のスライドと比較します。 | 結果を Keynote で開いて新しいファイルに保存し、変換結果、フォント、編集可能性、必要な再生動作を確認します。 |

書き出しと変換の確認項目は、[Keynote ワークフロー](references/keynote-workflow.md)を参照してください。Windows では、中間ファイルとなる PowerPoint スライドまで準備できます。Keynote 形式での納品には Mac 版 Keynote が必要で、最終ファイルの保存と確認もそこで行います。この確認を終えるまでは、Keynote 形式での納品作業は完了扱いにしません。

付属スクリプトには Python 3.11 以降、`lxml`、Pillow が必要です。利用できる同梱ランタイムがあれば、それを使います。付属の Windows 用プレビュー出力には Microsoft PowerPoint が必要です。スライドの新規作成や再構成には、編集可能なネイティブ要素を扱える作成環境が別途必要です。

元のファイルは保持し、成果物は新しいファイルに保存します。研究ファイルは、アップロードが明示的に許可されない限りローカルに留めます。このスキルは複数枚の研究発表スライドを対象としており、月次報告を 1 ページにまとめる用途は対象外です。

## 詳細ドキュメント

以下のドキュメントは英語です。

- [使い方、インストール、必要な環境](docs/usage.md)
- [デザインシステム](references/design-system.md)
- [Keynote ワークフロー](references/keynote-workflow.md)
- [科学的内容の保持](references/scientific-fidelity.md)
- [変換計画の仕様](references/transform-plan.md)
- [検証方法](docs/validation.md)
