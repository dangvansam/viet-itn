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

import pynini
from pynini.lib import pynutil

from src.inverse_text_normalization.vi.graph_utils import NEMO_NOT_QUOTE, GraphFst, delete_space


class OrdinalFst(GraphFst):
    """
    Finite state transducer for verbalizing ordinal, e.g.
       ordinal { integer: "2" } -> thứ 2
    """

    def __init__(self):
        super().__init__(name="ordinal", kind="verbalize")
        graph = (
            pynutil.delete("integer:")
            + delete_space
            + pynutil.delete('"')
            + pynini.closure(NEMO_NOT_QUOTE, 1)
            + pynutil.delete('"')
        )

        graph = pynutil.insert("thứ ") + graph
        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()
