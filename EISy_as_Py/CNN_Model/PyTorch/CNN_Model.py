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
    
    MD = "Nyquist/Missing" # Determine the number of type and then give the directory of each type of image
    SP = "Nyquist/SinglePeak"
    TP = "Nyquist/TwoPeaks"
    # TL = "Nyquist/Tail"
    LABELS = {MD:0, SP:1, TP:2 }
    training_data = []
    mdcount = 0
    spcount = 0
    tpcount = 0
    #tlcount = 0
    
    def make_training_data(self):
    	"""Take the data from assigned file and transfrom images into array."""
    	"""Also, categorize the labeled training data."""
        for label in self.LABELS: #iterate the directory
            print(label)
            for f in tqdm(os.listdir(label)): # iterate all the image within the directory, f -> the file name
                path = os.path.join(label, f) # get the full path to the image
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE) # convert the iimage to gray scale (optional)
                img = rescale(img, 0.15)
                self.training_data.append([np.array(img), np.eye(3)[self.LABELS[label]]])                 

                if label == self.MD:
                    self.mdcount += 1
                elif label == self.SP:
                    self.spcount += 1
                elif label == self.TP:
                    self.tpcount += 1
                #elif label == self.TL:
                    #self.tlcount += 1    
                
        np.random.shuffle(self.training_data)
        np.save("eis_training_data.npy", self.training_data)
        print("Missing:", self.mdcount)
        print("SinglePeak:", self.spcount)
        print("TwoPeaks:", self.tpcount)
        #print("Tail:", self.tlcount)
        
if REBUILD_DATA:
    Type = EISType()
    Type.make_training_data()
    
