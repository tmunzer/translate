import dotenv
import os
import json
import requests

SRC_LANGUAGE="en"

def load():
    dotenv.load_dotenv()
    key = os.getenv('KEY')
    url = os.getenv('URL')
    return (key, url)


def get_models(credentials: str, url: str):
    headers = {"Content-Type": "application/json"}
    full_url = "{0}/v3/models?version=2018-05-01".format(url)
    resp = requests.get(full_url, auth=(
        'apikey', credentials), headers=headers)
    json_data = resp.json()
    models = []
    for model in json_data["models"]:
        if model["source"] == SRC_LANGUAGE:
            models.append(model)
    pretty = json.dumps(models, indent=4)
    print(pretty)


credentials, url = load()
get_models(credentials, url)
