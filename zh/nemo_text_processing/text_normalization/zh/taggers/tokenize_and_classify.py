import os
import time

import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import (
    NEMO_WHITE_SPACE,
    GraphFst,
    delete_extra_space,
    delete_space,
    generator_main,
)
from nemo_text_processing.text_normalization.zh.taggers.date import DateFst
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from nemo_text_processing.text_normalization.zh.taggers.word import WordFst
from nemo_text_processing.text_normalization.zh.taggers.fraction import FractionFst
from nemo_text_processing.text_normalization.zh.taggers.percent import PercentFst
from nemo_text_processing.text_normalization.zh.taggers.sign import SignFst
from nemo_text_processing.text_normalization.zh.taggers.money import MoneyFst
from pynini.lib import pynutil

# from nemo.utils import logging


class ClassifyFst(GraphFst):
    """
    Final class that composes all other classification grammars. This class can process an entire sentence including punctuation.
    For deployment, this grammar will be compiled and exported to OpenFst Finate State Archiv (FAR) File. 
    More details to deployment at NeMo/tools/text_processing_deployment.
    
    Args:
        input_case: accepting either "lower_cased" or "cased" input.
        deterministic: if True will provide a single transduction option,
            for False multiple options (used for audio-based normalization)
        cache_dir: path to a dir with .far grammar file. Set to None to avoid using cache.
        overwrite_cache: set to True to overwrite .far files
        whitelist: path to a file with whitelist replacements
    """

    def __init__(
        self,
        input_case: str,
        deterministic: bool = True,
        cache_dir: str = None,
        overwrite_cache: bool = False,
        whitelist: str = None,
    ):
        super().__init__(name="tokenize_and_classify", kind="classify", deterministic=deterministic)

        far_file = None
        if cache_dir is not None and cache_dir != "None":
            os.makedirs(cache_dir, exist_ok=True)
            whitelist_file = os.path.basename(whitelist) if whitelist else ""
            far_file = os.path.join(
                cache_dir, f"en_tn_{deterministic}_deterministic_{input_case}_{whitelist_file}_tokenize.far"
            )
        if not overwrite_cache and far_file and os.path.exists(far_file):
            self.fst = pynini.Far(far_file, mode="r")["tokenize_and_classify"]
            # logging.info(f'ClassifyFst.fst was restored from {far_file}.')
        else:
            # logging.info(f"Creating ClassifyFst grammars.")

            start_time = time.time()
            date = DateFst(deterministic=deterministic)
            date_graph = date.fst
            number = NumberFst(deterministic=deterministic)
            number_graph = number.fst
            word = WordFst(deterministic=deterministic)
            word_graph = word.fst
            fraction = FractionFst(deterministic=deterministic)
            fraction_graph = fraction.fst
            percent = PercentFst(deterministic=deterministic)
            percent_graph = percent.fst
            sign = SignFst(deterministic=deterministic)
            sign_graph = sign.fst
            money = MoneyFst(deterministic=deterministic)
            money_graph = money.fst
            # logging.debug(f"date: {time.time() - start_time: .2f}s -- {date_graph.num_states()} nodes")

            classify = (
                pynutil.add_weight(date_graph, 0.8)               
                |pynutil.add_weight(fraction_graph,0.5)
                |pynutil.add_weight(percent_graph,0.5)
                |pynutil.add_weight(money_graph,0.5)
                |pynutil.add_weight(number_graph, 1.2)
                |pynutil.add_weight(sign_graph, 1.5)
                |pynutil.add_weight(word_graph, 200)

            )

            token = pynutil.insert("tokens { ") + classify + pynutil.insert(" }")
            graph = token
            self.fst = graph.optimize()