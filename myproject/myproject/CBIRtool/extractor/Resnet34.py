from torchvision import transforms
import torchvision.models as models
import torch
from PIL import Image
class Extractor:
    def __init__(self,device):
        self.device = device
        self.model = models.resnet34(pretrained = True).to(self.device)
    def load(self):
        pass
    def extract(self,img):
        img = Image.open(img)
        img = img.resize((256,256))
        img = img.convert("RGB")
        img = transforms.ToTensor()(img)
        img = img.unsqueeze(0)
        with torch.no_grad():
            img.to(self.device)
            #print("img to device successful")
            out = self.model(img)
        return out.numpy()
        


