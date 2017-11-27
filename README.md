# Synopsis-Stripper

For the iTunes TV packaging/checking workflow:

This app pulls the episode description from each iTunes TV metadata XML and stores in .txt on user desktop, separated by two newlines, for spellchecker analysing (OS X/MacOS only).

Instructions for use:
- Drag and drop Container ID folder (containing episode .itmsps with metadata XMLs) from Finder onto app
- Hit submit and .txt is created
- .txt opens in default application for spellchecking

Requires compilation with py2app or similar.
---
I used:
- Python 2.7
- wxPython (a GUI framework)
