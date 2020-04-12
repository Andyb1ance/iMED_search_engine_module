#import faiss
import numpy as np

'''
the input of faiss should be numpy
'''
def transform(vectors):
        #transform list of vectors to numpy
        return np.array(vectors,dtype=float).astype('float32')

class Encoder:

    def __init__(self,device):
        self.device = device
    def construct(self,vectors,Dimension,indexFile):
        # if self.device == 'gpu':
        #     res = faiss.StandardGpuResources()
        #     index = faiss.index_cpu_to_gpu(res, 0, index)
        # assert type(vectors)==list
        vectors = transform(vectors)
        vectors = np.squeeze(vectors)
        print(vectors.shape)    
        index=faiss.IndexFlatL2(Dimension)
        index.add(vectors)
        with open(indexFile,'w') as file:
    	    file.write('')
        faiss.write_index(index, indexFile)
        return index


    def update(self,vectors,indexFile):
        pass
    def search(self,vector,indexFile,k):
        vector = transform(vector) 
        index = faiss.read_index(indexFile)
        D, I = index.search(vector, k)
        return D,I




