from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst
from nemo_text_processing.text_normalization.zh.verbalizers.date import DateFst
from nemo_text_processing.text_normalization.zh.verbalizers.number import NumberFst
from nemo_text_processing.text_normalization.zh.verbalizers.word import WordFst
from nemo_text_processing.text_normalization.zh.verbalizers.fraction import FractionFst
from nemo_text_processing.text_normalization.zh.verbalizers.percent import PercentFst
from nemo_text_processing.text_normalization.zh.verbalizers.sign import SignFst
from nemo_text_processing.text_normalization.zh.verbalizers.money import MoneyFst
class VerbalizeFst(GraphFst):
    """
    Composes other verbalizer grammars.
    For deployment, this grammar will be compiled and exported to OpenFst Finate State Archiv (FAR) File. 
    More details to deployment at NeMo/tools/text_processing_deployment.
    Args:
        deterministic: if True will provide a single transduction option,
            for False multiple options (used for audio-based normalization)
    """

    def __init__(self, deterministic: bool = True):
        super().__init__(name="verbalize", kind="verbalize", deterministic=deterministic)
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
        graph = ( 
        	date_graph
            |number_graph
            |fraction_graph
            |word_graph
            |sign_graph
            |percent_graph
            |money_graph
        )
        self.fst = graph
