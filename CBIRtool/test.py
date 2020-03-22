from transformer import PIL
from extractor import Resnet
#from encoder import Faiss
t = PIL.transform('./sample/13_left.jpeg')
e = Resnet.extract(t,'cpu')

print(e)

# Faiss.construct(e,10,"./encoder/index/10dim.index")

# print(Faiss.search(e,"./encoder/index/10dim.index",1))
