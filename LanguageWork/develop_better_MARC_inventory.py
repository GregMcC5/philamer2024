import requests
import metadata_utils as mu
from bs4 import BeautifulSoup

marc_langs_full = {}

response = requests.get("https://www.loc.gov/standards/codelists/languages.xml")
if response.status_code == 200:
    lang_xml = BeautifulSoup(response.content, "lxml-xml")
    mu.write_xml(response.content, "marc_lang_database.xml")

for language in lang_xml.find_all("language"):
    print("full language xml content\n", language)
    code = [x.text for x in language if x.name == "code"][0] if len([x.text for x in language if x.name == "code"]) == 1 else None
    print("\ncode:", code)
    names = [x.text for x in language if x.name == "name"]
    uf_names = []
    for uf in [x for x in language if x.name == "uf"]:
        uf_names.extend([x.text for x in BeautifulSoup(str(uf), "xml").find_all("name")])

    print("code", code)
    print("lang names", names)
    print("UF", uf_names)

    names.extend(uf_names)
    marc_langs_full[code] = names
    print("===========")

mu.write_json("new_marc_lang_codes.json", marc_langs_full)



print('done')