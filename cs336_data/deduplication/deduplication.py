import os
import mmh3
import re
import unicodedata
import shutil
import numpy as np
from typing import List, Set, Dict

PAT_PUNCTUATION = re.compile(r"[^a-zA-Z0-9\s]")
PAT_SPACE = re.compile(r"\s+")

def exact_line_deduplicate(
    path_input_list: List[str | os.PathLike],
    path_output: str | os.PathLike
) -> None:
    line_counter = {}
    for path_input in path_input_list:
        with open(path_input, "r") as f:
            for line in f:
                line_hash = mmh3.hash(line)
                line_counter.setdefault(line_hash, 0)
                line_counter[line_hash] += 1
    for path_input in path_input_list:
        file_name = os.path.basename(path_input)
        with open(os.path.join(path_output, file_name), "w") as f_out:
            with open(path_input, "r") as f_in:
                for line in f_in:
                    line_hash = mmh3.hash(line)
                    if line_counter.get(line_hash, 0) == 1:
                        f_out.write(line)


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(PAT_PUNCTUATION, " ", text)
    text = re.sub(PAT_SPACE, " ", text).strip()
    # removes accents
    text = unicodedata.normalize("NFD", text)
    return text


def get_minhash(
    ngram_bag: Set[str],
    num_hashes: int
) -> List[int]:
    minhash_list = [min(mmh3.hash(ngram, seed=seed_i) for ngram in ngram_bag)
                    for seed_i in range(num_hashes)]
    return minhash_list

def get_ngram_bags(
    path_input_set: Set[str | os.PathLike],
    n_gram: int
) -> Dict[str | os.PathLike, Set[str]]:
    ngram_bag_dict = {}
    for path_input in path_input_set:
        with open(path_input, "r") as f:
            text = f.read()
        text = normalize(text)
        word_list = text.split(" ")
        ngram_bag = set(
            " ".join(word_list[idx:(idx + n_gram)])
            for idx in range(len(word_list) - n_gram + 1)
        )
        ngram_bag_dict[path_input] = ngram_bag
    return ngram_bag_dict


def get_signature(
    path_input: str | os.PathLike,
    num_hashes: int,
    n_gram: int
) -> List[int]:
    ngram_bag = get_ngram_bags(set([path_input]), n_gram)[path_input]
    signature = get_minhash(ngram_bag, num_hashes)
    return signature


def dedup_given_duplicated_docs_in_bands(
    path_input_list: List[str | os.PathLike],
    duplicate_file_list: List[Set[str | os.PathLike]],
    n_gram: int,
    jaccard_threshold: float
) -> Set[str | os.PathLike]:
    path_input_set = set(path_input_list)
    for dup_file_set in duplicate_file_list:
        ngram_bag_dict = get_ngram_bags(dup_file_set, n_gram)
        dedup_file_list = []
        for file in dup_file_set:
            if not dedup_file_list:
                dedup_file_list.append(file)
            else:
                for dedup_file in dedup_file_list:
                    jaccard_score = len(ngram_bag_dict[file].intersection(ngram_bag_dict[dedup_file])) / \
                                    len(ngram_bag_dict[file].union(ngram_bag_dict[dedup_file]))
                    if jaccard_score > jaccard_threshold:
                        path_input_set.discard(file)
    return path_input_set

def minhash_deduplicate(
    path_input_list: List[str | os.PathLike],
    num_hashes: int,
    num_lsh_bands: int,
    n_gram: int,
    jaccard_threshold: float,
    path_output: str | os.PathLike
) -> None:
    signature_dict = {}
    for path_input in path_input_list:
        signature_dict[path_input] = get_signature(path_input, num_hashes, n_gram)
    band_size = num_hashes // num_lsh_bands
    band_dict = {}
    for file, signature in signature_dict.items():
        for band in range(num_lsh_bands):
            signature_band = tuple([band] + signature[((band - 1) * band_size):(band * band_size)])
            band_dict.setdefault(signature_band, set([])).add(file)

    duplicate_file_list = []
    for signature_band in band_dict:
        if len(band_dict[signature_band]) > 1:
            duplicate_file_list.append(band_dict[signature_band])

    path_input_set = dedup_given_duplicated_docs_in_bands(path_input_list, duplicate_file_list, 
                                                          n_gram, jaccard_threshold)
    for file in path_input_set:
        shutil.copy2(file, os.path.join(path_output, os.path.basename(file)))