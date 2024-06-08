import os
import languages
import argparse


def download_language_datasets():
    os.environ["KAGGLE_CONFIG_DIR"] = "/mnt/data/language_detection"
    data = languages.languages

    os.makedirs("datasets", exist_ok=True)

    parser = argparse.ArgumentParser(description="Download language datasets")
    parser.add_argument("-l", "--language", help="Specify a language to download")
    args = parser.parse_args()

    languages_to_download = args.language.split(",") if args.language else data.keys()

    for language in languages_to_download:
        info = data.get(language)
        if info is None:
            print(f"Language '{language}' not found in the language list.")
            continue

        platform = info.get("platform")
        command = info.get("command")

        print("\nDOWNLOADING", language, "\n")

        if platform == "kaggle":
            if " -f " in command:
                file_name = command.split(" -f ")[-1] + ".zip"
            elif "/" in command:
                file_name = command.split("/")[-1] + ".zip"
            else:
                file_name = command.split(" ")[-1] + ".zip"

            os.system(f"cd datasets && {command}")
            os.rename(f"datasets/{file_name}", f"datasets/{language}.zip")
            os.system(f"cd datasets && unzip {language}.zip -d {language} && rm {language}.zip")

        elif platform == "wget":
            file_name = command.split("/")[-1]
            extension = file_name.split(".")[-1]
            os.system(f"cd datasets && wget {command}")
            os.rename(f"datasets/{file_name}", f"datasets/{language}.{extension}")

            if extension == "zip":
                print(f"Unzipping... {file_name}")
                os.system(f"cd datasets && unzip {language}.zip -d {language} && rm {language}.zip")
            elif extension == "tgz":
                print(f"Unzipping... {language}")
                os.system(f"cd datasets && mkdir {language} && cd {language} && tar -xvzf ../{language}.tgz && rm ../{language}.tgz")

        print("\nDONE", language, "\n")


def main():
    download_language_datasets()


if __name__ == "__main__":
    main()
