"""Import necessary package"""
import os
import cv2
from tqdm import tqdm

import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import rescale

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


"""Data Import and Pre-Processing"""
REBUILD_DATA = True


class EISType():

    def DataImporter_Training(k, path_list):
        """



        """
    count_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    count = []
    for i in range(len(count_list)):
        count.append(0)
    
    training_data = []
    # Iterate the directory
    for label in range(len(path_list)-1): 
        print(path_list[label])
        # Iterate all the image within the directory, f -> the file name 
        for f in tqdm(os.listdir(path_list[label])): 
            # Get the full path to the image              
            path = os.path.join(path_list[label], f) 
            if "png" in path:
                # Read images in the given path and turn them into nparray.
                # Convert the iimage to gray scale (optional)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 
                img = cv2.resize(img, (800, 536))
                training_data.append([path, np.array(img), np.eye(k)[label]])
                
                for i in range(k):
                    if label == i:
                        count[i] += 1  

    np.random.shuffle(training_data)
    np.save(path_list[-1], training_data)
        
    for i in range(len(path_list)-1):
        print(path_list[i], ":", count[i])

if REBUILD_DATA:
    Type = EISType()
    Type.make_training_data()

"""Data Status Check"""

def load_training_data(np_ndarray_file):
    """
    Load the data from the default file "eis_training_data.npy"
    to check if all the images have been in the program.

    Returns
    ----------
    training_data:  the dataset expressed in numpy array form.
                    type -> numpy.ndarray

    """
    training_data = np.load(np_ndarray_file, allow_pickle=True)
    return training_data


def data_information(training_data):
    """
    Check the size of image and dataset.

    Parameters
    ----------
    training_data: the data loading from "eis_training_data.npy"
    
    """
    print("Size of training_data:", len(training_data))
    print("Size of image(after rescale):", training_data[0][1].shape[1],
          "x", training_data[0][1].shape[0])


def ploting_data(training_data, k):
    """
    Show the assigned image with matplotlib package.

    Parameters
    ----------
    training_data: the data loading from "eis_training_data.npy"
    k:  assign one image in training_data to show.
        k should fall in the range of dataset size.

    """
    print(training_data[k][0])
    plt.imshow(training_data[k][1])
    plt.show


"""Convolutional Neural Network Model"""
class Net(nn.Module):
    
    def __init__(self, input_size, image_width, image_height,
                 firstHidden, kernel_size, output_size):
        """

        Parameters
        ----------
        input_size:
        image_width: The width of input images.
                     this is provided from the data_information function
        image_height: The width of input images.
                     this is provided from the data_information function
        firstHidden: The size of first hidden layer.
                     The size of next layer will be twice of the current layer
                     Ex: 1st is 8, 2nd will be 16, 3rd will be 24 and so on.
                     Number of hidden layer is set as 4 by default.
        kernel_size: It will form a subwindom with size of kernel to scan over
                     the original image.
                     kernel_size must be an odd integer,
                     usually not larger than 7
        output_size: The number of final target category.

        """
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(input_size, firstHidden, kernel_size)
        self.conv2 = nn.Conv2d(firstHidden, firstHidden*2, kernel_size)
        self.conv3 = nn.Conv2d(firstHidden*2, firstHidden*4, kernel_size)
        self.conv4 = nn.Conv2d(firstHidden*4, firstHidden*8, kernel_size)
        
        x = torch.randn(image_height, image_width).view(-1, 1, image_height,
                                                        image_width)
        conv_to_linear = self.last_conv_neuron(x)

        self.fc1 = nn.Linear(conv_to_linear, 64)
        self.fc2 = nn.Linear(64, output_size)

    def last_conv_neuron(x):
        """
        Calculate how many neurons that the last convolutional layer will
        connect to the linear hidden layer

        Parameters
        ----------
        x: a random torch tensor with size (-1, 1, image_height, image_width)
        Ex: x = torch.randn(image_height, image_width
                            ).view(-1, 1, image_height, image_width)
        """
        x = self.convs(x)
        conv_to_linear = x[0].shape[0]*x[0].shape[1]*x[0].shape[2]
        return conv_to_linear

    def convs(self, x):
        """
        Put the image into the convolutional hidden layer. Scan over the
        original image to and use the max pooling function (with size 2) to
        determine the one number to represent the sub-image.

        """
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv4(x)), (2, 2))
        return x
   
    def forward(self, x):
        """ """
        x = self.convs(x)
        conv_to_linear = x[0].shape[0]*x[0].shape[1]*x[0].shape[2]
        # Flatten the data
        xF = x.view(-1, conv_to_linear)
        # put into the first fully connected layer
        output = F.relu(self.fc1(xF))
        output = self.fc2(output)
        return F.softmax(output, dim=1)


def image_to_tensor(training_data, image_height, image_width):
    """Transform the array image into tensor."""
    X = torch.Tensor([i[0] for i in training_data]).view(-1, image_height,
                                                         image_width)
    return X


def type_to_tensor(training_data):
    """Transform the array type into tensor."""
    y = torch.Tensor([i[1] for i in training_data])
    return y


def data_separation(data, ratio_of_testing, TRAIN):
    """Separate the training and testing data."""
    VAL_PCT = ratio_of_testing
    val_size = int(len(data)*VAL_PCT)

    if TRAIN is True:
        train_data = data[:-val_size]
        print("Training Samples:", len(train_data))
        return train_data
    test_data = data[-val_size:]
    print("Testing Samples:", len(test_data))
    return test_data


def learning(train_data1, train_data2, input_size, image_width, image_height,
             firstHidden, kernel_size, output_size, learning_rate, BATCH_SIZE,
             EPOCHS):
    """ 

    """
    optimizer = optim.Adam(Net(input_size, image_width, image_height,
                               firstHidden, kernel_size, output_size
                               ).parameter(), lr=learning_rate)
    loss_function = nn.MSELoss()

    for epoch in range(EPOCHS):
        for i in tqdm(range(0, len(train_data1), BATCH_SIZE)):
            batch_data1 = train_data1[i:i+BATCH_SIZE].view(-1, 1,
                                                           image_height,
                                                           image_width)
            batch_data2 = train_data2[i:i+BATCH_SIZE]

            Net(input_size, image_width, image_height, firstHidden,
                kernel_size, output_size).zero_grad()
            outputs = Net(input_size, image_width, image_height, firstHidden,
                          kernel_size, output_size)(batch_data1)
            loss = loss_function(outputs, batch_data2)
            loss.backward()
            optimizer.step()

        print(loss)


def accuracy(test_data1, test_data2, input_size, image_width, image_height,
             firstHidden, kernel_size, output_size):
    """

    """
    correct = 0
    total = 0
    with torch.no_grad():
        for i in tqdm(range(len(test_data1))):
            real_type = torch.argmax(test_data2[i])
            net_out = Net(input_size, image_width,
                          image_height, firstHidden,
                          kernel_size, output_size
                          )(test_data1[i].view(-1, 1, image_height,
                                               image_width))[0]
            predicted_type = torch.argmax(net_out)

            if predicted_type == real_type:
                correct += 1
            total += 1

    print("Accuracy:", round(correct/total, 3))



