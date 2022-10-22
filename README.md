# About

This program takes a folder structure and converts it into a single PDF with bookmarks. 

The output is a single file "final.pdf". The main folder can hold a file called "00portada.pdf" that holds the portrait of the expected document.

# Requirements
The software that needs to be installed is the following:
- Ghostscript. The command "gs" should be executable from command line
- The fpdf library for python
- The unidecode for python
- python3

# Running it

If the folder to be converted is FOLDER, the command would be

  python3 folder2pdf.py FOLDER

