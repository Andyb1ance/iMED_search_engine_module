from torchvision import transforms
import torchvision.models as models
import torch

class resnet:
    def __init__(self,device):
        self.device = device
        self.model = models.resnet34(pretrained = True).to(self.device)
    def extract(self,img):
        img = transforms.ToTensor()(img)
        img = img.unsqueeze(0)
        with torch.no_grad():
            img.to(self.device)
            #print("img to device successful")
            out = self.model(img)
        return out
    


