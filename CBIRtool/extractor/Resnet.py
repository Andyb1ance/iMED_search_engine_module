from torchvision import transforms
import torchvision.models as models
import torch

class resnet:
    def __init__():
        self.model = models.resnet34(pretrained=True,num_classes=10).to(device)
    def extract(img,device):
        img = transforms.ToTensor()(img)
        img = img.unsqueeze(0)
        with torch.no_grad():
            img.to(device)
            #print("img to device successful")
            out = self.model(img)
        return out
    


