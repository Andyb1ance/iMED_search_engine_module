import CBIRtool
import os

a = CBIRtool.frame.Framework("Resnet34","Faiss",'./CBIRtool/encoder/index/sample.index')
os.chdir('./sample')
a.construct(os.listdir())

print(a.search('./sample/10_left.jpeg',3))
