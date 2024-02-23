import metadata_utils as mu
import re

# records = mu.read_csv("dlxs.csv")
# marc_lang = [x for x in mu.read_csv("marc_lang.csv") if "-" not in x[0]]
# output = [["dlxs_id", "original_lang", "possible langs", "notes & keywords"]]

# #print(len([x for x in records if "map" in x[-2]]))
# for record in [x for x in records if "map" in x[-2]]:
#     possible_langauges = list()
#     for lang in marc_lang:
#         if f"in {lang[1].split(' ')[0]}".lower() in record[-3].lower():
#             possible_langauges.append(lang[0])
#         if lang[1].split(" ")[0].lower() not in ("church", "no", "east", "west"):
#             re_langs = set(re.findall(lang[1].split(" ")[0].lower()+" ", record[-1].lower() + record[-3].lower(), re.DOTALL))
#             if re_langs:
#                 for re_lang in [x for x in re_langs]:
#                     possible_langauges.extend([x[0] for x in marc_lang if re_lang[:-1] in x[1].lower()])
#     print(list(set(possible_langauges)))
#     output.append([record[1],record[-2][2:5], possible_langauges, record[-1] + record[-3]])

# mu.write_csv("Oct2023_map_lang_recs.csv", output)
# print('done')

#more work to be done here; load in larger dataset of languages with more specific umbrella codes (phi)
#Now occurring below


#----------------------------

records = mu.read_csv("dlxs.csv")
marc_lang = mu.read_json("new_marc_lang_codes.json")
output = [["dlxs_id", "original_lang", "possible codes", "possible lang names" "notes & keywords"]]

for record in [x for x in records if "map" in x[-2]]:
    possible_langauges = list()
    possible_lang_names = list()
    for code,lang_names in marc_lang.items():
        for lang in lang_names:
            #not changing lang name
            if f"in {lang}".lower() in record[-3].lower() and code not in possible_langauges:
                if code not in possible_langauges:
                    possible_langauges.append(code)
                if lang not in possible_lang_names:
                    possible_lang_names.append(lang)
            if " " + lang.lower() in  " " +record[-1].lower().lstrip("['").replace("'", "") + record[-3].lower().lstrip("['").replace("'", ""):
                if code not in possible_langauges:
                    possible_langauges.append(code)
                if lang not in possible_lang_names:
                    possible_lang_names.append(lang)
            #changing lang name
            if "(" in lang and ")" in lang:
                lang = lang[:lang.index('(')]
                if f"in {lang}".lower() in record[-3].lower():
                    if code not in possible_langauges:
                        possible_langauges.append(code)
                    if lang not in possible_lang_names:
                        possible_lang_names.append(lang)
                if " " + lang.lower() in " " + record[-1].lower().lstrip("['") + record[-3].lower().lstrip("['"):
                    if code not in possible_langauges:
                        possible_langauges.append(code)
                    if lang not in possible_lang_names:
                        possible_lang_names.append(lang)
    output.append([record[1],record[-2][2:5], possible_langauges, possible_lang_names, record[-1] + record[-3]])

mu.write_csv("Oct2023_map_lang_recs_2.csv", output)
print('done')
