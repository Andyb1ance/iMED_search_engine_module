import CBIRtool
import os

a = CBIRtool.frame.Framework("Resnet34","Faiss",'./CBIRtool/encoder/index/sample.index')
folder = './sample'
filelist = os.listdir(folder)
for i,v in enumerate(filelist):
    filelist[i]=os.path.join(folder,v)
a.construct(filelist)

print(a.search('./sample/10_left.jpeg',3))
