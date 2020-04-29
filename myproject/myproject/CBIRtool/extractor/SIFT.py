import cv2
import numpy as np
import os 
def sift_extractor(file_path):
    '''
    Description: extract \emph{sift} feature from given image
    Input: file_path - image path
    Output: des - a list of descriptors of all the keypoint from the image
    '''
    img = cv2.imread(file_path)
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    _,des = sift.detectAndCompute(gray,None) 

    return des

#KMeans
def get_cluster_center(des_set, K):
    '''
    Description: cluter using a default setting
    Input: des_set - cluster data
                 K - the number of cluster center
    Output: laber  - a np array of the nearest center for each cluster data
            center - a np array of the K cluster center
    '''
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.01)
    des_set = np.float32(des_set)
    ret, label, center = cv2.kmeans(des_set, K, None, criteria, 3, cv2.KMEANS_RANDOM_CENTERS)
    return label, center

def get_codebook(all_des, K):
    '''
    Description: train the codebook from all of the descriptors
    Input: all_des - training data for the codebook
                 K - the column of the codebook
    '''
    label, center = get_cluster_center(all_des, K)
    return label, center

def get_pic_vlad(des, codebook):
    '''
    Description: get the vlad vector of each image
    '''
    vlad = np.zeros(shape=[32, 128])
    for each in des:
        min_dist = 1000000000.0
        ind = 0
        for i in range(32):
            dist = cal_vec_dist(each, codebook[i])
            if dist < min_dist:
                min_dist = dist
                ind = i
        vlad[ind] += each - codebook[ind]
    
    vlad_norm = vlad.copy()
    cv2.normalize(vlad, vlad_norm, 1.0, 0.0, cv2.NORM_L2)
    vlad_norm = vlad_norm.reshape(32 * 128, -1)
    
    return vlad_norm
def cal_vec_dist(vec1, vec2):
    '''
    Description: calculate the Euclidean Distance of two vectors
    '''
    return np.linalg.norm(vec1 - vec2)
class Extractor:
    def __init__(self,device=None):
        self.codebook = None
    def load(self):
        pass
    def train(self,images):
        descriptors = list()
        for each in images:
            descriptors.extend(sift_extractor(each))
        label,codebook = get_codebook(descriptors,32)
        np.save('sift.npy',codebook[1])
    def extract(self,img):
        # img = Image.open(img)
        # img = img.resize((256,256))
        # img = img.convert("RGB")
        # img = transforms.ToTensor()(img)
        # img = img.unsqueeze(0)
        if not self.codebook:
            self.codebook = np.load('sift.npy')
        des = sift_extractor(img)
        out = get_pic_vlad(des,self.codebook)
        return out

e = Extractor()
folder = '../sample'
filelist = os.listdir(folder)
for i,v in enumerate(filelist):
    filelist[i]=os.path.join(folder,v)
e.train(filelist)
print(e.extract('../sample/10_left.jpeg'))