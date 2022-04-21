# translate

this python script is leveraging IBM Watson to accelerate the translation

### IBM Account
1. Create an IBM Wastrong account [here](https://cloud.ibm.com/registration?target=/catalog/services/language-translator) 
2. Register for [Language Translator](https://cloud.ibm.com/catalog/services/language-translator), select the `Lite` plan (the registration process requires a credit card, but the [translation API is free for basic usage and up to 1,000,000 characters per month](https://www.ibm.com/cloud/watson-language-translator/pricing))
3. In you IBM account, go to your [Resource List](https://cloud.ibm.com/resources). In the list, you should see `Services and software (1)` and below it `Language Translator-XX`. Click on `Language Translator-XX` and then `View Full Details`. In this page are displayed your `API Key` and your `URL` 

### Script Configuration
1. Clone this repository on your hard drive
2. from the repository folder, install the script dependencies (`python3 -m pip install -r requirements.txt`)
3. create a `.env` file in the repository folder, with the following:
```
KEY=the_key_from_the_step_3_above
URL=the_url_from_the_step_3_above
```
3. copy the source file to translate in the repository folder
4. update the `MODEL` variables in the script file, to match your requirements:
* `MODEL`: the WATSON Model. It's basically something like `xx-yy`, where `xx` is the source language code (e.g. `en` for English) and `yy` is the destination language code (e.g. `fr` for Franch). You can use the `languages.py` script to list all the available models.
5. Run the script with `python3 ./translate.py -s <source_file> `
6. The output is saved in a new file named as the source file name, but prefixed with the destination language.