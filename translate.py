import dotenv
import os
import json
import requests
import sys
import getopt

SOURCE = 'resource.json'
DEST = ''
MODEL = "en-fr"


def load():
    dotenv.load_dotenv()
    key = os.getenv('KEY')
    url = os.getenv('URL')
    return (key, url)


def read_file(src_file):
    with open(src_file, 'r') as source:
        json_data = json.load(source)
        return json_data


def save_file(data_translated, dst_file):
    with open(dst_file, 'w') as dest:
        json.dump(data_translated, dest, ensure_ascii=False, indent=4)


def translate(data: json, credentials: str, url: str, model: str):
    data_translated = {}
    for key in data:
        str_to_transalte = data[key].replace("__NOT_TRANSLATED__: ", "")
        arr_tranlated = watson(str_to_transalte, credentials, url, model)
        if (len(arr_tranlated) == 1):
            translation = arr_tranlated[0]["translation"]
        else:
            translation = arr_tranlated
        print('"{0}": "{1}" -> "{2}"'.format(key, str_to_transalte, translation))
        data_translated[key] = translation
    return data_translated


def watson(str_to_transalte: str, credentials: str, url: str, model: str):
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"text": str_to_transalte, "model_id": MODEL})
    full_url = "{0}/v3/translate?version=2018-05-01".format(url)
    resp = requests.post(full_url, auth=(
        'apikey', credentials), headers=headers, data=payload)
    resp_json = resp.json()
    return resp_json["translations"]


def usage():
    print('''
Script using IBM Watson APIs to translate variables in JSON file.

This script requires IBM API Keys:
# IBM Account
1.  Create an IBM Wastrong account here
2.  Register for Language Translator, select the Lite plan (the registration
    process requires a credit card, but the translation API is free for basic
    usage and up to 1,000,000 characters per month)
3.  In you IBM account, go to your Resource List. In the list, you should see
    Services and software (1) and below it Language Translator-XX. Click on 
    Language Translator-XX and then View Full Details. In this page are 
    displayed your API Key and your URL

# Script configuration
1. create a .env file in the repository folder, with the following:
KEY=the_key_from_the_step_3_above
URL=the_url_from_the_step_3_above

# Script Options
    -s, --source        Source file location
    -d, --destination   Destintation file location
    -m --model          Watson translation model. It's basically something like 
                        xx_yy, where xx is the source language code (e.g. en for
                        English) and yy is the destination language code (e.g.
                        fr for Franch). You can use the languages.py script to 
                        list all the available models.
                        NOTE: You can "hard code" the model by editing the script
    -h              This help

''')


def main(argv):
    src_file = SOURCE
    dst_file = DEST
    dst_file_set = False
    model = MODEL
    try:
        opts, args = getopt.getopt(
            argv, "hs:d:m:", ["source=", "destination=", "model="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-s", "--source"):
            src_file = arg
        elif opt in ("-d", "--destination"):
            dst_file = arg
            dst_file_set = True
        elif opt in ("-m", "--model="):
            model = arg

    if (not src_file):
        usage()
        sys.exit(2)
    if (not dst_file_set):
        dst_language = model.split("-")[1]
        if (src_file.index("_en_") > -1):
            dst_file = src_file.replace("_en_", "_{0}_".format(dst_language))
        else:
            dst_file = "{0}_{1}".format(dst_language, src_file)

    print("Source File      : {0}".format(src_file))
    print("Destination File : {0}".format(dst_file))
    print("Model            : {0}".format(model))
    credentials, url = load()
    data_to_translate = read_file(src_file)
    data_translated = translate(data_to_translate, credentials, url, model)
    save_file(data_translated, dst_file)


if __name__ == "__main__":
    main(sys.argv[1:])
