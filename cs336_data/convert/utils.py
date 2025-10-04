import os
import gzip
from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import detect_encoding
from fastwarc.warc import ArchiveIterator, WarcRecordType

def extract_text(raw_html_bytes: bytes) -> str:
    encoding = detect_encoding(raw_html_bytes)
    raw_html_str = raw_html_bytes.decode(encoding, errors="replace")
    text = extract_plain_text(raw_html_str)
    return text


def extract_text_from_warc(
    path: str | os.PathLike,
    num_iter: int
) -> None:
    count = 0
    with gzip.open(path, "rb") as f:
        for record in ArchiveIterator(f):
            if ((record.record_type == WarcRecordType.response) and
                (record.content_length > 0)):
                text = extract_text(record.reader.read())
                print(f"################################# non-empty response #{count} #################################")
                print(text)
                count += 1
                if count == num_iter:
                    break