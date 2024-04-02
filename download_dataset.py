import os
import languages
import zipfile

os.environ["KAGGLE_CONFIG_DIR"] = "/mnt/data/APIs"

data = languages.languages
test = data["Hindi"]["command"]

os.makedirs("datasets", exist_ok=True)

for i, j in data.items():
    language = i
    try:
        command = j["command"]
        platform = j["platform"]
    except KeyError:
        command, platform = None, None

    print("\nDOWNLOADING", language, "\n")

    if platform == "kaggle":
        if "/" in command:
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