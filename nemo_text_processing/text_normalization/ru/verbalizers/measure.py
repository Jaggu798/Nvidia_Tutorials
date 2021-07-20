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

from nemo_text_processing.text_normalization.en.graph_utils import GraphFst
from nemo_text_processing.text_normalization.ru.alphabet import RU_ALPHA

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False


class MeasureFst(GraphFst):
    """
    Finite state transducer for verbalizing measure, e.g.
        measure { negative: "true" cardinal { integer: "twelve" } units: "kilograms" } -> minus twelve kilograms
        measure { decimal { integer_part: "twelve" fractional_part: "five" } units: "kilograms" } -> twelve point five kilograms
        tokens { measure { units: "covid" decimal { integer_part: "nineteen"  fractional_part: "five" }  } } -> covid nineteen point five
    
    Args:
        deterministic: if True will provide a single transduction option,
            for False multiple transduction are generated (used for audio-based normalization)
    """

    def __init__(self, deterministic: bool = True):
        super().__init__(name="measure", kind="verbalize", deterministic=deterministic)

        graph = pynini.closure(RU_ALPHA | " ")
        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()