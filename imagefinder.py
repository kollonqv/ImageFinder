import requests
import urllib.request
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

def downloadImages(url, imageFolder, iteration):
    if not os.path.exists(imageFolder):
        os.mkdir(imageFolder)
    fileName = imageFolder + "\\" + str(iteration) + "_" + url.split("/")[-1]
    print("Image found: " + url)
    print("File name: " + fileName)
    urllib.request.urlretrieve(url, fileName)

def getImages(url):
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    print(tqdm(soup.find_all("img")))
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        imageUrl = img.attrs.get("src")
        if not imageUrl:
            continue
        imageUrl = urllib.parse.urljoin(url, imageUrl)
        try:
            r = requests.get(imageUrl)
        except requests.exceptions.InvalidSchema:
            continue
        if r.status_code is 200:
            urls.append(imageUrl)
    return urls

def createFile(images, filename):
    f = open(filename,"w+")
    for i in range(len(images)):
        f.write(images[i] + "\n")
    f.close()

def askUrl():
    defaultUrl = "https://www.f-secure.com/en/home"
    url = input("Please enter an url from which to search images \nIf you want to search images from the default location: " + defaultUrl + ", just press ENTER\n")
    if url is '':
        url = defaultUrl
    return url

def main():
    url = askUrl()
    images = getImages(url)
    i = 1
    for img in images:
        downloadImages(img,"images", i)
        i += 1
    createFile(images, "images.txt")

if __name__== "__main__":
    main()
