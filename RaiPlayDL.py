#!/usr/bin/env python3

import re, os, contextlib, sys
import urllib
import pydub
import glob
from os import path as path
from pydub import AudioSegment
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

class Raipodcast():
    def __init__(self, url):
        self.url = url
        
    def getFile (self, url,filename):
        ## Not sure why, but for some files only wget works fine, NOT the request thing
        os.system('wget -O '+filename+' '+url)
        #request = requests.get(url, timeout=60, stream=True)
        #with open(filename, 'wb') as fh:
        #    for chunk in request.iter_content(1024 * 1024):
        #        fh.write(chunk)

    def process(self, folder):
        #Check tmp directory
        if not os.path.exists('./tmp'):
            os.makedirs('./tmp')
        #Clean tmp directory		
        files = glob.glob('tmp/*')
        for f in files:
            os.remove(f)

        print(self.url)
        result = requests.get(self.url)
        if result.status_code != 200:
            return None

        soup = BeautifulSoup(result.content, "html.parser")
        title = soup.find('title').text
        
        ##print(soup) ## Utile per capire che diavolo sta parsando
        ##1. header is never used --> simplify the code
        ##header = soup.find("div", class_="descriptionProgramma")
        ##2. I don't care for description or image
        ##description = header.find(class_='textDescriptionProgramma').text
        ##image = urljoin(self.url, soup.find(class_='imgHomeProgramma')['src'])
        ##print ("Download collection image...")
        ##urllib.request.urlretrieve (image, "tmp/" + finalfilename + ".jpg")
        
        finalfilename = str(title).strip().replace(' ', '_')
        finalfilename = re.sub(r'(?u)[^-\w.]', '', finalfilename)    
        print ("Starting download for \"" + title + "\"")               

        
        allelements = soup.find_all(['li','div'])
        print ("Download single MP3s...")
        elementID = 1
        for element in allelements:
            if element.has_attr('data-mediapolis') and element.has_attr('data-title'):				
                mp3 = url = urljoin(self.url, element['data-mediapolis'])
                singletitle = element['data-title']
                singletitle = re.sub(r'(?u)[^-\w.]', '', singletitle)                   
                filename = str(elementID).zfill(2) + "_"  + str(title).strip().replace(' ', '_')
                filename = re.sub(r'(?u)[^-\w.]', '', filename)                   
                elementID = elementID + 1
                print ("Download \"" + singletitle + "\" (" + mp3 + ")")
                #if "Sinfonian.7" in singletitle: #This is in case, for some reason, you need only 1 file
                #    self.getFile(mp3, "tmp/" + singletitle + ".mp3")
                self.getFile(mp3, "tmp/" + singletitle + ".mp3")

        print ("Done!\nFiles saved in ./tmp/ --> Move them or they will be removed next time you run this code.")
        
def main():
    print ("""
 ____       _ ____  _             
|  _ \ __ _(_)  _ \| | __ _ _   _ 
| |_) / _` | | |_) | |/ _` | | | |
|  _ < (_| | |  __/| | (_| | |_| |
|_| \_\__,_|_|_|   |_|\__,_|\__, |
       Downloader           |___/     
 ---------------------------------
 Proudly developed by Andrea Fortuna
 andrea@andreafortuna.org
 https://www.andreafortuna.org
    """)
    if len(sys.argv) < 2:
        print('Need a url')
        exit(2)
        
    getPodcast = Raipodcast(sys.argv[1])
    getPodcast.process('.')
    
if __name__ == '__main__':
    main()
