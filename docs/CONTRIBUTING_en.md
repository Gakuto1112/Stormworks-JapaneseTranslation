Language: 　**English**　|　[日本語](./CONTRIBUTING.md)

## CONTRIBUTING
### Files that should be edited
From v1.10.8-b, component names are written in both Japanese and English.
The directory structure of this repository has changed drastically because of this.
The file that you should edit when editing Japanese translations is `/src/translation_data/japanese.tsv`.

The addition of English component names will be done on the remote.
Therefore, please fill in the component names in `/src/translation_data/japanese.tsv` **only in Japanese**.

### Translation rules
These are two rules for Japanese translation.
Please keep these rules when you contribute to this repository.

1. Do not use prohibited characters.
   - Prohibited characters are the followings: "、", "。", "　 (multi-bytes space)", "|"
   - Please replace Japanese reading marks into ", ". A space after a comma is required unless at the end of a sentence.
   - Please replace Japanese punctuation marks into ". ". A space after a period is required unless at the end of a sentence.


2. Fill all Japanese translations
   - Please make sure that the ⚠️ mark doesn't appear in "japanese" on the "Language" page.
   - Hovering over the ⚠️ mark will point out the missing translation key.

This is not required, but please make sure that your translation fits the ["About Japanese Translations" in README]((./README_en.md#translation-policies)).
If necessary, we will review them in your pull request.

### Pull requests
Tests are run automatically when you submit your pull requests or push additional commits to ensure your translation meets the above two rules.
Please make sure that your translation passes this test.
