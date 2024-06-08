import pandas as pd
import os
import logging
import logging.handlers
import sys
import signal

os.makedirs("final", exist_ok=True)
os.makedirs("logs", exist_ok=True)

logger_name = "logs/language_detection"

logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(message)s]")

if not logger.handlers:
    handler = logging.handlers.RotatingFileHandler(logger_name + ".log", maxBytes=100 * 1024 * 1024, backupCount=10)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)


def writeLog(message, level=logging.INFO):
    """
    Write a log message to the logger.

    Parameters:
        message (str): The log message to be written.
        level (int): The log level (default: logging.INFO).
    """
    logger.log(level, message)


def get_assamese_data():
    writeLog("Reading Assamese data", logging.INFO)
    file_paths = [
        "datasets/Assamese/nenow_preprocessed.csv",
        "datasets/Assamese/news18_preprocessed.csv"
    ]

    dfs = []
    for file_path in file_paths:
        df = pd.read_csv(file_path, usecols=['summary'])
        df['language'] = "Assamese"
        dfs.append(df)

    final = pd.concat(dfs)
    final.drop_duplicates(inplace=True)
    final.rename(columns={'summary': 'text'}, inplace=True)

    output_file = os.path.join('final', 'Assamese.csv')
    writeLog("Saving Assamese data", logging.INFO)
    final.to_csv(output_file, index=False)
    return final


def get_bengali_data():
    writeLog("Reading Bengali data", logging.INFO)
    file_paths = [
        "datasets/Bengali/data/data.json",
        "datasets/Bengali/data_v2/data_v2.json"
    ]

    dfs = []
    for file_path in file_paths:
        df = pd.read_json(file_path)
        if 'title' in df.columns:
            df = df[['title']]
            df['language'] = "Bengali"
            dfs.append(df)

    writeLog("Merged Bengali data", logging.INFO)

    if dfs:
        final = pd.concat(dfs)
        final.drop_duplicates(inplace=True)
        final.rename(columns={'title': 'text'}, inplace=True)

        output_file = os.path.join('final', 'Bengali.csv')

        writeLog("Saving Bengali data", logging.INFO)

        final.to_csv(output_file, index=False)
        return final
    else:
        writeLog("No data found", logging.ERROR)
        return pd.DataFrame()


def get_english_data():
    writeLog("Reading English data", logging.INFO)
    data = pd.read_csv("datasets/English/metadata.csv", usecols=['title'])
    data.drop_duplicates(inplace=True)
    data.rename(columns={'title': 'text'}, inplace=True)
    data['language'] = 'English'
    writeLog("Saving English data", logging.INFO)
    data.to_csv('final/English.csv', index=None)
    return data


def get_gujarati_data():
    writeLog("Reading Gujarati data", logging.INFO)
    data = pd.read_csv('datasets/Gujarati/Guj_train.csv')
    data = data[['Heading']]
    data.rename(columns={'Heading': 'text'}, inplace=True)
    data['language'] = 'Gujarati'
    writeLog("Saving Gujarati data", logging.INFO)
    data.to_csv('final/Gujarati.csv', index=None)
    return data


def get_hindi_data():
    writeLog("Reading Hindi data", logging.INFO)
    data = pd.read_csv('datasets/Hindi/hindi_news_dataset.csv')
    data = data[['Headline']]
    data.drop_duplicates(inplace=True)
    data.rename(columns={'Headline': 'text'}, inplace=True)
    data['language'] = 'Hindi'
    writeLog("Saving Hindi data", logging.INFO)
    data.to_csv('final/Hindi.csv', index=None)
    return data


def get_kannada_data():
    writeLog("Reading Kannada data", logging.INFO)
    data = pd.read_csv('datasets/Kannada/train.csv')
    data = data[['headline']]
    data.rename(columns={'headline': 'text'}, inplace=True)
    data.drop_duplicates(inplace=True)
    data['language'] = 'Kannada'
    writeLog("Saving Kannada data", logging.INFO)
    data.to_csv('final/Kannada.csv', index=None)
    return data


def get_malayalam_data():
    writeLog("Reading Malayalam data", logging.INFO)
    data = pd.read_csv('datasets/Malayalam/news_90k.csv')
    data = data[['headline']]
    data.rename(columns={'headline': 'text'}, inplace=True)
    data['language'] = 'Malayalam'
    writeLog("Saving Malayalam data", logging.INFO)
    data.to_csv('final/Malayalam.csv', index=None)
    return data


def get_odia_data():
    file_paths = [
        "datasets/Odia/train.csv",
        "datasets/Odia/valid.csv"
    ]
    writeLog("Reading Odia data", logging.INFO)

    dfs = []
    for file_path in file_paths:
        df = pd.read_csv(file_path, usecols=['headings'])
        df.rename(columns={'headings': 'text'}, inplace=True)
        df['language'] = "Odia"
        dfs.append(df)

    final = pd.concat(dfs)
    final.drop_duplicates(inplace=True)

    writeLog("Saving Odia data", logging.INFO)

    output_file = os.path.join('final', 'Odia.csv')
    final.to_csv(output_file, index=False)

    return final


def get_tamil_data():
    writeLog("Reading Tamil data", logging.INFO)
    data = pd.read_csv('datasets/Tamil/tamilmurasu_dataset.csv')
    data = data[['news_title']]
    data.drop_duplicates(inplace=True)
    data.rename(columns={'news_title': 'text'}, inplace=True)
    data['language'] = 'Tamil'
    writeLog("Saving Tamil data", logging.INFO)
    data.to_csv('final/Tamil.csv', index=None)
    return data


def get_telugu_data():
    writeLog("Reading Telugu data", logging.INFO)
    data = pd.read_parquet('datasets/Telugu/telugu_news_dataset (1).parquet')
    data = data[['title']]
    data.drop_duplicates(inplace=True)
    data.rename(columns={'title': 'text'}, inplace=True)
    data['language'] = 'Telugu'
    writeLog("Saving Telugu data", logging.INFO)
    data.to_csv('final/Telugu.csv', index=None)
    return data


def create_final_dataset():
    writeLog("Creating final dataset", logging.INFO)
    assamese_data = get_assamese_data()
    bengali_data = get_bengali_data()
    english_data = get_english_data()
    gujarati_data = get_gujarati_data()
    hindi_data = get_hindi_data()
    kannada_data = get_kannada_data()
    malayalam_data = get_malayalam_data()
    odia_data = get_odia_data()
    tamil_data = get_tamil_data()
    telugu_data = get_telugu_data()

    final_df = pd.concat([assamese_data, bengali_data, english_data, gujarati_data, hindi_data, kannada_data,
                          malayalam_data, odia_data, tamil_data, telugu_data], ignore_index=True)

    writeLog("Saving final dataset", logging.INFO)

    final_df.to_csv('Languages.csv', index=None)

    return final_df


def main():
    final_dataset = create_final_dataset()
    print(final_dataset.head())


if __name__ == '__main__':
    def sigterm_handler(_signo, _stack_frame):
        writeLog("Killing Application][{}".format("Thanks! Bye Bye!!!"))
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    main()