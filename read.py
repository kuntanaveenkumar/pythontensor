import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms


class SimpleCNN(nn.Module):
    def __init__(self, num_classes=2):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 16 * 16, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

pretrained_dict = torch.load('image_classification_model.pth')
for key, value in pretrained_dict.items():
    print(key, value.shape)
    
model = SimpleCNN(num_classes=2)


model.load_state_dict(torch.load("./image_classification_model.pth",weights_only=None), strict=False)


model.eval()


# image_path = "./truck.png"
# image = Image.open(image_path)


# transform = transforms.Compose(
#     [
#         transforms.Resize((64, 64)),
#         transforms.ToTensor(),
#     ]
# )


# image_tensor = transform(image)


# image_tensor = image_tensor.unsqueeze(0)


# print(f"Image tensor shape: {image_tensor.shape}")

input_image = torch.randn(1, 3, 64, 64)
output = model(input_image)

print(output)
