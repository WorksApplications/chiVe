
import itertools
from pathlib import Path

from dataset.base import BaseDataset, BaseInstance
from utils import build_tokenizer


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
        insts = [TextClassificationInstance(d, l)
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
    LIVEDOOR_LABEL_LIST = ["dokujo-tsushin", "kaden-channel", "movie-enter",
                           "smax", "topic-news", "it-life-hack",
                           "livedoor-homme", "peachy", "sports-watch"]
    pre_tokenized = process_config["pre-tokenized"]
    tok = None if pre_tokenized else build_tokenizer(
        process_config["tokenizer"]["name"], process_config["tokenizer"]["others"])

    base = Path(dir_path)
    label_names = []
    txt_xs = []
    for label_dir in sorted(base.glob("*")):
        if not label_dir.is_dir():
            continue
        label_name = label_dir.name
        assert label_name in LIVEDOOR_LABEL_LIST, "Invalid label directory"
        for doc_path in sorted(label_dir.glob("*.txt")):  # get document files
            if pre_tokenized == True:
                raise NotImplementedError()
            else:
                doc = tokenize_doc(doc_path, tok, process_config)
            txt_xs.append(doc)
            label_names.append(label_name)
    assert len(txt_xs) == len(label_names), "Inconsistent length"
    ys = [LIVEDOOR_LABEL_LIST.index(n) for n in label_names]
    return txt_xs, ys


def tokenize_doc(doc_path, tok, process_config):
    ms = []
    with Path(doc_path).open() as fi:
        for l in fi:
            ms.append(tok.tokenize(l))
    ms = itertools.chain.from_iterable(ms)

    if (used_pos := process_config["used-pos"]) != "all":
        ms = (m for m in ms if m.part_of_speech()[0] in used_pos)

    match (form := process_config["tokenizer"]["others"]["form"]):
        case "surface": return [m.surface() for m in ms]
        case "normalized": return [m.normalized_form() for m in ms]
        case _: raise ValueError(f"invalid tokenizer form: {form}")
