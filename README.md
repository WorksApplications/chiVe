# chiVe: Japanese Word Embedding with Sudachi & NWJC

[日本語 README](#chive-sudachiとnwjcによる日本語単語ベクトル)

*(See [GitHub - WorksApplications/chiVe](https://github.com/WorksApplications/chiVe) for the latest README)*

## Abstract

"chiVe" (Suda**chi Ve**ctor) is a Japanese pre-trained word embedding resource using large-scale corpus and multi-granular tokenization.

Based on the [skip-gram algorithm](https://arxiv.org/abs/1301.3781), we used word2vec ([gensim](https://radimrehurek.com/gensim/)) to train the vectors.

We used [NINJAL Web Japanese Corpus (NWJC)](https://pj.ninjal.ac.jp/corpus_center/nwjc/) from National Institute for Japanese Language and Linguistics which contains around 100 million web page text as a training corpus, and used [Sudachi](https://github.com/WorksApplications/Sudachi) by Works Applications for tokenization.

We used Sudachi's multi-granular tokenziation results (short, mid, and named entity) of NWJC text to train word vectors.

## Data

|Version     | Normalized | Min Count | Vocab      | Binary | Text |SudachiDict            | Download |
|----------|-----|------|---------|-----|--------|---------------------|--------|
|v1.0 mc5  |x    |5     |3,644,628|4.1GB|12GB    |0.1.1-dictionary-full| [tar.gz](https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/chive/chive-1.0-mc5-20190314.tar.gz) (4.9GB) |
|v1.1 mc5 |o    |5     |3,196,481|3.6GB|11GB    |20191030-core        | [tar.gz](https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/chive/chive-1.1-mc5-20200318.tar.gz) (4.4GB) |
|v1.1 mc15|o    |15    |1,452,205|1.7GB|4.7GB   |20191030-core        | [tar.gz](https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/chive/chive-1.1-mc15-20200318.tar.gz) (2.0GB) |
|v1.1 mc30|o    |30    |910,424  |1.1GB|3.0GB   |20191030-core        | [tar.gz](https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/chive/chive-1.1-mc30-20200318.tar.gz) (1.3GB) |
|v1.1 mc90|o    |90    |480,443  |0.6GB|1.6GB   |20191030-core        | [tar.gz](https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/chive/chive-1.1-mc90-20200318.tar.gz) (0.7GB) |

The format is based on the original word2vec.

The training algorithm is the same for both v1.0 and v1.1.

"Normalized" indicates if the text is normalized using the tokenizer Sudachi. For example, words `空き缶`, `空缶`, `空き罐`, `空罐`, `空きカン`, `空きかん` will all be normalized to `空き缶`.

"Min Count" indicates the number of minimum appearance count in the training corpus (`min_count` in [gensim](https://radimrehurek.com/gensim/models/word2vec.html)).

Sudachi version: [v0.1.1](https://github.com/WorksApplications/Sudachi/releases/tag/v0.1.1) for chiVe 1.0 and [v0.3.0](https://github.com/WorksApplications/Sudachi/releases/tag/v0.3.0) for chiVe1.1.

## Licence

Copyright (c) 2020 National Institute for Japanese Language and Linguistics and Works Applications Co., Ltd. All rights reserved.

"chiVe" is distributed by [National Institute for Japanese Langauge and Linguistics](https://www.ninjal.ac.jp/) and [Works Applications Co.,Ltd.](https://www.worksap.co.jp/) under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Slack

We have a Slack workspace for developers and users to ask questions and discuss a variety of topics.

- https://sudachi-dev.slack.com/
- (Please get an invite from [here](https://join.slack.com/t/sudachi-dev/shared_invite/enQtMzg2NTI2NjYxNTUyLTMyYmNkZWQ0Y2E5NmQxMTI3ZGM3NDU0NzU4NGE1Y2UwYTVmNTViYjJmNDI0MWZiYTg4ODNmMzgxYTQ3ZmI2OWU))


## Citing chiVe

We have published a following paper about chiVe;

- 真鍋陽俊, 岡照晃, 海川祥毅, 髙岡一馬, 内田佳孝, 浅原正幸. [複数粒度の分割結果に基づく日本語単語分散表現](https://www.anlp.jp/proceedings/annual_meeting/2019/pdf_dir/P8-5.pdf) *(Japanese Word Embedding based on Multi-granular Tokenization Results, in Japanese)*. 言語処理学会第25回年次大会, 2019.
- 河村宗一郎, 久本空海, 真鍋陽俊, 高岡一馬, 内田佳孝, 岡照晃, 浅原正幸. [chiVe 2.0: SudachiとNWJCを用いた実用的な日本語単語ベクトルの実現へ向けて](https://www.anlp.jp/nlp2020/) *(chiVe 2.0: Towards Prctical Japanese Embedding wiht Sudachi and NWJC, in Japanese)*. 言語処理学会第26回年次大会, 2020.

When citing chiVe in papers, books, or services, please use the follow BibTex entries;

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

***

# chiVe: SudachiとNWJCによる日本語単語ベクトル

[English README](#chive-japanese-word-embedding-with-sudachi--nwjc)

*（最新のREADMEは [GitHub - WorksApplications/chiVe](https://github.com/WorksApplications/chiVe) を参照してください）*

## 概要

"chiVe" (チャイブ, Suda**chi Vec**tor) は、大規模コーパスと複数粒度分割に基づく日本語単語ベクトルです。

[Skip-gramアルゴリズム](https://arxiv.org/abs/1301.3781)を元に、word2vec （[gensim](https://radimrehurek.com/gensim/)） を使用して単語分散表現を構築しています。

学習には約1億のウェブページ文章を含む国立国語研究所の[日本語ウェブコーパス（NWJC）](https://pj.ninjal.ac.jp/corpus_center/nwjc/)を採用し、分かち書きにはワークスアプリケーションズの形態素解析器[Sudachi](https://github.com/WorksApplications/Sudachi)を使用しています。

Sudachiで定義されている短・中・長単位の3つの分割単位でNWJCを解析した結果を元に分散表現の学習を行なっています。

## データ

|版     |正規化|最低頻度|語彙数      |バイナリ |テキスト|Sudachi辞書            |ダウンロード  |
|----------|-----|------|---------|-----|--------|---------------------|--------|
|v1.0 mc5  |x    |5     |3,644,628|4.1GB|12GB    |0.1.1-dictionary-full| [tar.gz](https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/chive/chive-1.0-mc5-20190314.tar.gz) (4.9GB) |
|v1.1 mc5 |o    |5     |3,196,481|3.6GB|11GB    |20191030-core        | [tar.gz](https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/chive/chive-1.1-mc5-20200318.tar.gz) (4.4GB) |
|v1.1 mc15|o    |15    |1,452,205|1.7GB|4.7GB   |20191030-core        | [tar.gz](https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/chive/chive-1.1-mc15-20200318.tar.gz) (2.0GB) |
|v1.1 mc30|o    |30    |910,424  |1.1GB|3.0GB   |20191030-core        | [tar.gz](https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/chive/chive-1.1-mc30-20200318.tar.gz) (1.3GB) |
|v.1.1 mc90|o    |90    |480,443  |0.6GB|1.6GB   |20191030-core        | [tar.gz](https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/chive/chive-1.1-mc90-20200318.tar.gz) (0.7GB) |

データは、オリジナルのword2vecフォーマットに従っています。

学習アルゴリズム自体はv1.0とv1.1で変わりません。

「正規化」は、形態素解析器Sudachiによる表記統制です。例えば `空き缶`, `空缶`, `空き罐`, `空罐`, `空きカン`, `空きかん` はすべて正規化表記 `空き缶` に統制されます。

「最低頻度」は、コーパス内での出現回数での足切り基準（[gensim](https://radimrehurek.com/gensim/models/word2vec.html)での `min_count` ）です。

形態素解析器Sudachiのバージョンは、chiVe 1.0では [v0.1.1](https://github.com/WorksApplications/Sudachi/releases/tag/v0.1.1) 、chiVe 1.1では [v0.3.0](https://github.com/WorksApplications/Sudachi/releases/tag/v0.3.0) を使用しています。

## ライセンス

Copyright (c) 2020 National Institute for Japanese Language and Linguistics and Works Applications Co., Ltd. All rights reserved.

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)の下で[国立国語研究所](https://www.ninjal.ac.jp/)と[株式会社ワークスアプリケーションズ](https://www.worksap.co.jp/)によって提供されています。

## Slack

開発者やユーザーの方々が質問したり議論するためのSlackワークスペースを用意しています。

- https://sudachi-dev.slack.com/
- ([こちら](https://join.slack.com/t/sudachi-dev/shared_invite/enQtMzg2NTI2NjYxNTUyLTMyYmNkZWQ0Y2E5NmQxMTI3ZGM3NDU0NzU4NGE1Y2UwYTVmNTViYjJmNDI0MWZiYTg4ODNmMzgxYTQ3ZmI2OWU)から招待を受けてください)

## chiVeの引用

chiVeについて、論文を発表しています;

- 真鍋陽俊, 岡照晃, 海川祥毅, 髙岡一馬, 内田佳孝, 浅原正幸. [複数粒度の分割結果に基づく日本語単語分散表現](https://www.anlp.jp/proceedings/annual_meeting/2019/pdf_dir/P8-5.pdf). 言語処理学会第25回年次大会, 2019.
- 河村宗一郎, 久本空海, 真鍋陽俊, 高岡一馬, 内田佳孝, 岡照晃, 浅原正幸. [chiVe 2.0: SudachiとNWJCを用いた実用的な日本語単語ベクトルの実現へ向けて](https://www.anlp.jp/nlp2020/). 言語処理学会第26回年次大会, 2020.

Sudachiを論文や書籍、サービスなどで引用される際には、以下のBibTexをご利用ください。

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
