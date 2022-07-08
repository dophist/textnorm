#!/usr/bin/env python3
# coding=utf-8
import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst, insert_space
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class MoneyFst(GraphFst):
    '''
        ￥1.25 --> 一点二五元
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="number", kind="classify", deterministic=deterministic)
        currency_graph = pynini.string_file(get_abs_path("data/money/currency.tsv"))
        self.fst = pynutil.insert("f") + currency_graph


