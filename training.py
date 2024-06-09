import logging
import utils
import os
import pandas as pd
import fasttext

os.makedirs("models", exist_ok=True)


def create_fasttext_data(data):
    utils.writeLog("Creating fasttext model", logging.INFO)
    with open('fasttext_dataset.txt', 'w', encoding='utf-8') as f:
        for index, row in data.iterrows():
            text = row['text']
            language = row['language']
            f.write(f'__label__{language} {text}\n')
    utils.writeLog("Fasttext model created", logging.INFO)


def train_model():
    if not os.path.isfile("Languages.csv"):
        utils.writeLog("Languages.csv not found. Generating Languages.csv", logging.INFO)
        utils.create_final_dataset()
        utils.writeLog("Languages.csv generated", logging.INFO)

    data = pd.read_csv('Languages.csv')
    create_fasttext_data(data)
    training_data_path = 'fasttext_dataset.txt'
    model_save_path = 'models/fasttext_finetuned.bin'
    utils.writeLog("Training model", logging.INFO)
    model = fasttext.train_supervised(input=training_data_path, epoch=100, lr=1.0)
    model.save_model(model_save_path)
    os.remove(training_data_path)
    utils.writeLog("Model saved", logging.INFO)