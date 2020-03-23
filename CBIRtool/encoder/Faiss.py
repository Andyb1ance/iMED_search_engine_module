import faiss
import numpy as np

'''
the input of faiss should be numpy
'''
def transform(vectors):
    #transform list of vectors to numpy
    return np.array(vectors,dtype=float).astype('float32')

def construct(vectors,Dimension,indexFile,GPU=False):
    # if GPU:
    #     res = faiss.StandardGpuResources()
    #     index = faiss.index_cpu_to_gpu(res, 0, index)
    #assert type(vectors)==list
    vectors = transform(vectors)
    print(vectors)    
    index=faiss.IndexFlatIP(Dimension)
    index.add(vectors)
    with open(indexFile,'w') as file:
    	file.write('')
    faiss.write_index(index, indexFile)
    return index


def update(vectors,indexFile):
    pass
def search(vector,indexFile,k,GPU = False):
    vector = transform(vector) 
    index = faiss.read_index(indexFile)
    D, I = index.search(vector, k)
    return D,I




