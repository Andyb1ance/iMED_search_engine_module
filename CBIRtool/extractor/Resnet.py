from torchvision import transforms
import torchvision.models as models
import torch
def extract(img,device):
    img = transforms.ToTensor()(img)
    img = img.unsqueeze(0)
    model = models.resnet34(num_classes=10).to(device)
    with torch.no_grad():
        img.to(device)
        #print("img to device successful")
        out = model(img)

    return out


