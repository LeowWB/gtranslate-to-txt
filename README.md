I suppose it's more accurate to call this repo `gtranslate-to-csv` since the output is actually in `.csv` format. Oops.

Google Translate has this "Saved Translations" feature, and it also allows you to export your saved translations to Google Sheets. That's pretty useful for someone like me who makes Anki flashcards out of the saved translations. Problem is, the exported Google Sheet doesn't have pinyin. So I made this script to take that exported Google Sheet and to add the pinyin in separately, also using Google Translate but in a Selenium-controlled browser. The output will be a `.csv` file that you can import into Anki.

To use this, install the dependencies and stuff as usual. Also download the Chrome Webdriver and indicate its path in the script. And remember to convert your saved translations to a Google Sheet, then download that sheet as a `.csv` file. Might wanna change your terminal font too. SimHei works for me.
