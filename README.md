
# Additional Philamer Scripts

Gregory McCollum, February 2024




## Summary

This repository contains scripts and data related to the Philamer Metadata Remediation project conducted by Gregory McCollum, Curtis Hunt, and Jackson Huang during their time at the University of Michigan Library.

Most the work for this project was completed in 2022. More on this project can found [here](https://mlit.atlassian.net/wiki/spaces/DC/pages/10133864455/Summary+of+Philamer+Metadata+Remediation+Project)

Additionally much of the scripts associated with this project are already documented in [this repository](https://github.com/GregMcC5/philamer_2)

The materials contained in this repository correspond to work completed by Gregory McCollum in late 2023/early 2024. Specifically, he reworked some of the language metadata and prepared the changes on the U-M Library digital collections server.


## LanguageWork

This directory contains the scripts used by Greg to develop new language recommendations for items in the the Philamer collection that utilized the "map" MARC language code, classifying the language of the text as "Austronesian (Other)".

Firstly, in *develop_better_MARC_inventory.py*, we take *marc_lang_database.xml*, which comes from the [Library of Congress MARC webpage](https://www.loc.gov/standards/codelists/languages.xml), and saving the data in a JSON format, with 3-digital language codes as keys, and a list of all full language names as the corresponding value. This approach collapses any distinction between the primary language designation and the Use For (UF) designation that MARC utilizes. This output is saved as *new_marc_lang_codes.json*.

Then runs *new_map_lang.py*, which loops through all the record in the philamer metadata (*dlxs.csv*) which have "map" set as their language. It then loops through each each key-value pair in *new_marc_lang_codes.json* and checks if that languages appears in the keywords or notes fields of the record. If it does, the full language name and code are saved under a "possible langs" field for that record. A spreadsheet with each "map" record, the possible languages w/ codes, and the reocrds notes and keywords field is written to *map_lang_recs.csv*.

This spreadsheet was then manually reviewed, checking for instances where language names were incorrectly detected, identifying which the possible languages were correct, and conducting futher investigation where no languages were detected. Susan Go, Librarian for Southeast Asia, Australia, New Zealand and the Pacific Islands, was consulted when encountering records where not additonal language information was discernible from the metadata.

## deploying_changes

This directory contains the scripts that were run on /quod-dev/dev/gregmcc/philamer in order to develop new data files for the philamer collection with the new metadata.

*deploy.py* runs in a directory with a "data" folder containing all the item-level XML files for the philamer collection. It loops through each of these files, providing new data from the *new_full_best_values.csv*, "check_author.csv*, and *map_lang_changes.csv* (the finalized version of the spreadsheet output by the language process referenced above) files.

While it loops through the values in these spreadsheets, it tracks what fields were edited for each item, these changes are eventually written to *inventory.json*.

The newly edited files are written to another directory "new_data".

Another script, *count_inventory.py* counts the number of instances each field is referenced in *inventory.json* and writes a count of how many times each field was edited across the whole collection to *change_count.json*.
## Note

Gregory McCollum can be reached at gregmcc@umich.edu and gregmcc@uchicago.edu.
