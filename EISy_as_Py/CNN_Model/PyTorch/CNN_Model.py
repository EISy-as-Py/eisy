# Import necessary package
# The basic python package
import numpy as np
import matplotlib.pyplot as plt
import skimage
#from scipy.misc import imread
from IPython import display
from PIL import Image
from skimage.transform import rescale
%matplotlib inline

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
