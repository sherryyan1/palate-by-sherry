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

**palate** は、研究発表のスライドをよりわかりやすく整える Codex スキルです。複雑な研究内容でも、聞き手が話の流れを追いやすいように、構成からデザインまで見直します。

**今ある PowerPoint を、そのままアップロードしてください。** 文字が詰まっていても、レイアウトがばらばらでも、まだ作成途中でもかまいません。あらかじめ整えておく必要はありません。

まず確認するのは、誰に向けて、何を、どのくらいの時間で伝える発表なのか。そこから説明の順序を組み直し、重要なポイントを整理して、データと主張のつながりが伝わるようにスライドを一枚ずつ調整します。

学会発表、研究室でのミーティング、授業では、必要な説明の深さも見せ方も異なります。決まったテンプレートに当てはめるのではなく、発表の目的に合わせて構成を考えます。研究内容の意味や重要な前提条件を勝手に変えることはありません。

完成後は、**編集可能な PowerPoint ファイル**と、変更点や確認した内容、追加で確認が必要な箇所をまとめた短いレポートを受け取れます。

*A palate for ideas, a palette for slides.*

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

palate はデータ、数値、単位、数式、ラベル、凡例、不確実性、限定条件、参考文献を保持します。ツールが対応する既存のテキストや図表は、編集できる状態を維持します。再構成の正しさを検証できない複雑な図は、そのまま残します。新しい編集可能なスライドファイルと、変更点、確認内容、残る制約をまとめた簡潔なレポートを受け取れます。palate は内容が保たれているか、編集できるか、実際の表示に問題がないかをそれぞれ確認します。必要な確認を完了できない場合は、残る作業をレポートに明記し、スライドを確認待ちの候補版として渡します。

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; 対応言語

この README は **English、简体中文、日本語、한국어** で読めます。ページ上部のリンクから表示言語を切り替えられます。

翻訳を依頼しない限り、スライドは元の言語を保ちます。

翻訳を依頼すると、palate は数値、単位、科学的な意味を保ちながら、内容の翻訳を支援します。専門用語に複数の訳語が考えられる場合は、推測で決めずに確認します。

## 対応形式と必要な環境

palate は PowerPoint と Keynote に同じデザインの考え方を適用します。元の形式によって、必要なファイルと最終確認を完了できる環境が異なります。

| 元の形式 | palate が行うこと | 協力が必要になる場合 |
| :--- | :--- | :--- |
| PowerPoint | 互換性のある編集可能なスライドを整え、ツールが対応する範囲で要素の編集可能性を保ちます。結果を元のスライドと照合します。 | 元のファイルを開けない場合は、互換性のある編集可能なコピーの提供をお願いします。palate が納品先のアプリケーションを利用できない場合は、残る確認をお願いし、その手順を案内します。 |
| Keynote | デザインを変更する前に、PowerPoint の書き出しファイルを元のスライドや見た目の基準となる PDF と比較します。その後、新しい PowerPoint のコピーを整え、Keynote での最終確認を案内します。 | palate が Mac の Keynote を利用できない場合は、PowerPoint と PDF の書き出しファイルの提供と、Mac の Keynote で `.key` ファイルとして保存し、確認する作業をお願いします。 |

Windows では、palate は PowerPoint のコピーを準備できますが、Keynote の `.key` ファイルを直接編集することはできません。Mac の Keynote を利用できない場合は、書き出しと最終ファイルの保存・確認を案内し、残る作業をレポートに記載します。[Keynote ワークフロー](references/keynote-workflow.md)では、具体的な手順と、Keynote 形式での納品を完了するために必要な確認を説明しています。

付属スクリプトの実行には Python 3.11 以降、`lxml`、Pillow が必要です。利用できる同梱ランタイムがあれば、palate がそれを使います。付属の Windows 用プレビュー出力には Microsoft PowerPoint が必要です。本文の変更や翻訳、スライドの新規作成、編集可能な要素の再構成には、利用可能なプレゼンテーション編集ツールが必要です。そのツールを利用できない場合は、palate が納品内容への制約を説明します。

元のファイルは保持し、成果物は新しいファイルに保存します。研究ファイルは、アップロードが明示的に許可されない限りローカルに留めます。このスキルは複数枚の研究発表スライドを対象としており、月次報告を 1 ページにまとめる用途は対象外です。

## 詳細ドキュメント

以下のドキュメントは英語です。

- [使い方、インストール、必要な環境](docs/usage.md)
- [デザインシステム](references/design-system.md)
- [Keynote ワークフロー](references/keynote-workflow.md)
- [科学的内容の保持](references/scientific-fidelity.md)
- [変換計画の仕様](references/transform-plan.md)
- [検証方法](docs/validation.md)
