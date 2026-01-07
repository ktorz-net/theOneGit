"""
Created on Feb 13 2019

@author: G. Lozenguez
"""

# -*- coding: utf-8 -*-
import re, os
from bs4 import BeautifulSoup
from copy import copy

class Page() :
    def __init__(self, htmlFile):
        fd= open( htmlFile, "r")
        self.soup = BeautifulSoup( fd.read(), 'html.parser' )
        #self.soup= parseHomeMadeTag(fd)
        fd.close()

    def clean(self):
        # Remove empty lines:
        self.soup = BeautifulSoup( re.sub(r'[\n\s]+', r'\n', str(self.soup), re.MULTILINE), 'html.parser' )
        
    def setStyle(self, styleFiles):
        # Cleanup old style: 
        for tag in self.soup.head.select('style'):
            tag.extract()
        for tag in self.soup.head.select('link'):
            if tag.attrs['rel'] == ["stylesheet"] :
                tag.extract()
        self.clean()
        # create new ones: 
        #<link href="style/hpage.css" rel="stylesheet"/>
        for s in styleFiles :
            self.soup.head.append( self.soup.new_tag("link", rel= ["stylesheet"], href= s ) )
            self.soup.head.append("\n")

    def addHtml5Tags(self, headerFile):
        soup= self.soup
        soup5 = BeautifulSoup( '<!DOCTYPE html>\n<html lang="fr">\n</html>', 'html.parser' )
        soup5.html.append( soup.head )
        soup5.html.append("\n")
        soup5.html.append( soup5.new_tag("body") )
        soup5.html.body.append("\n")
        soup5.html.body.append( soup5.new_tag("article") )

        # Header: 
        div= soup5.new_tag("header")
        fd= open( headerFile, "r")
        div.append( BeautifulSoup( fd.read(), 'html.parser' ) )
        fd.close()
        div.append( soup.h1 )
        soup5.article.append( "\n" )
        soup5.article.append( div )
        div= soup5.new_tag("section")
        soup5.article.append( "\n" )
        soup5.article.append( div )

        div.append( "\n" )
        for elt in soup.html.body :
            if elt.name == 'h2' :
                div= soup5.new_tag("section")
                soup5.article.append( "\n" )
                soup5.article.append( div )
                div.append( "\n" )

            if elt.name == 'aside' :
                div.parent.append( copy(elt) )
            elif elt.name == 'section' :
                div= copy(elt)
                soup5.html.article.append( "\n" )
                soup5.article.append( div )
            else :
                div.append( copy(elt) )
        self.soup= soup5

    def addNavigation( self, home, navList ):
        navHtml= "<nav><ul>\n"
        navHtml+= f"<li><a href=\".\">{home}</a></li>\n"
        for elt in navList :
            navHtml+= f"<li><a href=\"{elt['name']}\">{elt['name']}</a></li>\n"
        navHtml+= "</ul></nav>"
        self.soup.body.append( BeautifulSoup( navHtml, 'html.parser' ) )

    def save( self, htmlFile ):
        fd= open( htmlFile, "w" )
        fd.write( str(self.soup) )
        fd.close()

#from os import listdir
#from os.path import isfile, join
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def loadTag( projectDir="/home/guillaume/Commands" ):
    tag=  []
    dir= projectDir + "/html-part"
    if os.path.isdir( dir ) :
        for file in os.listdir( dir ) :
            t= re.search('(.*).tag.html', file)
            if( t ):
                tag.append( t.group(1) )
    return tag

def readTag(tag, projectDir="/home/guillaume/Commands" ) :
    tagFile=  projectDir + "/html-part/"+tag+".tag.html"
    return open( tagFile, "r").read()

def parseHomeMadeTag( htmlFileDsc ):
    html= ""
    tags= loadTag()

    print( f"Loaded tags: {tags}" )

    for ligne in htmlFileDsc:
        bodyRE= re.search('(.*)(</body>.*)', ligne)
        tagRE= re.search('(.*)<!--([a-zA-Z0-9]+)-->(.*)', ligne)

        if tagRE :
            print("TAG: ", tagRE.group(2))
            if tagRE.group(2) in tags :
                html+= readTag( tagRE.group(2) )
            else :
                html+= '<div class="'+tagRE.group(2)+'"> </div>'

        elif bodyRE :
            html+= bodyRE.group(1)
            html+= bodyRE.group(2)
        else :
            html+= ligne
    return html

def parseFile( htmlFile ):
    fd= open( htmlFile, "r")
    html= parseHomeMadeTag(fd)
    fd.close()
    html= toHTML5(html)
    html= identifyImages(html)
    fd= open( htmlFile, "w" )
    #html= html.replace("\n", "")
    #html= html.replace("html><html", "html>\n<html")
    #html= html.replace("</head>", "</head>\n")
    #html= html.replace("</header>", "</header>\n")
    #html= html.replace("</section>", "</section>\n")
    #html= html.replace("</body>", "\n")
    #html= html.replace("</html>", "\n</body>\n</html>")
    fd.write( html )
    fd.close()
    return html

def toHTML5( html ):

    soup = BeautifulSoup( html, 'html.parser' )
    soup5 = BeautifulSoup( '<!DOCTYPE html>\n<html lang="fr">\n</html>', 'html.parser' )

    soup5.html.append( soup.head )
    soup5.html.append("\n")
    soup5.html.append( soup5.new_tag("body") )
    soup5.html.append("\n")
    soup5.html.append( soup5.new_tag("article") )
    div= soup5.new_tag("header")
    soup5.html.article.append( "\n" )
    soup5.html.article.append( div )
    div.append( "\n" )

    for elt in soup.html.body :
        if elt.name == 'h2' :
            div= soup5.new_tag("section")
            soup5.article.append( "\n" )
            soup5.article.append( div )
            div.append( "\n" )

        if elt.name == 'aside' :
            div.parent.append( copy(elt) )
        elif elt.name == 'section' :
            div= copy(elt)
            soup5.html.article.append( "\n" )
            soup5.article.append( div )
        else :
            div.append( copy(elt) )
    return str(soup5)

def identifyImages( html ):

    soup = BeautifulSoup( html, 'html.parser' )
    print("identify all images :")
    for img in soup.find_all('img') :
        srcFile= img.get("src").split("/")[-1]
        img["id"]= srcFile.replace(".","_")

    return str(soup)
