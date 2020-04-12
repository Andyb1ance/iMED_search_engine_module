import CBIRtool
a = CBIRtool.frame.Framework("Resnet34","Faiss",'./CBIRtool/encoder/index/sample.index')
p = a.construct('./sample')
print(p)
print(a.search('./sample/10_left.jpeg'))
