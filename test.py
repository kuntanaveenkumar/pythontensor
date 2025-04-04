import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import os


transform = transforms.Compose([
    transforms.Resize((128, 128)),  # Resize images to 128x128
    transforms.ToTensor(),  # Convert to tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize
])


train_data = datasets.ImageFolder('./train', transform=transform)
test_data = datasets.ImageFolder('./test', transform=transform)

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
test_loader = DataLoader(test_data, batch_size=32, shuffle=False)


class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)  
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16 * 64 * 64, 128)  
        self.fc2 = nn.Linear(128, len(train_data.classes))  

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = x.view(-1, 16 * 64 * 64)  
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleCNN()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

criterion = nn.CrossEntropyLoss()  
optimizer = optim.Adam(model.parameters(), lr=0.001)


num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {running_loss/len(train_loader)}, Accuracy: {100*correct/total}%")


model.eval()  
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"Test Accuracy: {100 * correct / total}%")


torch.save(model.state_dict(), "image_classification_model.pth")
print("Model saved successfully!")


# model = SimpleCNN()
# model.load_state_dict(torch.load("image_classification_model.pth"))
# model.eval()


# from PIL import Image
# import requests

# image_path = './truck.png'
# img = Image.open(image_path)
# img = transform(img).unsqueeze(0).to(device)

# model.eval()
# with torch.no_grad():
#     output = model(img)
#     _, predicted_class = torch.max(output, 1)

# predicted_class_name = train_data.classes[predicted_class.item()]
# print(f"Predicted Class: {predicted_class_name}")

# # 9. Visualize the Results (Optional)
# def show_image(image_path):
#     img = Image.open(image_path)
#     plt.imshow(img)
#     plt.show()

# show_image(image_path)
import torch
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt

# Load the trained model
model = SimpleCNN()
model.load_state_dict(torch.load("./image_classification_model.pth"), strict=False)
model.eval()

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define the image transformation
transform = transforms.Compose([
    transforms.Resize((128, 128)),  # Match input size used in training
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
])

# Load and preprocess the image
image_path = './2015-honda-civic-lx.jpg'
img = Image.open(image_path).convert('RGB')
img = transform(img).unsqueeze(0).to(device)

# Predict the class
model.eval()
with torch.no_grad():
    output = model(img)
    _, predicted_class = torch.max(output, 1)


class_names = ['class_1', 'class_2', 'class_3', 'class_4', 'class_5', 'class_6', 'class_7'] 
predicted_class_name = class_names[predicted_class.item()]
print(f"Predicted Class: {predicted_class_name}")

# Optional: Visualize the image
def show_image(image_path):
    img = Image.open(image_path)
    plt.imshow(img)
    plt.axis('off') 
    plt.show()

show_image(image_path)
