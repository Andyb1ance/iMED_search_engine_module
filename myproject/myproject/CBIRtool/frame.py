import CBIRtool
import os
class Framework:
    def __init__(self,extractor,encoder,indexFile,device = 'cpu'):
        self.extractor = CBIRtool.extractor.select[extractor](device)
        self.encoder = CBIRtool.encoder.select[encoder](device)
        self.indexFile = indexFile
    def construct(self,file_list):
        for img in file_list:
            #extract feature and store in list 'temp'
            temp.append(self.extractor.extract(img))
        #construct the index
        self.encoder.construct(temp,self.indexFile)
        return 
    def search(self,imagePath,k):
        distance,index = self.encoder.search(self.extractor.extract(imagePath),self.indexFile,k)
        return index[0]

# ##加上insert图片的语句..不过faiss是从0自增,可能需要调整.
# conn = psycopg2.connect(database="test", user="lee", password="666666", host="127.0.0.1", port="5432") 
# cur = conn.cursor()
# for img in fileList:
#     with open(os.path.join(imageFolder,img),'rb') as f:
#         image = f.read()
#     sql = "insert into imgTable (img) values ({})".format(psycopg2.Binary(image))
#     cur.execute(sql)
# conn.commit()
