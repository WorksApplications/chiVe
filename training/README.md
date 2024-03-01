# Training chiVe

chiVe is trained using [gensim](https://radimrehurek.com/gensim/index.html) library.

## Training procedure

### 0. Setup

Install libraries with `pip install -r requirements.txt`.
Note that, for the reproducablity, the versions of Sudachi in `requirements.txt` are fixed.
If you want to use latest ones, modify them or update Sudachi.

### 1. Prepare corpus

Training a word2vec model requires a corpus.

We load the corpus using [`gensim.models.word2vec.LineSentence`](https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.LineSentence) or [`PathLineSentences`](https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.LineSentence) class.
Since they assumes that words are already preprocessed and whitespace separated, we preprocess our corpus.

Put corpus text file(s) in a directory (subdirectories are NOT searched), and run
`python prepare_corpus.py --input path/to/input_dir --output path/to/output_dir`.
This script does followings:

- Analyze input text files using Sudachi, and output each morphemes separeted by a whitespace (分かち書き/wakachi-gaki).
- Each morphemes are converted into `normalized_form` (正規化形).
- Analysis is performed 3 times, using each of Sudachi split modes (A/B/C).
  - Output 3 files per an input file.
- Analysis is performed per line.
- Words that its normalized_form is a whitespace (" ") are skiped.

Set `--skip-existing` to skip an analysis for a pair of (input file, Sudachi split mode) that already processed.
Skippableness is judged based on the existance of the output file and its line count (for the case of analysis was interrupted).

Use `--mode` to specify Sudachi split mode to use. e.g. `--mode AC` to use only mode A and C.

example:

```bash
ls -A data/raw_corpus/*.txt | xargs -L 1 -I{} -P 20 \
    python prepare_corpus.py --skip-existing \
        --input {} --output data/corpus/
```

### 2. Training

Use `train_chive.py` to run training using gensim word2vec class.
`--input` should be set the output directory of `prepare_corpus.py`.

example:

```bash
python train_chive.py \
    --input data/corpus/ --output model/full/ \
    --epochs 15 --min-count 90 \
    --save-epochs 3 --keep-ckpt 5 \
    --worker 16
```

chiVe ~v1.3 are trained 15 epochs with following parameters.

```json
{
  "vector_size": 300,
  "window": 8,
  "sg": 1,
  "hs": 0,
  "n_negative": 5,
  "threshold_downsample": 1e-5,
  "alpha": 0.025,
  "min_alpha": 0.0001
}
```

You can resume training from a checkpoint saved (auto detect from the output directory).
You should resume with same parameters and corpus, otherwise the result may not be an expected one.
Note that resuming a training is not the feature of gensim, and may contain some error on precision.

### 3. Convert to distribution formats

Trained (full) model contains values for update model parameters, that is not neccessary for querying.
Use `convert_model_format.py` to generate text and `gensim.KeyedVectors` format for the distribution.

example:

```bash
python convert_model_format.py \
    --input model/full/ --output model/release/
```

[magnitude](https://github.com/plasticityai/magnitude) does not seems to be maintained, so we stop to distribute in that format from chiVe v1.3.
