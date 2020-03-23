from PIL import Image

def transform(imagePath:str):
    
#     transform = transforms.Compose([
#                 transforms.Resize([256,256])
# #               transforms.ToTensor()
# #            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
#     ])

    
    img = Image.open(imagePath)
    img = img.resize((256,256))
    #print(img.size,img.mode)
    img = img.convert("RGB")
    return img

    
