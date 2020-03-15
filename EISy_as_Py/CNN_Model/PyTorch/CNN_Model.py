# Import necessary package

# The basic python package
import numpy as np
import matplotlib.pyplot as plt
import skimage
# from scipy.misc import imread
from IPython import display
from PIL import Image
from skimage.transform import rescale

# The processing package
import os
import cv2
from tqdm import tqdm

# The torch package
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
from torchvision import transforms, datasets
from torch.utils.data import DataLoader

# Data Pre-Processing

REBUILD_DATA = True

class EISType():

    MD = "Nyquist/Missing"  # Determine the number of type and then give the directory of each type of image
    SP = "Nyquist/SinglePeak"
    TP = "Nyquist/TwoPeaks"
    # TL = "Nyquist/Tail"
    LABELS = {MD: 0, SP: 1, TP: 2}
    training_data = []
    mdcount = 0
    spcount = 0
    tpcount = 0
    # tlcount = 0
    
    def make_training_data(self):
        """
        Take the data from assigned file and transfrom images into array.
        Also, categorize the labeled training data.
        """
        for label in self.LABELS:  # iterate the directory
            print(label)
            for f in tqdm(os.listdir(label)):  # iterate all the image within the directory, f -> the file name
                path = os.path.join(label, f)  # get the full path to the image
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # convert the iimage to gray scale (optional)
                img = rescale(img, 0.15)
                self.training_data.append([np.array(img), np.eye(3)[self.LABELS[label]]])

                if label == self.MD:
                    self.mdcount += 1
                elif label == self.SP:
                    self.spcount += 1
                elif label == self.TP:
                    self.tpcount += 1
                # elif label == self.TL:
                    # self.tlcount += 1
                
        np.random.shuffle(self.training_data)
        np.save("eis_training_data.npy", self.training_data)
        print("Missing:", self.mdcount)
        print("SinglePeak:", self.spcount)
        print("TwoPeaks:", self.tpcount)
        # print("Tail:", self.tlcount)
        
if REBUILD_DATA:
    Type = EISType()
    Type.make_training_data()    


def load_training_data(training_data):
    """Load the data to check if all the images have been in the program."""
    training_data = np.load("eis_training_data.npy", allow_pickle = True)
    return training_data

def data_information(training_data, k):
    """Check the size of image and dataset."""
    print("Size of training_data:", len(training_data))
    print("Size of image:", training_data[k][0].shape[0], "x" ,training_data[k][0].shape[1])

def ploting_data(training_data, k):
    """Showing the assigned image."""
    plt.imshow(training_data[k][0])
    plt.show

def Neuron_Calculation(numConvLayer, width, height, firstHidden, kernel, poolSize):
    """Calculating how many neurons we need for the output of last convolutional layer"""
    size = [0, 0, 0]
    for i in range(numConvLayer):
        width = int((width - kernel + 1) / poolSize)
        height = int((height - kernel + 1) / poolSize)
        size[0] = width
        size[1] = height
        size[2] = firstHidden*(2**i)

    print(size)
    total = size[0]*size[1]*size[2]
    return total

# Convolutional Neural Network Model
class Net(nn.Module):
    
    def __init__(self, input_size, firstHidden, kernel_size, output_size):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(input_size, firstHidden, kernel_size) 
        self.conv2 = nn.Conv2d(firstHidden, firstHidden*2, kernel_size)
        self.conv3 = nn.Conv2d(firstHidden*2, firstHidden*4, kernel_size)
        self.conv4 = nn.Conv2d(firstHidden*4, firstHidden*8, kernel_size)
        
        self.fc1 = nn.Linear(7296, 64) 
        self.fc2 = nn.Linear(64, output_size)

    def convs(self, ):




   
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2,2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2,2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2,2))
        x = F.max_pool2d(F.relu(self.conv4(x)), (2,2))
        
        xF = x.view(-1, 64 * 19 * 6 ) # flatten
        output = F.relu(self.fc1(xF)) # put into the first fully connected layer
        output = self.fc2(output)
        
        return F.softmax(output, dim=1)

def image_to_tensor(training_data, image_height, image_width):
    """Transform the array image into tensor."""
    X = torch.Tensor([i[0] for i in training_data]).view(-1, image_height, image_width)
    return X

def type_to_tensor(training_data):
    """Transform the array type into tensor."""
    y = torch.Tensor([i[1] for i in training_data])
    return y

def data_separation(data, ratio_of_testing, TRAIN):
    """Separate the training and testing data."""
    VAL_PCT = ratio_of_testing
    val_size = int(len(X)*VAL_PCT)

    if TRAIN = True:
        train_data = data[:-val_size]
        print("Training Samples:", len(train_data))
        return train_data
    test_data = data[-val_size:]
    print("Testing Samples:", len(test_data))
    return test_data

def learning(train_data1, train_data2, image_width, image_height, learning_rate, BATCH_SIZE, EPOCHS):
    """ """
    optimizer = optim.Adam(net.parameter(), lr = learning_rate)
    loss_function = nn.MSELoss()

    for epoch in range(EPOCHS):
        for i in tqdm(range(0, len(train_data1), BATCH_SIZE)):
            batch_data1 = train_data1[i:i+BATCH_SIZE].view(-1, 1, image_height, image_width)
            batch_data2 = train_data2[i:i+BATCH_SIZE]

            net.zero_grad()
            outputs = net(batch_data1)
            loss = loss_function(outputs, batch_data2)
            loss.backward()
            optimizer.step()
            
        print(loss)


