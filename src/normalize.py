import os
# import pynini
import vinorm
# from pynini.lib.rewrite import top_rewrite
from src.inverse_text_normalization import InverseNormalizer

class InverseTextNormalizer:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.invert_text_normalizer = InverseNormalizer(
            lang='vi',
            cache_dir=dir_path + "/cache",
            overwrite_cache=True
        )
        # reader_classifier = pynini.Far(os.path.join(dir_path, "far/classify/tokenize_and_classify.far"))
        # reader_verbalizer = pynini.Far(os.path.join(dir_path, "far/verbalize/verbalize.far"))
        # self.classifier = reader_classifier.get_fst()
        # self.verbalizer = reader_verbalizer.get_fst()

    def normalize(self, text: str, verbose=False) -> str:
        return vinorm.TTSnorm(text)
    
    def inverse_normalize(self, text: str, verbose=False) -> str:
        return self.invert_text_normalizer.inverse_normalize(text, verbose=verbose)


if __name__ == "__main__":
    inverse_normalizer = InverseTextNormalizer()
    texts = [
        "tổng chi phí là một triệu hai trăm hai mươi hai nghìn đồng",
        "khi giá vàng lên cao kỷ lục một trăm hai mươi năm triệu đồng/lượng ở chiều bán người dân đổ xô đến cửa hàng",
        "khi giá vàng lên cao kỷ lục một hai năm triệu đồng/lượng ở chiều bán người dân đổ xô đến cửa hàng",
        "anh ta vay năm trăm tám bốn triệu",
        "tôi nhận của anh hà bên kỹ thuật điện số tiền là năm bốn hai triệu",
        "Anh ta vay năm trăm linh năm triệu không trăm linh năm nghìn không trăm linh năm đồng vào năm một chín chín chín và trả dần trong hai mươi lăm năm rưỡi, mỗi tháng hai mươi mốt triệu không trăm linh một nghìn đồng, chưa tính lãi một phẩy năm phần trăm mỗi năm.",
        "khi giá vàng lên cao kỷ lục một trăm hai mươi năm triệu đồng/lượng ở chiều bán người dân đổ xô đến cửa hàng",
        "chuyên gia tài chính cho thấy sáu mươi ba phần trăm tin rằng giá vàng sẽ tiếp tục đi lên trong tuần này trong khi chỉ hai mươi năm phần trăm dự báo giảm và mười hai phần trăm cho rằng giá sẽ đi ngang",
        "đuôi số điện thoại của tôi là năm tám năm năm",
        "đuôi số điện thoại của tôi là năm tám năm hai",
        "nghị định số tám mươi hai năm hai nghìn mười nđ-cp",
        "kết thúc chuỗi ngày nghỉ lễ (từ ngày ba mươi tháng tư đến ngày bốn tháng năm) giá vàng miếng sjc được niêm yết tại một trăm mười chín phẩy ba đến một trăm hai mươi mốt phẩy ba triệu đồng mỗi lượng (mua - bán) còn giá vàng nhẫn là một trăm mười bốn đến một trăm mười sáu phẩy năm triệu đồng mỗi lượng (mua - bán)",
        "dựa trên hiến pháp năm hai nghìn không trăm linh bốn",
        "mã sản phẩm mới là hai triệu không trăm lẻ tám",
        "giá của nó là một triệu rưỡi"
    ]

    for text in texts:
        text_norm = inverse_normalizer.inverse_normalize(text, verbose=False)
        print("input :", text)
        print("output:", text_norm)