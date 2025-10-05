import os
import re
import fasttext
from typing import Tuple, Any, List


LANGUAGE_IDENTIFY_MODEL = fasttext.load_model(f"data/lid.176.bin")
HARMFUL_CONTENT_IDENTIFY_MODEL = {
    "nsfw": fasttext.load_model(f"data/jigsaw_fasttext_bigrams_nsfw_final.bin"),
    "hatespeech": fasttext.load_model(f"data/jigsaw_fasttext_bigrams_hatespeech_final.bin")
}
PAT_DICT = {
    "email": {
        "pattern": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
        "replacement": "|||EMAIL_ADDRESS|||"
    },
    "phone_number": {
        "pattern": re.compile(r"(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"),
        "replacement": "|||PHONE_NUMBER|||"
    },
    "ip": {
        "pattern": re.compile(r"((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}"),
        "replacement": "|||IP_ADDRESS|||"
    }
}

def identify_language(
    text: str,
    model: Any = LANGUAGE_IDENTIFY_MODEL
) -> Tuple[str, float]:
    labels, probs = model.predict("".join(text.split()), k=1)
    return labels[0][9:], probs[0]


def mask_pii(
    text: str,
    to_mask: List[str] = ["email", "phone_number", "ip"]
) -> str:
    """
    Masks emails, phone numbers, and IP addresses
    """
    for mask_item in to_mask:
        text, num_masked = re.subn(PAT_DICT[mask_item]["pattern"], 
                                   PAT_DICT[mask_item]["replacement"], 
                                   text)
    return text, num_masked


def identify_harmful_content(
    text: str,
    to_identify: str = "nsfw"
) -> Tuple[str, float]:
    text = text.replace('\n', ' ').lower()
    labels, probs = HARMFUL_CONTENT_IDENTIFY_MODEL[to_identify].predict(text)
    return labels[0][9:], probs[0]


def gopher_quality_filter(text: str) -> bool:
    word_list = re.findall(r"\b\w[\w']*\b", text)
    line_list = text.splitlines()
    is_high_quality = True
    is_high_quality = is_high_quality and (50 <= len(word_list) <= 100000)
    mean_len = sum(map(len, word_list)) / len(word_list)
    is_high_quality = is_high_quality and (3 <= mean_len <= 10)
    portion_with_one_char = sum(map(lambda x: 1 if re.search(r"[A-Za-z]", x) is not None else 0, word_list)) / len(word_list)
    is_high_quality = is_high_quality and (0.8 <= portion_with_one_char)
    portion_end_with_ellipsis = sum(map(lambda x: x[-3:] != "...", line_list)) / len(line_list)
    is_high_quality = is_high_quality and (0.3 < portion_end_with_ellipsis)
    return is_high_quality
