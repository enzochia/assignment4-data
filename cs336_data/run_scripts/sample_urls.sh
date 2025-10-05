uv run --active -m cs336_data.quality_classifier.sample_urls \
  --path_input data/enwiki-20240420-extracted_urls.txt \
  --path_output data/enwiki-20240420-extracted_url_5000sample.txt \
  --max_lines 5000 \
  --max_iters 100000 \
  --print_every 10000