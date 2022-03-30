import dotenv
import os
import json
import requests

SOURCE = 'jp_common_resource.json'
DEST = 'fr_common_resource.json'
LNG_DST = "en-fr"


def load():
    dotenv.load_dotenv()
    key = os.getenv('KEY')
    url = os.getenv('URL')
    return (key, url)


def read_file():
    with open(SOURCE, 'r') as source:
        json_data = json.load(source)
        return json_data


def save_file(data_translated):
    with open(DEST, 'w') as dest:
        json.dump(data_translated, dest, ensure_ascii=False, indent=4)


def translate(data: json, credentials: str, url: str):
    data_translated = {}
    for key in data:
        str_to_transalte = data[key].replace("__NOT_TRANSLATED__: ", "")
        arr_tranlated = watson(str_to_transalte, credentials, url)
        if (len(arr_tranlated) == 1):
            translation = arr_tranlated[0]["translation"]
        else:
            translation = arr_tranlated
        print('"{0}": "{1}" -> "{2}"'.format(key, str_to_transalte, translation))
        data_translated[key] = translation
    return data_translated


def watson(str_to_transalte: str, credentials: str, url: str):
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"text": str_to_transalte, "model_id": LNG_DST})
    full_url = "{0}/v3/translate?version=2018-05-01".format(url)
    resp = requests.post(full_url, auth=(
        'apikey', credentials), headers=headers, data=payload)
    resp_json = resp.json()
    return resp_json["translations"]


credentials, url = load()
data_to_translate = read_file()
data_translated = translate(data_to_translate, credentials, url)
save_file(data_translated)
