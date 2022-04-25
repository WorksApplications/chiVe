# chiVeの追加学習

chiVeは、各ドメイン（分野）に合わせたデータで追加学習させられます。
chiVeは、追加学習なしでも利用できますが、追加学習することでそのドメイン（分野）でのタスクの性能改善が期待できます。


## Step 1. フルモデルをダウンロード

[学習させたいモデル](../README.md#追加学習用のフルモデル)を選択してダウンロードし、解凍します。

```sh
$ wget https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.2-mc90_gensim-full.tar.gz
$ tar xzvf chive-1.2-mc90_gensim-full.tar.gz
```

## Step 2. 学習コーパスの用意

分かち書きした学習コーパスが必要です。
平文データ `corpus.txt` から、分かち書きしたファイル `corpus.tok.txt` を作ります。

```bash
$ pip install sudachipy sudachidict_core
```

```py
import sudachipy

tokenizer = sudachipy.Dictionary().create()

def tokenize(sentence: str, mode: str) -> str:
    mode = {
        'A': sudachipy.Tokenizer.SplitMode.A,
        'B': sudachipy.Tokenizer.SplitMode.B,
        'C': sudachipy.Tokenizer.SplitMode.C}[mode]
    tokens = [m.normalized_form() for m in tokenizer.tokenize(sentence, mode)]
    return ' '.join(tokens)

def create_training_corpus(inputpath, outputpath):
    with open(inputpath) as inputfile, open(outputpath, 'w') as outputfile:
        for mode in ('A', 'B', 'C'):
            for line in inputfile:
                line = line.strip()
                if line == '':
                    continue
                outputfile.write(tokenize(line, mode) + '\n')
            inputfile.seek(0)

create_training_corpus('corpus.txt', 'corpus.tok.txt')
```


## Step 3. 学習

学習パラメータの詳細は、[gensim.models.word2vec.Word2Vec.train](https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.Word2Vec.train)を参照してください。

```bash
$ pip install gensim
```

```py
from gensim.models.word2vec import LineSentence
from gensim.models import Word2Vec

sentences = LineSentence('corpus.tok.txt')
model = Word2Vec.load('chive-1.2-mc90_gensim-full/chive-1.2-mc90.bin')
model.vocabulary.min_count = 3
model.build_vocab(sentences, update=True)
model.train(sentences, total_examples=model.corpus_count, epochs=15)
```

学習したモデルを保存します。

* KeyedVectors: 学習に使用するパラメータを削除した埋め込みのみのデータ形式
* Full model: 学習に使用するパラメータも保持したデータ形式

```py
model.wv.save('chive-1.2-mc90.finetuned-mc3.kv')  # Save as KeyedVectors
model.save('chive-1.2-mc90.finetuned-mc3.bin')    # Save as Full model
```
