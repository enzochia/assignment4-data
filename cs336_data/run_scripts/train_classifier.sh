uv run --active -m cs336_data.quality_classifier.train_classifier \
  --path_input data/training_data.shuffled.txt \
  --path_output data/quality_classifier.bin \
  --epoch 32 \
  --lr 0.1 \
  --wordNgrams 3