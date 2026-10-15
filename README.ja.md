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
  <a href="#使ってみる">使ってみる</a> &nbsp;·&nbsp;
  <a href="references/design-system.md">デザインの考え方（英語）</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">詳しい使い方（英語）</a>
</p>

*A palate for ideas, a palette for slides.*

**palate** は、研究者のプレゼン資料をよりわかりやすく整える Codex スキルです。複雑な研究内容でも、聞き手が話の流れを追いやすいように、構成からデザインまで見直します。

**今あるプレゼン資料を、そのままアップロードしてください。** 文字が詰まっていても、レイアウトがばらばらでも、まだ作成途中でもかまいません。あらかじめ整えておく必要はありません。

まず確認するのは、誰に向けて、何を、どのくらいの時間で伝える発表なのか。そこから説明の順序を組み直し、重要なポイントを整理して、データと主張のつながりが伝わるようにスライドを一枚ずつ調整します。

学会発表、研究室でのミーティング、授業では、必要な説明の深さも見せ方も異なります。決まったテンプレートに当てはめるのではなく、発表の目的に合わせて構成を考えます。研究内容の意味や重要な前提条件を勝手に変えることはありません。

完成後は、**編集可能なプレゼン資料**と、変更点や確認した内容、追加で確認が必要な箇所をまとめた短いレポートを受け取れます。

## <img src="assets/icons/square-terminal.svg" width="22" height="22" align="bottom" alt="">&nbsp; 使ってみる

### 01 | **palate** をインストールする

Codex を開き、次の依頼を貼り付けます。Codex が実行環境と必要なツールを確認し、インストールを進めます。

```text
https://github.com/sherryyan1/palate-by-sherry から Codex スキル palate をインストールしてください。

Codex が動作する環境を確認し、docs/installation.md に従って、$palate が利用可能になったことを確認してください。すでにインストールされている場合は、置き換える前に確認してください。
```

### 02 | プレゼン資料をアップロードする

今あるプレゼン資料を添付します。文字が多くても、レイアウトがそろっていなくても、作成途中でもかまいません。

```text
$palate でこのプレゼン資料を整えてください。
```

### 03 | 発表の条件を伝える

聴衆、持ち時間、必要な説明の詳しさが決まっていれば、最初に伝えてください。詳しい依頼書は不要です。**palate** はすでに伝えられた情報を使い、デザインの判断を左右する不足事項だけを確認します。説明の詳しさを任せる場合は、資料と発表の条件を見て判断します。ほかの依頼方法は[使い方ガイド](docs/usage.md)で説明しています。

インストール先は、Codex が動作する Windows、macOS、Linux の実行環境です。チャットに使う端末と、Codex が実際に動作するコンピュータやリモート環境は、同じとは限りません。iOS／iPadOS 上でのネイティブインストールは、この手順の対象外です。追加の権限や操作、Codex の再起動が必要な場合は、その時点で Codex が案内します。手動で設定する場合は[インストール手順](docs/installation.md)を参照してください。

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; 対応言語

この README は **English、简体中文、日本語、한국어** で読めます。ページ上部のリンクから表示言語を切り替えられます。

翻訳を依頼しない限り、**palate** はプレゼン資料の元の言語を保ちます。翻訳する場合も、数値、単位、科学的な意味は変えません。専門用語に複数の訳語があり、選び方によって科学的な意味が変わる場合は、推測で決めずに確認します。

## <img src="assets/icons/compass.svg" width="22" height="22" align="bottom" alt="">&nbsp; デザインの考え方

### <img src="assets/icons/users-round.svg" width="22" height="22" align="top" alt="">&nbsp; 01 | 聴衆から考える

<sub><em>聴衆に何を理解してもらう必要があるか？</em></sub>

チュートリアルでは仕組みを段階的に説明し、研究室のミーティングでは議論に必要な手法や不確実性を示すなど、**palate** は発表の場に合わせて説明の深さを調整します。

持ち時間は、説明の**深さと進め方**を決める手がかりです。時間からスライド枚数を機械的に決めることはせず、補足情報は必要に応じてノートや付録に置きます。

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/chart-no-axes-combined.svg" width="22" height="22" align="top" alt="">&nbsp; 02 | 根拠と論理を見せる

<sub><em>根拠と論理のつながりを、どうすれば追いやすくできるか？</em></sub>

**palate** は情報の優先順位を整理し、比較が妥当な結果は尺度をそろえて示します。手法は論理を追える順序で示し、結果はその根拠や解釈に必要な条件の近くに置きます。

余白、ティールのアクセント、セクションや説明の進行を示すマーカーは、関係や順序を伝えるために使います。すべてのスライドに一律に加えるものではありません。

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/shield-check.svg" width="22" height="22" align="top" alt="">&nbsp; 03 | 科学的な意味を守る

<sub><em>デザインを変えても、変えてはいけないものは何か？</em></sub>

**palate** はデータ、数値、単位、数式、ラベル、凡例、不確実性、限定条件、参考文献を保持します。既存の要素はツールが対応する範囲で編集できる状態を維持し、再構成の正しさを検証できない複雑な図はそのまま残します。

### <img src="assets/icons/package-check.svg" width="22" height="22" align="top" alt="">&nbsp; 受け取れるもの

ツールと形式が対応する範囲で、新しい編集可能なプレゼン資料と、変更点、完了した確認、残る制約をまとめた短いレポートを受け取れます。**palate** は科学的内容、編集可能性、実際の表示をそれぞれ確認します。重要な確認を完了できない場合は、残る作業を明記し、資料を最終版ではなく確認待ちの候補版として渡します。

## <img src="assets/icons/files.svg" width="22" height="22" align="bottom" alt="">&nbsp; 対応形式と必要な環境

**palate** は PowerPoint と Keynote に同じデザインの考え方を適用します。元の形式によって、必要なファイルと最終確認を完了できる環境が異なります。

| 元の形式 | 受け取るファイル |
| :--- | :--- |
| PowerPoint（`.pptx`） | 原稿と照合した、編集可能な新しい `.pptx`。 |
| Keynote（`.key`） | 書き出した `.pptx` と PDF を基にした、編集可能な新しい `.pptx`。`.key` は Mac の Keynote で保存・確認後に渡します。 |

原稿を開けない場合は、**palate** が互換性のある編集可能なコピーを依頼します。納品先アプリでの確認ができない場合は、残る確認の手順を案内します。Mac の Keynote を **palate** が利用できない場合は、PowerPoint と PDF の書き出しファイルを提供し、Mac で保存と確認を行ってください。

Windows では、**palate** は `.pptx` ファイルを準備できますが、Keynote の `.key` ファイルを直接編集することはできません。Keynote 形式で受け取るには、Mac の Keynote で保存と最終確認を完了する必要があります。それまでは `.pptx` ファイルが成果物となり、**palate** は残る Keynote の作業をレポートに記載します。詳しくは [Keynote ワークフロー](references/keynote-workflow.md)を参照してください。

付属スクリプトの実行には Python 3.11 以降、`lxml`、Pillow が必要です。利用できる同梱ランタイムがあれば、**palate** がそれを使います。付属の Windows 用プレビュー出力には Microsoft PowerPoint が必要です。本文の変更や翻訳、スライドの新規作成、編集可能な要素の再構成には、利用可能なプレゼンテーション編集ツールが必要です。そのツールを利用できない場合は、**palate** が成果物への制約を説明します。

**palate** は元のファイルを保持し、成果物を新しいファイルに保存します。ファイルを扱う場所は、Codex の実行環境がローカルかクラウドかによって異なります。研究ファイルを別のサービスへ送信する前に、**palate** が許可を確認します。このスキルは複数枚のプレゼン資料を対象としており、月次報告を 1 ページにまとめる用途は対象外です。

## <img src="assets/icons/book-open.svg" width="22" height="22" align="bottom" alt="">&nbsp; 詳細ドキュメント

以下のドキュメントは英語です。

- [使い方](docs/usage.md)
- [インストールと必要な環境](docs/installation.md)
- [伝わる説明の組み立て方](references/communication-design.md)
- [デザインシステム](references/design-system.md)
- [Keynote ワークフロー](references/keynote-workflow.md)
- [科学的内容の保持](references/scientific-fidelity.md)
- [変換計画の仕様](references/transform-plan.md)
- [検証方法](docs/validation.md)
