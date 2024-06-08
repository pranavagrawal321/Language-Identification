import download_dataset
import os
import training

if not os.path.exists('datasets'):
    download_dataset.download_language_datasets()

training.train_model()