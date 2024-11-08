import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

class CycloneCNN(nn.Module):
    def __init__(self):
        super(CycloneCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.flattened_size = self._get_flattened_size()
        self.fc1 = nn.Linear(self.flattened_size, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 7) 

    def _get_flattened_size(self):
        with torch.no_grad():
            x = torch.randn(1, 3, 250, 250)
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))
            x = self.pool(F.relu(self.conv3(x)))
            x = self.pool(F.relu(self.conv4(x)))
            return x.numel()

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.pool(F.relu(self.conv4(x)))
        x = x.view(-1, self.flattened_size)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def load_model():
    model = CycloneCNN()
    model.load_state_dict(torch.load("trained_model.pth", map_location=torch.device('cpu')))
    model.eval()
    return model

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((250, 250)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0) 

def predict_cyclone_attributes(image_path):
    model = load_model()
    input_tensor = preprocess_image(image_path)
    with torch.no_grad():
        output = model(input_tensor)
    attributes = {
        "Central Pressure": output[0, 0].item(),
        "Cyclone Intensity": output[0, 1].item(),
        "Eye Diameter": output[0, 2].item(),
        "Rainfall Intensity": output[0, 3].item(),
        "Sea Surface Temperature": output[0, 4].item(),
        "Size (Diameter)": output[0, 5].item(),
    }
    return attributes