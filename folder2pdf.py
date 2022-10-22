#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Folder2PDF, a program to convert a folder structure with pdfs 
# into a single pdf having as bookmarks folder names
# Copyright (C) 2016  Jorge J. Gomez-Sanz
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA


import os
import subprocess
import sys
from unidecode import unidecode
from fpdf import FPDF

def stripbookmark(pdffile):
  pdffile=pdffile.replace("\'","\\\'").replace("(","\\(").replace(")","\\)").replace("&","\\&").replace(" ","\\ ")
  cmd = "cp %s /tmp/temp.pdf" % pdffile 
  print (cmd)
  q=subprocess.check_call(cmd, shell=True,stderr=subprocess.STDOUT,)
  #for subline in q.stdout.readlines():
        
  cmd = "pdftk A=/tmp/temp.pdf cat A1-end output %s" % pdffile 
  q=subprocess.check_call(cmd, shell=True)
  #for subline in q.stdout.readlines():
  return 0

def getNumberOfPages(pdffile):
  pdffile=pdffile.replace("\'","\\\'").replace("(","\\(").replace(")","\\)").replace("&","\\&").replace(" ","\\ ")
  cmd = "pdfinfo %s" %pdffile 
 
  q=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  for subline in q.stdout.readlines():
    if "Pages:" in str(subline):
        return int(subline[7:])
  print("ERROR: No pages found in "+pdffile)
  return 0

files=[]        
links={}

# Simulates the creation of section index to estimate its size in pages. This is necessary to know what is the real starting page of the first file document in the folder. For large document names and a large number of documents, a section index can take several pages.
def estimateIndexLengthInPages(cpath,dirName,nextPageNumber,subdirList,fileList):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial",'U', size=24)
        nextPageNumber=1000#test with four digits
        if (dirName[dirName.rfind("/")+1:]!=""):
               pdf.multi_cell(200, 12, txt=unidecode(dirName[dirName.rfind("/")+1:]), align="C")
        else:
               pdf.multi_cell(200, 12, txt=unidecode(dirName), align="C")   
        pdf.set_font("Arial", size=20)
        for fname in fileList:
               if fname.lower().endswith(".pdf"):
                     #print fname                
                     pageCount=getNumberOfPages(cpath+"/"+fname)
                     prettyfname=fname.replace(".pdf","").replace(".PDF","")         
                     sectionContent=prettyfname+"....."+str(nextPageNumber)+"\n"
                     pdf.multi_cell(0, 10, txt=unidecode(sectionContent), align="R")
                     nextPageNumber=nextPageNumber+pageCount                     
        for subdirName in subdirList:
                     sectionContent="+ "+subdirName+"...."+str(nextPageNumber)+"\n"
                     pdf.multi_cell(0, 10, txt=unidecode(sectionContent), align="L")
        return pdf.page_no()

# Generates the bookmarks for the documents contained in the rootDir. These bookmarks will be  appended to the final pdf
def generateBookmarks(rootDir,currentPageNumber, cpath):

        nextPageNumber=currentPageNumber    
        (dirName, subdirList, fileList) = next (os.walk(rootDir))
        itemcount=len(subdirList)+ len(fileList)             
        validFile=0
        validFolder=0
        sectionString=""
        #create section pdf with the name of the containing folder
        if ("00seccion.pdf" in  fileList):
               print(fileList)
               fileList.remove("00seccion.pdf") # removes previous occurences of 00section
#               sys.exit(0)
#       fileList.append("00seccion.pdf") # ensures it is the last element to consider
        sectionContent=""
        # get the name of all pdf files, prepare their bookmark
        fileList=sorted(set(fileList))
        # generate a page listing section subcontent. The section index is very long to fit into one page

        pdf = FPDF()#orientation='P',unit='mm',format=(210,700))
        pdf.add_page()
        pdf.set_font("Arial",'U', size=24)
        if (dirName[dirName.rfind("/")+1:]!=""):
               pdf.multi_cell(200, 12, txt=unidecode(dirName[dirName.rfind("/")+1:]), align="C")
        else:
               pdf.multi_cell(200, 12, txt=unidecode(dirName), align="C")   
        pdf.set_font("Arial", size=20)
        files.append((cpath+"/00seccion.pdf"))
        subdirList.sort()
        initialPage=nextPageNumber
        estimatedPages=estimateIndexLengthInPages(cpath,dirName,initialPage,subdirList,fileList)
        nextPageNumber= nextPageNumber+estimatedPages
        for fname in fileList:
               if fname.lower().endswith(".pdf") and not fname.lower() == "00portada.pdf" :
                     #print fname                
                     stripbookmark(cpath+"/"+fname)
                     pageCount=getNumberOfPages(cpath+"/"+fname)
                     prettyfname=fname.replace(".pdf","").replace(".PDF","")         
                     sectionString=sectionString+"[/Title ("+prettyfname+") /Page "+str(nextPageNumber)+" /OUT pdfmark\n"        
                     sectionContent=prettyfname+"....."+str(nextPageNumber)+"\n"
                     pdf.multi_cell(0, 10, txt=unidecode(sectionContent), align="R")
                     validFile=validFile+1                  
                     nextPageNumber=nextPageNumber+pageCount
                     files.append(cpath+"/"+fname)

        for subdirName in subdirList:
               (result,subsectionNextPage)=generateBookmarks(cpath+"/"+subdirName,nextPageNumber, cpath+"/"+subdirName)
               if subsectionNextPage!=nextPageNumber:
                     sectionContent="+section "+subdirName+"...."+str(nextPageNumber)+"\n"
                     pdf.multi_cell(0, 10, txt=unidecode(sectionContent), align="L")
                     nextPageNumber=subsectionNextPage
                     sectionString=sectionString+result
                     validFolder=validFolder+1 

        # perform the same process on subfolders                
        if (dirName[dirName.rfind("/")+1:]!=""):
               sectionString="[/Count -"+str(validFile+validFolder)+" /Title ("+dirName[dirName.rfind("/")+1:]+") /Page "+str(currentPageNumber)+" /OUT pdfmark\n"+sectionString
        else:
               sectionString="[/Count -"+str(validFile+validFolder)+" /Title ("+dirName+") /Page "+str(currentPageNumber)+" /OUT pdfmark\n"+sectionString
               
        print ("writing to "+(cpath+"/00seccion.pdf")+"\n")
        pdf.output((cpath+"/00seccion.pdf"), 'F')
        if (getNumberOfPages((cpath+"/00seccion.pdf"))!=estimatedPages):
                print("error estimating the number of pages, it was expected to have "+str(estimatedPages)+" and there were "+str(getNumberOfPages((cpath+"/00seccion.pdf")))+" in file "+cpath+"/00seccion.pdf")
                sys.exit(-1)
#        nextPageNumber=nextPageNumber+getNumberOfPages((cpath+"/00seccion.pdf"))
        return (sectionString,nextPageNumber)


print (""" Folder2PDF, a program to convert a folder structure with pdfs 
 into a single pdf having as bookmarks folder names
 Copyright (C) 2016  Jorge J. Gomez-Sanz

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software Foundation,
 Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA""")

input("Press Enter to continue...")

if (len(sys.argv)<1):
        print ("Error: The script needs as parameter the path to the folder to be converted")
        print ("python pdfGenerationWithBookmarks.py PATH_TO_THE_FOLDER")
        print ("Generated pdf will be stored into 'final.pdf' file")
        print ("If you run into errors due to too long commands, type in your console ulimit ")
else:
        # makes the portrait the first page
        (dirName, subdirList, fileList) = next (os.walk(sys.argv[1]))
        for fname in fileList:
               if fname.lower() == "00portada.pdf" :
                files.append(sys.argv[1]+"/"+fname)                
        (result,totalPageCount)=generateBookmarks(sys.argv[1],2,sys.argv[1])
        f = open('pdfmarks', 'w')
        f.write(unidecode(result))
        f.close()


        # invoke gs to merge all files and combine with bookmarks stored into pdfmarks
        fileString=[]
        fileQuotedString=""
        for file in files:
               fileString.append(file)
        command=["gs","-dPrinted=false","-dBATCH","-dNOPAUSE","-sDEVICE=pdfwrite","-sOutputFile=final.pdf"]
        command=command + fileString+["pdfmarks"]
        q=subprocess.check_call(command)
