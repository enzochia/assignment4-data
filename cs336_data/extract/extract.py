import os
import gzip
from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import detect_encoding
from fastwarc.warc import ArchiveIterator, WarcRecordType
from cs336_data.quality_classifier import (
    identify_language,
    mask_pii,
    identify_harmful_content,
    gopher_quality_filter
)


def extract_text(raw_html_bytes: bytes) -> str:
    encoding = detect_encoding(raw_html_bytes)
    raw_html_str = raw_html_bytes.decode(encoding, errors="replace")
    text = extract_plain_text(raw_html_str)
    return text


def extract_text_from_warc(
    path_input: str | os.PathLike, 
    path_output: str | os.PathLike, 
    max_records: int = 1e5,
    print_every: int = 1e4,
    language: str = "en",
    language_threshold: float = 0.75,
    non_nsfw_threshold: float = 0.75,
    non_toxic_threshold: float = 0.75,
    positive_examples: bool = True
) -> None:
    extracted_count = 0
    passed_count = 0
    extracted_text_list = []
    with gzip.open(path_input, "rb") as f:
        for record in ArchiveIterator(f):
            extracted_count += 1
            if extracted_count % print_every == 0:
                print(f"Extracting and filtering {extracted_count}th record.")
            if ((record.record_type == WarcRecordType.response) and
                (record.content_length > 0)):
                text = extract_text(record.reader.read())
                language_label, language_prob = identify_language(text)
                if ((language_label != language) or
                    (language_prob < language_threshold)):
                    continue
                text, _ = mask_pii(text)
                nsfw_label, non_nsfw_prob = identify_harmful_content(text)
                if ((nsfw_label != "non-nsfw") or
                    (non_nsfw_prob < non_nsfw_threshold)):
                    continue
                toxic_label, non_toxic_prob = identify_harmful_content(text, "hatespeech")
                if ((toxic_label != "non-toxic") or
                    (non_toxic_prob < non_toxic_threshold)):
                    continue
                if (positive_examples and
                    (not gopher_quality_filter(text))):
                    continue
                extracted_text_list.append(text)
                passed_count += 1
                if passed_count == max_records:
                    break
    print(f"{passed_count} out of {extracted_count} extracted records passed the quality filters.")
    with open(path_output, "w") as f:
        for text_line in extracted_text_list:
            f.write(text_line + "\n")