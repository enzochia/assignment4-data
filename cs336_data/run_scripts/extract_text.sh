uv run --active -m cs336_data.extract.extract_text \
  --path_input data/positive_samples_unfiltered_5000urls.warc.gz \
  --path_output data/positive_samples_filtered_5000urls.txt \
  --max_records 1000000 \
  --print_every 2000 \
  --language en \
  --language_threshold 0.0 \
  --non_nsfw_threshold 0.5 \
  --non_toxic_threshold 0.5 \
  --positive_examples


uv run --active -m cs336_data.extract.extract_text \
  --path_input data/CC-MAIN-20250417135010-20250417165010-00065.warc.gz \
  --path_output data/negative_samples_filtered_10000records.txt \
  --max_records 10000 \
  --print_every 2000 \
  --language en \
  --language_threshold 0.0 \
  --non_nsfw_threshold 0.5 \
  --non_toxic_threshold 0.5 

awk '{print "__label__positive " $0}' data/positive_samples_filtered_5000urls.txt > data/training_data.txt
awk '{print "__label__negative " $0}' data/negative_samples_filtered_10000records.txt >> data/training_data.txt
shuf data/training_data.txt -o data/training_data.shuffled.txt