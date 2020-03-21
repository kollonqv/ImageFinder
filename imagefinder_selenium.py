import requests
import urllib.request
import os
from selenium import webdriver

def getImagesWithSelenium(url):
    driverPath = "C:\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driverPath)
    urls = []
    driver.get(url)
    allImages = driver.find_elements_by_tag_name("img")
    for image in allImages:
        imageUrl = image.get_attribute("src")
        try:
            r = requests.get(imageUrl)
        except requests.exceptions.InvalidSchema:
            continue
        if r.status_code is 200:
            urls.append(imageUrl)
    driver.close()
    return urls

def downloadImages(url, imageFolder, iteration):
    if not os.path.exists(imageFolder):
        os.mkdir(imageFolder)
    fileName = os.path.join(imageFolder, url.split("/")[-1])
    fileName = imageFolder + "\\" + str(iteration) + "_" + url.split("/")[-1]
    print("Image found: " + url)
    print("File name: " + fileName)
    urllib.request.urlretrieve(url, fileName)

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
    images = getImagesWithSelenium(url)
    i = 1
    for img in images:
        downloadImages(img,"images", i)
        i += 1
    createFile(images, "images.txt")

if __name__== "__main__":
    main()
