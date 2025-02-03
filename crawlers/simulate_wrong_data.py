import numpy as np
import re
import unicodedata
import random

accent_mapping = {
    'á': 'a', 'à': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
    'ă': 'a', 'ắ': 'a', 'ằ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
    'â': 'a', 'ấ': 'a', 'ầ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
    'é': 'e', 'è': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
    'ê': 'e', 'ế': 'e', 'ề': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
    'í': 'i', 'ì': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
    'ó': 'o', 'ò': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
    'ô': 'o', 'ố': 'o', 'ồ': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
    'ơ': 'o', 'ớ': 'o', 'ờ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
    'ú': 'u', 'ù': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
    'ư': 'u', 'ứ': 'u', 'ừ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
    'ý': 'y', 'ỳ': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    'đ': 'd',
    'Á': 'A', 'À': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
    'Ă': 'A', 'Ắ': 'A', 'Ằ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
    'Â': 'A', 'Ấ': 'A', 'Ầ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
    'É': 'E', 'È': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
    'Ê': 'E', 'Ế': 'E', 'Ề': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
    'Í': 'I', 'Ì': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
    'Ó': 'O', 'Ò': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
    'Ô': 'O', 'Ố': 'O', 'Ồ': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
    'Ơ': 'O', 'Ớ': 'O', 'Ờ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
    'Ú': 'U', 'Ù': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
    'Ư': 'U', 'Ứ': 'U', 'Ừ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
    'Ý': 'Y', 'Ỳ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
    'Đ': 'D'
}

# Bảng chuyển đổi dấu tiếng Việt
def change_accent(word):
    accent_groups = {
        'a': ['á', 'à', 'ả', 'ã', 'ạ'],
        'ă': ['ắ', 'ằ', 'ẳ', 'ẵ', 'ặ'],
        'â': ['ấ', 'ầ', 'ẩ', 'ẫ', 'ậ'],
        'e': ['é', 'è', 'ẻ', 'ẽ', 'ẹ'],
        'ê': ['ế', 'ề', 'ể', 'ễ', 'ệ'],
        'i': ['í', 'ì', 'ỉ', 'ĩ', 'ị'],
        'o': ['ó', 'ò', 'ỏ', 'õ', 'ọ'],
        'ô': ['ố', 'ồ', 'ổ', 'ỗ', 'ộ'],
        'ơ': ['ớ', 'ờ', 'ở', 'ỡ', 'ợ'],
        'u': ['ú', 'ù', 'ủ', 'ũ', 'ụ'],
        'ư': ['ứ', 'ừ', 'ử', 'ữ', 'ự'],
        'y': ['ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ'],
        'd': ['đ']
    }

    for base, accents in accent_groups.items():
        for accent in accents:
            if accent in word:
                word = word.replace(accent, random.choice(accents))
                return word

    return word

# Giả lập mất dấu tiếng Việt hoàn toàn
def remove_vietnamese_accent(text):
    # Chuẩn hóa chuỗi thành dạng Unicode tổ hợp (NFD)
    normalized_text = unicodedata.normalize('NFD', text)

    # Loại bỏ các ký tự dấu (ký tự có tổ hợp diacritics)
    non_accented_text = ''.join(
        char for char in normalized_text if unicodedata.category(char) != 'Mn'
    )

    return non_accented_text

# Bảng chuyển đổi tiếng Việt không dấu
def remove_accent_char(char):
    return accent_mapping.get(char, char)

# Hàm làm sai chính tả
def simulate_typo_vietnamese(text, error_probability=0.2):
    result = []
    for word in text.split():
        if re.search(r'\d', word):
            result.append(word)
            continue
        # Xử lý nếu từ chứa dấu câu
        if any(char in word for char in ",.?!;:()[]{}" + "\"'"):
            typo_word = make_typo_with_punctuation(word, error_probability)
            result.append(typo_word)
        else:
            # Quyết định ngẫu nhiên có làm sai từ này không
            if random.random() < error_probability:
                word = introduce_typo(word)
            result.append(word)
    return ' '.join(result)


def make_typo_with_punctuation(word, error_probability=0.2):
    # Tìm phần ký tự không phải chữ cái
    match = re.match(r"([\'\"\(\{\[]?)([a-zA-Z]+)([\'\"\)\}\]]?)", word)
    if match:
        prefix, core_word, suffix = match.groups()
        if random.random() < error_probability:
            typo_core_word = introduce_typo(core_word)
            return prefix + typo_core_word + suffix
    return word

# Hàm tạo lỗi sai ngẫu nhiên cho từ
def introduce_typo(word):
    typo_type = random.choice(['remove_accent', 'swap', 'add', 'delete', 'change_accent'])

    if typo_type == 'remove_accent':  # Bỏ dấu tiếng Việt
        word = ''.join(remove_accent_char(char) for char in word)

    elif typo_type == 'swap':  # Đảo vị trí hai ký tự ngẫu nhiên
        if len(word) > 2:
            idx = random.randint(1, len(word) - 2)
            word = word[:idx] + word[idx + 1] + word[idx] + word[idx + 2:]

    elif typo_type == 'add':  # Thêm ký tự ngẫu nhiên
        idx = random.randint(1, len(word))
        char = random.choice('abcdefghijklmnopqrstuvwxyz')
        word = word[:idx] + char + word[idx:]

    elif typo_type == 'delete':  # Xóa một ký tự ngẫu nhiên
        if len(word) > 2:
            idx = random.randint(1, len(word) - 1)
            word = word[:idx] + word[idx + 1:]

    elif typo_type == 'change_accent':  # Thay đổi dấu tiếng Việt
        word = change_accent(word)
    return word

