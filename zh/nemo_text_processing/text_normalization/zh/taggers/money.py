#!/usr/bin/env python3
# coding=utf-8
import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst, insert_space,NEMO_DIGIT
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from pynini.lib import pynutil
class MoneyFst(GraphFst):
    '''
        ￥1.25 --> 一点二五元
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="number", kind="classify", deterministic=deterministic)
        currency_graph = pynini.invert(pynini.string_file(get_abs_path("data/money/currency.tsv")))
        digit_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/digit.tsv")))
        self.fst = ' ' + NumberFst().final_graph + currency_graph

