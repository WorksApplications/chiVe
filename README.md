# chiVe: Sudachi による日本語単語ベクトル

[English README](README_en.md)

## 概要

"chiVe" (チャイブ, Suda**chi Vec**tor) は、大規模コーパスと複数粒度分割に基づく日本語単語ベクトルです。

[Skip-gram アルゴリズム](https://arxiv.org/abs/1301.3781)を元に、word2vec ([gensim](https://radimrehurek.com/gensim/)) を使用して単語分散表現を構築しています。

学習コーパスには、v1.0-v1.2 では約 1 億のウェブページ文章を含む国立国語研究所の[日本語ウェブコーパス（NWJC）](https://masayu-a.github.io/NWJC/)、
v1.3 では [CommonCrawl](https://commoncrawl.org/) から取得したウェブページ文章を採用しています。

分かち書きにはワークスアプリケーションズの形態素解析器 [Sudachi](https://github.com/WorksApplications/Sudachi) を使用しています。
Sudachi で定義されている A/B/C の 3 つの分割単位でコーパスを解析した結果を元に分散表現の学習を行なっています。

## データ

SudachiDict と chiVe のデータは、AWS の [Open Data Sponsorship Program](https://registry.opendata.aws/sudachi/) によりホストしていただいています。

| 版        | 最低頻度 | 正規化 | 語彙数    | テキスト                                                                                      | [gensim](https://radimrehurek.com/gensim/)                                                           | [Magnitude](https://github.com/plasticityai/magnitude)                                               |
| --------- | -------- | ------ | --------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| v1.3 mc5  | 5        | o      | 2,530,791 | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc5.tar.gz))     | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc5_gensim.tar.gz))     | -                                                                                                    |
| v1.3 mc15 | 15       | o      | 1,186,019 | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc15.tar.gz))    | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc15_gensim.tar.gz))    | -                                                                                                    |
| v1.3 mc30 | 30       | o      | 759,011   | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc30.tar.gz))    | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc30_gensim.tar.gz))    | -                                                                                                    |
| v1.3 mc90 | 90       | o      | 410,533   | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc90.tar.gz))    | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc90_gensim.tar.gz))    | -                                                                                                    |
| --------- | -------- | ------ | --------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| v1.2 mc5  | 5        | o      | 3,197,456 | 9.2GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc5.tar.gz))  | 3.8GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc5_gensim.tar.gz))  | 5.5GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc5.magnitude))  |
| v1.2 mc15 | 15       | o      | 1,454,280 | 5.0GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc15.tar.gz)) | 1.7GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc15_gensim.tar.gz)) | 2.4GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc15.magnitude)) |
| v1.2 mc30 | 30       | o      | 912,550   | 3.1GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc30.tar.gz)) | 1.1GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc30_gensim.tar.gz)) | 1.5GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc30.magnitude)) |
| v1.2 mc90 | 90       | o      | 482,223   | 1.7GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc90.tar.gz)) | 0.6GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc90_gensim.tar.gz)) | 0.8GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc90.magnitude)) |
| --------- | -------- | ------ | --------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| v1.1 mc5  | 5        | o      | 3,196,481 | 11GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc5.tar.gz))   | 3.6GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc5_gensim.tar.gz))  | 5.5GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc5.magnitude))  |
| v1.1 mc15 | 15       | o      | 1,452,205 | 4.7GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc15.tar.gz)) | 1.7GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc15_gensim.tar.gz)) | 2.4GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc15.magnitude)) |
| v1.1 mc30 | 30       | o      | 910,424   | 3.0GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc30.tar.gz)) | 1.1GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc30_gensim.tar.gz)) | 1.5GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc30.magnitude)) |
| v1.1 mc90 | 90       | o      | 480,443   | 1.6GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc90.tar.gz)) | 0.6GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc90_gensim.tar.gz)) | 0.8GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc90.magnitude)) |
| v1.0 mc5  | 5        | x      | 3,644,628 | 12GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.0-mc5.tar.gz))   | 4.1GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.0-mc5_gensim.tar.gz))  | 6.3GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.0-mc5.magnitude))  |

全て 300 次元のベクトルです。

「最低頻度」は、コーパス内での単語出現回数での足切り基準（[gensim](https://radimrehurek.com/gensim/models/word2vec.html) での `min_count` ）です。

「正規化」は、形態素解析器 Sudachi による表記統制です。例えば `空き缶`, `空缶`, `空き罐`, `空罐`, `空きカン`, `空きかん` はすべて正規化表記 `空き缶` に統制されます。

| 版   | Sudachi | Sudachi 辞書          | 学習コーパス                                         |
| ---- | ------- | --------------------- | ---------------------------------------------------- |
| v1.3 | v0.6.8  | 20240109-core         | CommonCrawl (CC-MAIN-2022-40, warc, first 20k files) |
| v1.2 | v0.4.3  | 20200722-core         | NWJC                                                 |
| v1.1 | v0.3.0  | 20191030-core         | NWJC                                                 |
| v1.0 | v0.1.1  | 0.1.1-dictionary-full | NWJC                                                 |

全て同じ学習アルゴリズムを使用しています。詳細は [training](training) を参照してください。

### 「A 単位語のみ」の資源

[Sudachi 辞書](https://github.com/WorksApplications/SudachiDict)にある A 単位語のみを含む資源です（A 単位語のみでの再学習ではなく、上にある元資源から、B 単位語、C 単位語、OOV 語（Out-of-vocabulary, 辞書にない語）を除いたものです）。

`v1.1 mc90 aunit` が、自然言語処理ツール [spaCy](https://github.com/explosion/spaCy/) の日本語モデルに使われています。

| 版              | 語彙数          | テキスト                                                                                            | [gensim](https://radimrehurek.com/gensim/)                                                                 | [Magnitude](https://github.com/plasticityai/magnitude)                                                     |
| --------------- | --------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| v1.1 mc5 aunit  | 322,094 (10.1%) | 1.1GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc5-aunit.tar.gz))  | 0.4GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc5-aunit_gensim.tar.gz))  | 0.5GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc5-aunit.magnitude))  |
| v1.1 mc15 aunit | 276,866 (19.1%) | 1.0GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc15-aunit.tar.gz)) | 0.3GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc15-aunit_gensim.tar.gz)) | 0.4GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc15-aunit.magnitude)) |
| v1.1 mc30 aunit | 242,658 (26.7%) | 0.8GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc30-aunit.tar.gz)) | 0.3GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc30-aunit_gensim.tar.gz)) | 0.4GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc30-aunit.magnitude)) |
| v1.1 mc90 aunit | 189,775 (39.5%) | 0.7GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc90-aunit.tar.gz)) | 0.2GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc90-aunit_gensim.tar.gz)) | 0.3GB ([.magnitude](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc90-aunit.magnitude)) |

### 追加学習用のフルモデル

chiVe は、各ドメイン（分野）に合わせたデータで追加学習させられます。
chiVe は、追加学習なしでも利用できますが、追加学習することでそのドメイン（分野）でのタスクの性能改善が期待できます。

chiVe を追加学習するためには、フルモデルを使用してください。詳しい使用方法は、[チュートリアル](docs/continue-training.md)をご覧ください。

| 版        | [gensim](https://radimrehurek.com/gensim/) (full)                                                         |
| --------- | --------------------------------------------------------------------------------------------------------- |
| v1.3 mc5  | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc5_gensim-full.tar.gz))     |
| v1.3 mc15 | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc15_gensim-full.tar.gz))    |
| v1.3 mc30 | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc30_gensim-full.tar.gz))    |
| v1.3 mc90 | GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc90_gensim-full.tar.gz))    |
| --------- | --------------------------------------------------------------------------------------------------------- |
| v1.2 mc5  | 6.7GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc5_gensim-full.tar.gz))  |
| v1.2 mc15 | 3.0GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc15_gensim-full.tar.gz)) |
| v1.2 mc30 | 1.9GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc30_gensim-full.tar.gz)) |
| v1.2 mc90 | 1.0GB ([tar.gz](https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc90_gensim-full.tar.gz)) |

## 利用方法

「テキスト」「gensim」「Magnitude」という 3 つのフォーマットでデータを公開しています。

### テキスト

プレーンテキスト形式のデータ（オリジナルの word2vec C フォーマット）です。

```
480443 300
の -0.08274004 -0.091033645 -0.08744463 -0.14393683 -0.053159036 ...
、 -0.014216528 -0.1027064 -0.07763326 -0.16008057 -0.16116066 ...
て -0.06049706 -0.15483096 0.052628547 -0.12448246 -0.14404581 ...
...
```

### gensim

ライブラリ [gensim](https://radimrehurek.com/gensim/) のための、[KeyedVectors](https://radimrehurek.com/gensim/models/keyedvectors.html) 形式のデータです。

```py
import gensim

vectors = gensim.models.KeyedVectors.load("./chive-1.1-mc90_gensim/chive-1.1-mc90.kv")

"すだち" in vectors # False, v1.1 では正規化されているため
"酢橘" in vectors # True

vectors["酢橘"]
# array([-5.68204783e-02, -1.26615226e-01,  3.53190415e-02, -3.67305875e-01, ...])

vectors.similarity("酢橘", "徳島")
# 0.3993048

vectors.most_similar("徳島", topn=5)
# [('愛媛', 0.8229734897613525),
# ('徳島県', 0.786933422088623),
# ('高知', 0.7795713543891907),
# ('岡山', 0.7623447179794312),
# ('徳島市', 0.7415297031402588)]

vectors.most_similar(positive=["阿波", "高知"], negative=["徳島"], topn=5)
# [('土佐', 0.620033860206604),
# ('阿波踊り', 0.5988592505455017),
# ('よさこい祭り', 0.5783430337905884),
# ('安芸', 0.564490556716919),
# ('高知県', 0.5591559410095215)]
```

### Magnitude (~v1.2)

ライブラリ [Magnitude](https://github.com/plasticityai/magnitude) 形式のデータです。デフォルトのパラメーターで変換されています（高度な未知語サポート有り、近似最近傍インデックス無し。Magnitude が公開しているモデルの `Medium` 相当）。

```py
from pymagnitude import Magnitude

vectors = Magnitude("chive1.1-mc90.magnitude")

"すだち" in vectors # False, v1.1 では正規化されているため
"酢橘" in vectors # True

vectors.query("すだち") # Magnitudeによるサブワードを使った未知語サポートによる
# array([ 0.03974148,  0.11290773,  0.01493122, -0.05296252,  0.12616251, ...])

vectors.most_similar("すだち", topn=5)
# [('あだち', 0.5930323079944302),
# ('すだ椎', 0.5872662462335323),
# ('だち', 0.5797546444016177),
# ('ムクノキ', 0.46228053338159725),
# ('椨', 0.4482612387097178)]

vectors.similarity("酢橘", "徳島")
# 0.3993048

vectors.most_similar("徳島", topn=5)
# [('愛媛', 0.8229735),
# ('徳島県', 0.78693324),
# ('高知', 0.7795714),
# ('岡山', 0.7623447),
# ('徳島市', 0.7415296)]

vectors.closer_than("徳島", "徳島市")
# ['愛媛', '徳島県', '高知', '岡山']

vectors.most_similar(positive=["阿波", "高知"], negative=["徳島"], topn=5)
# [('土佐', 0.62003386),
# ('阿波踊り', 0.5988593),
# ('よさこい祭り', 0.578343),
# ('安芸', 0.56449056),
# ('高知県', 0.55915594)]

vectors.most_similar_cosmul(positive=["阿波", "高知"], negative=["徳島"], topn=5)
# [('土佐', 0.83830714),
# ('よさこい祭り', 0.82048166),
# ('阿波踊り', 0.8168015),
# ('安芸', 0.80880433),
# ('伊予', 0.80250806)]
```

ライブラリを使っての、ダウンロード、リモートでのロード、HTTP 上のリモートでのストリームも可能です。

```py
from pymagnitude import Magnitude, MagnitudeUtils

# ダウンロード
vectors = Magnitude(MagnitudeUtils.download_model("chive-1.1-mc90-aunit", remote_path="https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/"))
 # デフォルトのダウンロード先: `~/.magnitude/`
 # ファイルが既にダウンロードされている場合は、再度ダウンロードしない
 # 引数 `download_dir` でローカルのダウンロード先を変更できる

# リモートでのロード
vectors = Magnitude("https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc90-aunit.magnitude")

# HTTP上のリモートでのストリーム
vectors = Magnitude("https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.1-mc90-aunit.magnitude", stream=True)
vectors.query("徳島") # ローカルにファイルをダウンロードせず、ベクトルをすばやく取得
```

## ライセンス

### v1.0, v1.1, v1.2

Copyright (c) 2020 National Institute for Japanese Language and Linguistics and Works Applications Co., Ltd. All rights reserved.

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) の下で[国立国語研究所](https://www.ninjal.ac.jp/)と[株式会社ワークスアプリケーションズ](https://www.worksap.co.jp/)によって提供されています。

### v1.3

Copyright (c) 2024 Works Applications Co., Ltd. All rights reserved.

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) の下で[株式会社ワークスアプリケーションズ](https://www.worksap.co.jp/)によって提供されています。

## Slack

開発者やユーザーの方々が質問したり議論するための Slack ワークスペースを用意しています。

- https://sudachi-dev.slack.com/
- ([こちら](https://join.slack.com/t/sudachi-dev/shared_invite/enQtMzg2NTI2NjYxNTUyLTMyYmNkZWQ0Y2E5NmQxMTI3ZGM3NDU0NzU4NGE1Y2UwYTVmNTViYjJmNDI0MWZiYTg4ODNmMzgxYTQ3ZmI2OWU)から招待を受けてください)

## chiVe の引用

chiVe について、論文を発表しています;

- 真鍋陽俊, 岡照晃, 海川祥毅, 髙岡一馬, 内田佳孝, 浅原正幸. [複数粒度の分割結果に基づく日本語単語分散表現](https://www.anlp.jp/proceedings/annual_meeting/2019/pdf_dir/P8-5.pdf). 言語処理学会第 25 回年次大会, 2019.
- 河村宗一郎, 久本空海, 真鍋陽俊, 高岡一馬, 内田佳孝, 岡照晃, 浅原正幸. [chiVe 2.0: Sudachi と NWJC を用いた実用的な日本語単語ベクトルの実現へ向けて](https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P6-16.pdf). 言語処理学会第 26 回年次大会, 2020.
- 久本空海, 山村崇, 勝田哲弘, 竹林佑斗, 髙岡一馬, 内田佳孝, 岡照晃, 浅原正幸. [chiVe: 製品利用可能な日本語単語ベクトル資源の実現へ向けて](https://www.ieice.org/ken/paper/20200910U1zQ/). 第 16 回テキストアナリティクス・シンポジウム, 2020. （[スライド](https://speakerdeck.com/sorami/chive-zhi-pin-li-yong-ke-neng-nari-ben-yu-dan-yu-bekutoruzi-yuan-falseshi-xian-hexiang-kete)）

chiVe を論文や書籍、サービスなどで引用される際には、以下の BibTex をご利用ください（基本的には、1 本目の(真鍋+ 2019)を引用してください）。

```
@INPROCEEDINGS{manabe2019chive,
    author    = {真鍋陽俊, 岡照晃, 海川祥毅, 髙岡一馬, 内田佳孝, 浅原正幸},
    title     = {複数粒度の分割結果に基づく日本語単語分散表現},
    booktitle = "言語処理学会第25回年次大会(NLP2019)",
    year      = "2019",
    pages     = "NLP2019-P8-5",
    publisher = "言語処理学会",
}
```

```
@INPROCEEDINGS{kawamura2020chive,
    author    = {河村宗一郎, 久本空海, 真鍋陽俊, 高岡一馬, 内田佳孝, 岡照晃, 浅原正幸},
    title     = {chiVe 2.0: SudachiとNWJCを用いた実用的な日本語単語ベクトルの実現へ向けて},
    booktitle = "言語処理学会第26回年次大会(NLP2020)",
    year      = "2020",
    pages     = "NLP2020-P6-16",
    publisher = "言語処理学会",
}
```

```
@INPROCEEDINGS{hisamoto2020chive,
    author    = {久本空海, 山村崇, 勝田哲弘, 竹林佑斗, 髙岡一馬, 内田佳孝, 岡照晃, 浅原正幸},
    title     = {chiVe: 製品利用可能な日本語単語ベクトル資源の実現へ向けて},
    booktitle = "第16回テキストアナリティクス・シンポジウム",
    year      = "2020",
    pages     = "IEICE-NLC2020-9",
    publisher = "電子情報通信学会",
}
```
