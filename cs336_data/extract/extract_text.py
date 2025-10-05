import argparse
from .extract import extract_text_from_warc

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_input", type=str, default="data/positive_samples_unfiltered_500urls.warc.gz")
    parser.add_argument("--path_output", type=str, default="data/positive_samples_filtered_500urls.txt")
    parser.add_argument("--max_records", type=int, default=1e6)
    parser.add_argument("--print_every", type=int, default=1e4)
    parser.add_argument("--language", type=str, default="en")
    parser.add_argument("--language_threshold", type=float, default=0.75)
    parser.add_argument("--non_nsfw_threshold", type=float, default=0.75)
    parser.add_argument("--non_toxic_threshold", type=float, default=0.75)
    parser.add_argument("--positive_examples", action="store_true")
    args = parser.parse_args()
    extract_text_from_warc(**vars(args))