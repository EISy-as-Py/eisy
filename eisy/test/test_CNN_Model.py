import os
import cv2
from tqdm import tqdm

import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import unittest

import cnn.Neural_Network.CNN_Model as CNN

class TestCNNModelTools(unittest.TestCase):
	def test_DataImporter_Training():
		train_d = CNN.EISDataImport.DataImporter_Training(self, k, 
														  path_List_training,
	                              						  image_width, 
	                              						  image_height)
		assert k == len(path_List_training) - 1, 'Incorrect number of type'
		assert k <= 7, 'Too many types.'
		assert type(path_List_training) == list, \
			'path_List_training should be a list'
		assert image_width <= 1000, 'Image size is too large'
		assert image_height <= 1000, 'Image size is too large'

	def test_DataImporter_Predict():
		predict_d = CNN.EISDataImport.DataImporter_Predict(self, k, 
														  path_List_predict,
	                              						  image_width, 
	                              						  image_height)
		assert k == len(path_List_training) - 1, 'Incorrect number of type'
		assert k <= 10 , 'Too many folders/paths.'
		assert type(path_List_training) == list, \
			'path_List_predict should be a list'
		assert image_width <= 1000, 'Image size is too large.'
		assert image_height <= 1000, 'Image size is too large.'

	def test_Build_Data():
		Build_d = CNN.Build_Data(Training, Predict, k, path_list, 
								 image_width, image_height)
		assert Training != Predict, 'Build only one type of data in one time.'
		if Training is True:
			assert k <= 7, 'Too many types.'
		if Predict is True:
			assert k <= 10, 'Too many folders/paths.'
		assert k == len(path_list) - 1, 'Incorrect number of type.'
		assert type(path_list) == list, 'path_list should be a list.'
		assert image_width <= 1000, 'Image size is too large.'
		assert image_height <= 1000, 'Image size is too large.'

	def test_load_array_data():
		load_array_d = CNN.load_training_data(np_ndarray_file)
		assert type(np_ndarray_file) == str, \
			'Wrong type. The np_ndarray_file should be a string.'

	def test_data_information()
