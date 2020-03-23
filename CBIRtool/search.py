from transformer import PIL
from extractor import Resnet
from encoder import Faiss


def search(imagePath,indexFile):
    
    e = Resnet.resnet('cpu')
    t = PIL.transform(imagePath)
    Faiss.search(e.extract(t),indexFile,5)