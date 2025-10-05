import timeit
import argparse
import fasttext
from cs336_data.extract import extract_text_from_warc

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_input", type=str, default="data/training_data.shuffled.txt")
    parser.add_argument("--path_output", type=str, default="data/quality_classifier.bin")
    parser.add_argument("--epoch", type=int, default=10)
    parser.add_argument("--lr", type=float, default=0.1)
    parser.add_argument("--wordNgrams", type=int, default=2)
    args = parser.parse_args()
    classifier = fasttext.train_supervised(
        input=args.path_input,
        epoch=args.epoch,
        lr=args.lr,
        wordNgrams=args.wordNgrams
    )
    classifier.save_model(args.path_output)
    print(f"Quality classifier saved to {args.path_output}.")