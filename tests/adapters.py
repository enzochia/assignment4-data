from __future__ import annotations

import os
from typing import Any
from cs336_data.extract import (
    extract_text
)
from cs336_data.quality_classifier import (
    identify_language,
    mask_pii,
    identify_harmful_content,
    gopher_quality_filter
)


def run_extract_text_from_html_bytes(html_bytes: bytes) -> str | None:
    return extract_text(html_bytes)


def run_identify_language(text: str) -> tuple[Any, float]:
    return identify_language(text)


def run_mask_emails(text: str) -> tuple[str, int]:
    return mask_pii(text, ["email"])


def run_mask_phone_numbers(text: str) -> tuple[str, int]:
    return mask_pii(text, ["phone_number"])


def run_mask_ips(text: str) -> tuple[str, int]:
    return mask_pii(text, ["ip"])


def run_classify_nsfw(text: str) -> tuple[Any, float]:
    return identify_harmful_content(text, "nsfw")


def run_classify_toxic_speech(text: str) -> tuple[Any, float]:
    return identify_harmful_content(text, "hatespeech")


def run_classify_quality(text: str) -> tuple[Any, float]:
    raise NotImplementedError


def run_gopher_quality_filter(text: str) -> bool:
    return gopher_quality_filter(text)


def run_exact_line_deduplication(
    input_files: list[os.PathLike], output_directory: os.PathLike
):
    raise NotImplementedError


def run_minhash_deduplication(
    input_files: list[os.PathLike],
    num_hashes: int,
    num_bands: int,
    ngrams: int,
    jaccard_threshold: float,
    output_directory: os.PathLike,
):
    raise NotImplementedError
