import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import time

# Set up device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define transformations for the training set
train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load the ImageNet training dataset
train_dataset = datasets.ImageFolder(root='/home/cc/imagenet-mini/train', transform=train_transforms)
train_loader = DataLoader(train_dataset, batch_size=400, shuffle=True, num_workers=32)

# Load the pre-trained ResNet-50 model
model = models.resnet50(pretrained=True)

# Modify the final fully connected layer to match the number of classes in ImageNet (1000 classes)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 1000)

# Move the model to the appropriate device (GPU or CPU)
model = model.to(device)

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

# Training loop
num_epochs = 1
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    data_transfer_time = 0.0
    computation_time = 0.0
    
    for inputs, labels in train_loader:
        # Measure data transfer time from CPU to GPU
        start_event = torch.cuda.Event(enable_timing=True)
        end_event = torch.cuda.Event(enable_timing=True)
        
        start_event.record()
        inputs, labels = inputs.to(device), labels.to(device)
        end_event.record()
        torch.cuda.synchronize()  # Wait for the events to be recorded
        
        batch_transfer_time = start_event.elapsed_time(end_event)  # Time in milliseconds
        data_transfer_time += batch_transfer_time

        # Zero the parameter gradients
        optimizer.zero_grad()

        # Measure computation time on GPU
        start_event.record()
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()
        end_event.record()
        torch.cuda.synchronize()

        batch_computation_time = start_event.elapsed_time(end_event)  # Time in milliseconds
        computation_time += batch_computation_time

        running_loss += loss.item()

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}')
    print(f'Total Data Transfer Time (s): {data_transfer_time/1000:.2f}')
    print(f'Total Computation Time (s): {computation_time/1000:.2f}')

print('Training complete.')