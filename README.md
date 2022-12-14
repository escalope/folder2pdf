# About

This program takes a folder structure and converts it into a single PDF with bookmarks. 

The output is a single file "final.pdf". The main folder can hold a file called "00portada.pdf" that holds the portrait of the expected document.

# Requirements

The software that needs to be installed is the following:
- Ghostscript. The command "gs" should be executable from command line
- The fpdf library for python
- The unidecode for python
- python3

It was made to run in linux, but it should run into other platforms, provided the "gs" command is available from command line and the python3 is installed. 


To install python3 requirements, it is recommended to use a virtual environment

    python -m venv virt
    virt/bin/pip3 install fpdf
    virt/bin/pip3 install unidecode
    
To install ghostscript

    sudo apt install ghostscript
    
# Running it

If the folder to be converted is FOLDER, the command would be

    python3 folder2pdf.py FOLDER
    
# Sample

The folder sample contains a possible folder structure with two pdf files. The file "final.pdf" exemplifies the result.

The bookmarks panel shows how the two inserted files within a single document with a hand made portrait. Bookmarks are clickable. 

![image](https://user-images.githubusercontent.com/3056482/197363954-72930b5f-6f29-486e-9f88-207eda23e792.png)

The resulting file can be downloaded from [https://github.com/escalope/folder2pdf/blob/main/final.pdf](https://github.com/escalope/folder2pdf/blob/main/final.pdf)

# License

This program is free software; you can redistribute it and/or modify  it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or  (at your option) any later version. 
This program is distributed in the hope that it will be useful,  but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  GNU General Public License for more details.
You should have received a copy of the GNU General Public License  along with this program; if not, write to the Free Software Foundation,  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
