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

**palate** はまず、誰に向けて、何を、どのくらいの時間で伝える発表なのかを確認します。その内容を踏まえて説明の流れを組み直し、強調すべきポイントを整理しながら、各スライドのレイアウトと情報の優先順位を調整して、研究の根拠、分析、結論が伝わるように整えます。

学会発表、研究室でのミーティング、授業では、必要な説明の深さも見せ方も異なります。そのため、**palate** は決まったテンプレートに当てはめず、発表の目的や場面に合わせて構成とデザインを考えます。その過程で、研究データを勝手に変更したり、結論の意味を変えたりすることはありません。結果の解釈に関わる仮定、適用条件、不確実性も省きません。

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

**palate** は共通のデザイン基準を使い、PowerPoint と Keynote はそれぞれのアプリで編集・確認します。別の納品形式が指定されなければ、元の形式を維持します。Keynote の資料を PowerPoint に変換する必要はありません。

| 元の形式 | 受け取るファイル |
| :--- | :--- |
| PowerPoint（`.pptx`） | 新しい編集可能な `.pptx`。最終確認は PowerPoint で行います。 |
| Keynote（`.key`） | Mac の Keynote で対応する操作を適用した、新しいネイティブ `.key` の候補版。 |

原稿を開けない場合は、**palate** が互換性のある編集可能なコピーを依頼します。Keynote の処理では、Codex の実行プロセスがアプリを操作するための Mac の権限が必要です。納品先のアプリを利用できなければ、その作業と確認は未完了として記録し、引き継ぎ方法を案内します。

付属の Keynote ネイティブ処理は**実験段階で、Mac での実機テストはまだ行っていません**。macOS と Keynote が必要で、自動編集は既存のテキストボックスと図形の配置・文字スタイルに限られます。それ以外の変更には、利用可能なネイティブ編集手段が必要です。手段がなければ、その変更は保留します。対応する操作と確認項目は [Keynote ワークフロー](references/keynote-workflow.md)を参照してください。形式の変換は、別形式の納品が指定された場合や、変換する方法を選んだ場合に限り行い、変換による差異も別途確認します。

Python ツールには Python 3.11 以降が必要です。`.pptx` の検査には `lxml`、画像解像度の診断には Pillow を使い、利用可能な同梱ランタイムがあれば優先します。Windows PowerPoint 用のレンダラーは、その環境で使えるプレビュー手段の一つです。Keynote や、ほかの PowerPoint 環境で必須ではありません。最終確認には実際に納品するアプリを使います。スキルのインストールだけではアプリは導入されず、操作権限も付与されません。

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
