import os
from nemo_text_processing.inverse_text_normalization import InverseNormalizer

class InverseTextNormalizer:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.invert_text_normalizer = InverseNormalizer(lang='vi', cache_dir=dir_path + "/cache")

    def inverse_normalize(self, text: str, verbose=False) -> str:
        return self.invert_text_normalizer.inverse_normalize(text, verbose=verbose)
