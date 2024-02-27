
import numpy as np
from scipy.spatial import distance

import sudachipy


def cos_sim(v1, v2):
    return 1.0 - distance.cosine(v1, v2)


def get_zero_vector(dim, eps=1e-8):
    return eps * np.ones(dim)


def build_tokenizer(tok_name, config):
    if tok_name == 'sudachi':
        tok = SudachiTokenizer(config.get("mode", "C"),
                               config.get("dic-name", None),
                               config.get("form", "surface"))
        return tok
    else:
        raise ValueError("Invalid Tokenizer Name: {}".format(tok_name))


class SudachiTokenizer():
    def __init__(self, mode=sudachipy.SplitMode.C, dic_name=None, form="surface"):
        mode = mode if type(mode) == sudachipy.SplitMode \
            else self._str2mode(mode)
        self._name = f"sudachipy_{dic_name}_{self._mode2str(mode)}"

        dic_name = "core" if dic_name is None else dic_name
        self._tok = sudachipy.Dictionary(dict_type=dic_name).create(mode=mode)

        assert form in ["surface",
                        "normalized"], f"Invalid form for sudachi: {form}."
        self.form = form
        return

    def get_name(self) -> str:
        return self._name

    def tokenize(self, sent):
        return self._tok.tokenize(sent)

    def wakati(self, sent):
        ms = self.tokenize(sent)
        match self.form:
            case "surface": return [m.surface() for m in ms]
            case "normalized": return [m.normalized_form() for m in ms]
            case _: raise RuntimeError(f"unknown sudachi form: {self.form}")

    @staticmethod
    def _str2mode(modestr: str) -> sudachipy.SplitMode:
        """parse sudachipy.SplitMode from str"""
        match modestr.strip():
            case "A" | "a": return sudachipy.SplitMode.A
            case "B" | "b": return sudachipy.SplitMode.B
            case "C" | "c": return sudachipy.SplitMode.C
            case _: raise ValueError(f"cannot parse {modestr} as SplitMode.")

    @staticmethod
    def _mode2str(mode: sudachipy.SplitMode) -> str:
        """convert sudachipy.SplitMode into str"""
        match mode:
            case sudachipy.SplitMode.A: return "A"
            case sudachipy.SplitMode.B: return "B"
            case sudachipy.SplitMode.C: return "C"
