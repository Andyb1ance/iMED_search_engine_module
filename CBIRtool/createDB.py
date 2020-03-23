from transformer import PIL
from extractor import Resnet
from encoder import Faiss
import os

def createDB(imageFolder,indexFile):
    images = os.walk(imageFolder)
    e = resnet()
    temp = list()
    for path,dir_list,file_list in images:
        for img in file_list:
            t = PIL.transform(img)
            temp.append(e.extract(t,'cpu'))

    Faiss.construct(temp,temp[0].size,indexFile)
    ##加上insert图片的语句..不过faiss是从0自增,可能需要调整.    
    