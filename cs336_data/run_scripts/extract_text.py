from cs336_data.extract import extract_text_from_warc

if __name__ == "__main__":
    warc_path = f"data/CC-MAIN-20250417135010-20250417165010-00065.warc.gz"
    num_iter = 2
    extract_text_from_warc(warc_path, num_iter)