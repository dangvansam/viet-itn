# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright 2015 and onwards Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pynini
from pynini.lib import pynutil

from src.inverse_text_normalization.vi.graph_utils import (
    NEMO_DIGIT,
    GraphFst,
    convert_space,
    delete_extra_space,
    delete_space,
    generator_main,
)
from src.inverse_text_normalization.vi.utils import get_abs_path
from src.inverse_text_normalization.vi.taggers.cardinal import CardinalFst
from src.inverse_text_normalization.vi.taggers.date import DateFst
from src.inverse_text_normalization.vi.taggers.decimal import DecimalFst, get_quantity
from src.inverse_text_normalization.vi.taggers.electronic import ElectronicFst
from src.inverse_text_normalization.vi.taggers.fraction import FractionFst
from src.inverse_text_normalization.vi.taggers.measure import MeasureFst
from src.inverse_text_normalization.vi.taggers.money import MoneyFst
from src.inverse_text_normalization.vi.taggers.ordinal import OrdinalFst
from src.inverse_text_normalization.vi.taggers.punctuation import PunctuationFst
from src.inverse_text_normalization.vi.taggers.telephone import TelephoneFst
from src.inverse_text_normalization.vi.taggers.time import TimeFst
from src.inverse_text_normalization.vi.taggers.whitelist import WhiteListFst
from src.inverse_text_normalization.vi.taggers.word import WordFst
from nemo_text_processing.text_normalization.en.graph_utils import INPUT_LOWER_CASED
from nemo_text_processing.utils.logging import logger


class ClassifyFst(GraphFst):
    """
    Composite FST that tokenizes and classifies entire sentences.
    Uses updated CardinalFst, MoneyFst, DecimalFst with quantity support.
    """

    def __init__(
        self,
        cache_dir: str = None,
        overwrite_cache: bool = False,
        whitelist: str = None,
        input_case: str = INPUT_LOWER_CASED,
    ):
        super().__init__(name="tokenize_and_classify", kind="classify")

        far_file = None
        if cache_dir and cache_dir != "None":
            os.makedirs(cache_dir, exist_ok=True)
            far_file = os.path.join(cache_dir, f"vi_itn_{input_case}.far")

        if not overwrite_cache and far_file and os.path.exists(far_file):
            self.fst = pynini.Far(far_file, mode="r")["tokenize_and_classify"]
            logger.info(f"ClassifyFst.fst restored from {far_file}.")
        else:
            logger.info("Creating updated ClassifyFst grammars.")
            # Instantiate tagging FSTs
            cardinal = CardinalFst()
            fraction = FractionFst(cardinal)
            ordinal = OrdinalFst()
            decimal = DecimalFst(cardinal)
            measure = MeasureFst(cardinal=cardinal, decimal=decimal)
            date = DateFst(cardinal=cardinal)
            word = WordFst()
            time = TimeFst()
            money = MoneyFst(cardinal=cardinal, decimal=decimal)
            whitelist_fst = WhiteListFst(input_file=whitelist)
            punct = PunctuationFst()
            electronic = ElectronicFst()
            telephone = TelephoneFst()

            # Collect weighted unions
            classify = (
                pynutil.add_weight(whitelist_fst.fst, 1.01)
                | pynutil.add_weight(time.fst, 1.05)
                | pynutil.add_weight(money.fst, 1.03)
                | pynutil.add_weight(telephone.fst, 1.04)
                | pynutil.add_weight(date.fst, 1.09)
                | pynutil.add_weight(decimal.fst, 1.08)
                | pynutil.add_weight(measure.fst, 1.1)
                | pynutil.add_weight(cardinal.fst, 1.1)
                | pynutil.add_weight(ordinal.fst, 1.1)
                | pynutil.add_weight(fraction.fst, 1.09)
                | pynutil.add_weight(electronic.fst, 1.1)
                | pynutil.add_weight(word.fst, 100)
            )

            punct_graph = pynutil.insert("tokens { ") + pynutil.add_weight(punct.fst, 1.1) + pynutil.insert(" }")
            token_graph = pynutil.insert("tokens { ") + classify + pynutil.insert(" }")
            token_plus_punct = (
                pynini.closure(punct_graph + delete_space)
                + token_graph
                + pynini.closure(delete_space + punct_graph)
            )

            # Full sentence grammar
            graph = token_plus_punct + pynini.closure(delete_extra_space + token_plus_punct)
            graph = delete_space + graph + delete_space
            self.fst = graph.optimize()

            # Write FAR cache if requested
            if far_file:
                generator_main(far_file, {"tokenize_and_classify": self.fst})