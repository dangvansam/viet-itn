from pynini.lib.rewrite import top_rewrite
import pynini
import os


def inverse_normalize(s: str, verbose=False) -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    reader_classifier = pynini.Far(os.path.join(dir_path, "far/classify/tokenize_and_classify.far"))
    reader_verbalizer = pynini.Far(os.path.join(dir_path, "far/verbalize/verbalize.far"))
    classifier = reader_classifier.get_fst()
    verbalizer = reader_verbalizer.get_fst()
    token = top_rewrite(s, classifier)
    if verbose:
        print(f"Tokenized: {token}")
    return top_rewrite(token, verbalizer)
