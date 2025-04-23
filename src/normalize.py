import os
import pynini
from pynini.lib.rewrite import top_rewrite

class InverseTextNormalizer:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        reader_classifier = pynini.Far(os.path.join(dir_path, "far/classify/tokenize_and_classify.far"))
        reader_verbalizer = pynini.Far(os.path.join(dir_path, "far/verbalize/verbalize.far"))
        self.classifier = reader_classifier.get_fst()
        self.verbalizer = reader_verbalizer.get_fst()
        
    def inverse_normalize(self, s: str, verbose=False) -> str:
        token = top_rewrite(s, self.classifier)
        if verbose:
            print(f"Tokenized: {token}")
        return top_rewrite(token, self.verbalizer)
