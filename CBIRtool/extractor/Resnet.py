from torchvision import transforms
import torchvision.models as models
import torch

class resnet:
    def __init__(self):
        self.model = models.resnet34(pretrained = True).to(device)
    def extract(self,img,device):
        img = transforms.ToTensor()(img)
        img = img.unsqueeze(0)
        with torch.no_grad():
            img.to(device)
            #print("img to device successful")
            out = self.model(img)
        return out
    


