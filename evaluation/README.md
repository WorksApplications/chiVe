# Evaluation of word vectors

See following paper for the detail.

- 真鍋陽俊, 岡照晃, 海川祥毅, 髙岡一馬, 内田佳孝, 浅原正幸. [複数粒度の分割結果に基づく日本語単語分散表現](https://www.anlp.jp/proceedings/annual_meeting/2019/pdf_dir/P8-5.pdf). 言語処理学会第 25 回年次大会, 2019.

## Setup

Download datasets.
The default task setting files (`resources/**/*.yaml`) assume datasets are located under `data/`, otherwise you need to modify it.

Download word vectors, and set the path in the vec setting file (`resources/vec/*.yaml`).
The default vec setting assumes to use `gensim.KeyedVector` format.

Install modules by `pip install -r requirements.txt`.

## Tasks

### Word similarity

Calculate the Spearman rank-order correlation coefficient between human annotated similarity and word vectors.

- Similarity of word vectors are measured by cosine-similariry.
- If a target word consists of multiple (sudachi) words, we use an average vector of each (sudachi) words.

We used following datasets:

- [JWSEN](http://www.utm.inf.uec.ac.jp/JWSAN/index.html)
  - Download jwsan.zip, unzip and place under `data/`
- [Japanese Word Similarity Dataset](https://github.com/tmu-nlp/JapaneseWordSimilarityDataset) (JWSD)
  - Clone the repository under `data/`

commands:

```bash
# JWSEN
python run_wordsim.py \
    --tconfig resources/sim/jwsen.yaml \
    --vconfig resources/vec/chive-1.3-mc90-sudachic.yaml

# JWSD
python run_wordsim.py \
    --tconfig resources/sim/tmu-sudachic.yaml \
    --vconfig resources/vec/chive-1.3-mc90-sudachic.yaml
```

### Document classification

Train classifier using word vector as a feature vector.

- Document vector is calculated by averaging word vectors of nouns in the document.
- LogisticRegression is used as a classifier.
- We conduct 10-fold cross validation.

We used following datasets:

- [livedoor news corpus](https://www.rondhuit.com/download.html#ldcc)
  - Download ldcc-20140209.tar.gz, untar and place under `data/`

commands:

```bash
# livedoor news corpus
python run_docclf.py \
    --tconfig resources/clf/livedoor-sudachic.yaml \
    --vconfig resources/vec/chive-1.3-mc30-sudachic.yaml
```

## Results

| version   | jwsan-1400 類似度 | jwsan-1400 関連度 | jwsd-verb | jwsd-adj | jwsd-noun | jwsd-adv | livedoor-acc   |
| --------- | ----------------- | ----------------- | --------- | -------- | --------- | -------- | -------------- |
| v1.3 mc5  | 0.493             | 0.626             | 0.309     | 0.459    | 0.351     | 0.231    | 0.862+1.46e-4  |
| v1.3 mc15 | 0.492             | 0.627             | 0.318     | 0.465    | 0.354     | 0.239    | 0.860+1.48e-4  |
| v1.3 mc30 | 0.496             | 0.626             | 0.318     | 0.459    | 0.354     | 0.250    | 0.859+1.23e-4  |
| v1.3 mc90 | 0.493             | 0.622             | 0.324     | 0.460    | 0.344     | 0.261    | 0.857+1.55e-4  |
|           |                   |                   |           |          |           |          |                |
| v1.2 mc5  | 0.520             | 0.633             | 0.316     | 0.466    | 0.355     | 0.297    | 0.865+0.436e-4 |
| v1.2 mc15 | 0.513             | 0.629             | 0.315     | 0.461    | 0.353     | 0.294    | 0.862+0.710e-4 |
| v1.2 mc30 | 0.515             | 0.631             | 0.311     | 0.458    | 0.354     | 0.289    | 0.860+0.546e-4 |
| v1.2 mc90 | 0.512             | 0.627             | 0.307     | 0.463    | 0.345     | 0.281    | 0.861+0.778e-4 |

## NOTE

- Current implementation uses zero-vector for OOV words and cosine-similarity with zero-vector is 1.0.
  This may affect the evaluation result.
