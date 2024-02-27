
from manalib.text.maout import get_result_from_mecab_guess, SudachiResult
from pathlib2 import Path

from dataset.base import BaseDataset, BaseInstance


class TextClassificationDataset(BaseDataset):
    def __init__(self, samples, label_name=None, name=None):
        super(TextClassificationDataset, self).__init__(samples, name)
        self.label_name = label_name

    def get_xys(self):
        xs = [b[0].word_list for b in self.batch_iter(1, rand_flg=False)]
        ys = [b[0].gold for b in self.batch_iter(1, rand_flg=False)]
        return xs, ys

    @staticmethod
    def build(docs, label_ids, label_name=False):
        """
        args:
            - docs (list<list<srt>>): documents
            - label_ids (list<int>): labels
            - label_name (list<str>): label names
        """
        assert len(docs) == len(label_ids), "Inconsistent length: {} != {}" \
               .format(len(docs), len(label_ids))
        insts = [TextClassificationInstance(d, l) \
                 for (d, l) in zip(docs, label_ids)]
        return TextClassificationDataset(samples=insts, label_name=label_name)


class TextClassificationInstance(BaseInstance):
    def __init__(self, word_list, label_id):
        """
        args:
            - word_list (list<str>): word sequence
            - label_id (int): label id
        """
        super(TextClassificationInstance, self).__init__()
        assert type(word_list) == list
        assert type(label_id) == int
        self.word_list = word_list
        self.gold = label_id

    def get_content(self):
        return (self.word_list, self.gold)


def build_doc_classification_dataset(name, dir_path, process_config):
    if name == "livedoor":
        txt_xs, ys = build_livedoor(dir_path, process_config)
    else:
        raise ValueError()
    dat = TextClassificationDataset.build(txt_xs, ys)
    return dat


def build_livedoor(dir_path, process_config):
    LIVEDOOR_LABEL_LIST = ["dokujo-tsushin", "kaden-channel", "movie-enter", \
                           "smax", "topic-news", "it-life-hack", \
                           "livedoor-homme", "peachy", "sports-watch"]
    pre_tokenized = process_config["pre-tokenized"]
    if pre_tokenized == False:
        # build toknizer
        raise NotImplementedError("Not available now")
    else:
        tok = None
    base = Path(dir_path)
    label_names = []
    txt_xs = []
    for label_dir in sorted(base.glob("*")):
        label_name = label_dir.name
        assert label_name in LIVEDOOR_LABEL_LIST, "Invalid label directory"
        for doc_path in sorted(label_dir.glob("*")):  # get document files
            if pre_tokenized == True:
                doc = load_doc(doc_path, process_config)
            else:
                raise NotImplementedError()
                doc = tokenize_doc(doc_path, tok)
            txt_xs.append(doc)
            label_names.append(label_name)
    assert len(txt_xs) == len(label_names), "Inconsistent length"
    ys = [LIVEDOOR_LABEL_LIST.index(n) for n in label_names]
    return txt_xs, ys


def load_doc(doc_path, process_config):
    tok_name = process_config["tokenizer"]["name"]
    if tok_name == "sudachi":
        morphs = SudachiResult.get_result_from_file(doc_path, is_flat=True)
    elif tok_name == "mecab":
        morphs = get_result_from_mecab_guess(doc_path, is_flat=True)

    used_pos = process_config["used-pos"]
    if used_pos == 'all':
        return [m.surface() for m in morphs]
    else:
        return [m.surface() for m in morphs if m.part_of_speech() in used_pos]
