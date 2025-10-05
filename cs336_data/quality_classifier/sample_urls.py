import argparse
from .utils import sample_lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_input", type=str, default="data/enwiki-20240420-extracted_urls.txt")
    parser.add_argument("--path_output", type=str, default="data/enwiki-20240420-extracted_url_sample.txt")
    parser.add_argument("--max_lines", type=int, default=1e4)
    parser.add_argument("--max_iters", type=int, default=1e5)
    parser.add_argument("--print_every", type=int, default=1e4)
    args = parser.parse_args()
    sample_lines(**vars(args))