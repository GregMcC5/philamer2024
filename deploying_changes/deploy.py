import os
import xml.etree.ElementTree as ET
import ast
import csv
import json

def log(message):
    os.system(f'echo "{message}" >> error_log.txt')
    print(message)

def read_csv(filepath, encoding='utf-8', newline='', delimiter=','):
    with open(filepath, 'r', encoding=encoding, newline=newline) as file_obj:
        data = []
        reader = csv.reader(file_obj, delimiter=delimiter)
        for row in reader:
            data.append(row)

        return data
    
def write_text(filepath, content):
    try:
        with open(filepath, 'w') as file:
            file.write(content)
        print(f"String written to '{filepath}' successfully.")
    except Exception as e:
        print(f"Error writing to '{filepath}': {e}")

def read_text(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

langs = list(read_csv("map_lang_changes.csv"))[1:]
vals = list(read_csv("new_full_best_values.csv"))[1:]
new_authors = list(read_csv("check_author.csv"))[1:]

inventory = dict()

for file in [x for x in os.scandir("data") if "noded" in x.name]:
    print(file.name)
    id = ".".join(file.name.split(".")[:3]).lower()
    inventory[id] = set()
    if file.name.split(".xml")[0].lower() in [x[1].lower() for x in vals]:
        # print(" found one")
        tree = ET.parse(file.path)
        root = tree.getroot()
        if [x for x in root.iter("IDNO") if x.attrib["TYPE"] == "dlps"][0].text.lower() in [x[1].lower() for x in vals]:
            print(file.name, 'ready')

            lang_match = [x for x in langs if x[0].lower() == file.name.split(".xml")[0].lower()]
            if len(lang_match) == 1:
                lang_match = lang_match[0]
            else:
                lang_match = None
            val_match = [x for x in vals if x[1].lower() == file.name.split(".xml")[0].lower()][0]

            #--introudcing changes--
            #-languages-
            try:
                if lang_match:
                    if "," not in lang_match[3]:
                        root.find("HEADER/PROFILEDESC/LANGUSAGE/LANGUAGE").text = lang_match[3].split(" - ")[1]
                        root.find("HEADER/PROFILEDESC/LANGUSAGE").attrib["ID"] = lang_match[3].split(" - ")[0]
                    else:
                        root.find("HEADER/PROFILEDESC/LANGUSAGE/LANGUAGE").text = "Multiple languages"
                        root.find("HEADER/PROFILEDESC/LANGUSAGE").attrib["ID"] = "mul"
                    # print(root.find("HEADER/PROFILEDESC/LANGUSAGE").attrib, root.find("HEADER/PROFILEDESC/LANGUSAGE/LANGUAGE").text)
                    inventory[id].add("Language")
            except:
                log("|".join([file.name, "language"]))

            #--Other Vals--

            # #-Title-
            # try:
            #     if root.find("HEADER/FILEDESC/TITLESTMT/TITLE").text != val_match[2]:
            #         print('title iss!--')
            #         print(root.find("HEADER/FILEDESC/TITLESTMT/TITLE").text)
            #         print(val_match[2])
            # except:
            #     log("|".join([file.name, "title"]))

            #-Keywords-
            if val_match[-1]:
                #try:
                    new_keywords = ast.literal_eval(val_match[-1]) if type(ast.literal_eval(val_match[-1])) == list else None
                    if new_keywords:
                        # print("fixing keywords")
                        key_tag = ET.Element("KEYWORDS")
                        if root.find("HEADER/PROFILEDESC/TEXTCLASS/KEYWORDS") is None:
                            inventory[id].add("Subject Terms")
                        for keyword in [x.rstrip(".") for x in new_keywords if "fast --" not in x]:
                            if "Subject Terms" not in inventory[id]:
                                if keyword not in [x.text for x in root.find("HEADER/PROFILEDESC/TEXTCLASS/KEYWORDS")]:
                                    inventory[id].add("Subject Terms")
                            term = ET.Element("TERM")
                            term.text = keyword
                            key_tag.append(term)
                        if root.find("HEADER/PROFILEDESC/TEXTCLASS") is None:
                            root.find("HEADER/PROFILEDESC").append(ET.Element("TEXTCLASS"))
                        if root.find("HEADER/PROFILEDESC/TEXTCLASS/KEYWORDS") is not None:
                            root.find("HEADER/PROFILEDESC/TEXTCLASS").remove(root.find("HEADER/PROFILEDESC/TEXTCLASS/KEYWORDS"))
                        root.find("HEADER/PROFILEDESC/TEXTCLASS").append(key_tag)
                #except:
                    #log("|".join([file.name, "keywords"]))
                
            #-Author-
            try:
                if file.name.split(".xml")[0].lower() in [x[1].lower() for x in new_authors]:
                    author_match = [x for x in new_authors if x[1].lower() == file.name.split(".xml")[0].lower()][0]
                    if root.find("HEADER/FILEDESC/TITLESTMT/AUTHOR") is not None:
                        if author_match[4]:
                            if root.find("HEADER/FILEDESC/TITLESTMT/AUTHOR").text != author_match[4]:
                                root.find("HEADER/FILEDESC/TITLESTMT/AUTHOR").text = author_match[4]
                                inventory[id].add("Author")
            except:
                log("|".join([file.name, "author"]))
            
            # if val_match[3]:
            #     prev_author = None
            #     for i, author in enumerate(list(root.iter("AUTHOR"))):
            #         # print(i)
            #         if i > 0:
            #             prev_author = author.text
            #         if prev_author and author.text != prev_author:
            #             print('multiple authors indicated')
            #         if author.text.lower() != val_match[3].lower():
            #             author.text = val_match[3]
            #             # print("fixed author")
            #         else:
            #             log("|".join([file.name, "author"]))
            

            #-Note-
            if val_match[-2] and val_match[-2] != "[]":
                #try:
                    new_notes = ast.literal_eval(val_match[-2]) if type(ast.literal_eval(val_match[-2])) == list else None
                    if new_notes:
                        #check match:
                        notesstmt_tag = ET.Element("NOTESSTMT")
                        if root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/NOTESSTMT") is None:
                            inventory[id].add("Notes")
                        for note in new_notes:
                            if "Notes" not in inventory[id]:
                                if note not in [child.text for child in root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/NOTESSTMT")]:
                                    inventory[id].add("Notes")
                            note_tag = ET.Element("NOTE")
                            note_tag.text = note
                            notesstmt_tag.append(note_tag)
                        if root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/NOTESSTMT") is not None:
                            root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL").remove(root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/NOTESSTMT"))
                        root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL").append(notesstmt_tag)
                    else:
                        print("no new notes")
                #except:
                    #log("|".join([file.name, "notes"]))
        

            #-PubPlace-
            if val_match[4]:
                try:
                    if root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/PUBPLACE") is not None:
                        if root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/PUBPLACE").text.lower().rstrip(" :").rstrip(":") != val_match[4].lower().rstrip(" :").rstrip(":"):
                            # print("replacing pub place")
                            root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/PUBPLACE").text = val_match[4].rstrip(" :").rstrip(":")
                            inventory[id].add("Publication Place")
                    else:
                        print("making new pubplace tag")
                        new_pubplace = ET.Element("PUBPLACE")
                        new_pubplace.text = val_match[4].rstrip(" :").rstrip(":")
                        root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT").append(new_pubplace)
                        inventory[id].add("Publication Place")
                except:
                    log("|".join([file.name, "pub_place"]))

            #-Publisher
            if val_match[5]:
                try:
                    if root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/PUBLISHER") is not None:
                        if root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/PUBLISHER").text.lower() != val_match[5].lower():
                            # print("replacing publisher")
                            root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/PUBLISHER").text = val_match[5]
                            inventory[id].add("Publisher")
                    else:
                        print("making new publisher tag")
                        new_publisher = ET.Element("PUBLISHER")
                        new_publisher.text = val_match[5]
                        root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT").append(new_publisher)
                        inventory[id].add("Publisher")
                except:
                    log("|".join([file.name, "Publisher"]))

            #-PubDate-
            if val_match[6]:
                try:
                    if root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/DATE") is not None:
                        if root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/DATE").text.lower().strip(".") != val_match[6].lower().strip('.'):
                            # print("replacing date")
                            root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT/DATE").text = val_match[6]
                            inventory[id].add("Publication Date")
                    else:
                        print("Making new date tag")
                        new_pub_date = ET.Element("DATE")
                        new_pub_date.text = val_match[6]
                        root.find("HEADER/FILEDESC/SOURCEDESC/BIBLFULL/PUBLICATIONSTMT").append(new_pub_date)
                        inventory[id].add("Publication Date")
                except:
                    log("|".join([file.name, "publication date"]))

        tree.write(f"new_data/{file.name.replace('.utf', '')}")
        print("wrote", file.name)
        print("\n","---"*4,"\n")
        inventory[id] = [x for x in inventory[id]]

    else:
        print("no data\n")
        write_text(f"new_data/{file.name.replace('.utf', '')}",read_text(file.path)) 
        inventory[id] = [x for x in inventory[id]]


write_json("inventory.json", inventory)
print("done")