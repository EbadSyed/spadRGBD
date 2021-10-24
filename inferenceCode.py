import os
import time
import csv
import numpy as np

import torch
import torch.backends.cudnn as cudnn
import torch.optim

from models import ResNet
from metrics import AverageMeter, Result
from dataloaders.dense_to_sparse import UniformSampling, SimulatedStereo
import criteria
import utils
import h5py

import skimage.io as io
# import matplotlib.pyplot as plt

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from PIL import Image

import dataloaders.transforms as transforms

rgbdMode = False

points = 8

path1 = '/home/ebad/spadRGBD/data/nyudepthv2/train/cafe_0001a/00001.h5'

if rgbdMode:
    model_path = '/home/ebad/spadRGBD/results/rgbd8/model_best.pth.tar'
else:
    model_path = '/home/ebad/spadRGBD/results/d8/model_best.pth.tar'


iheight, iwidth = 480, 640  # raw image size
output_size = (228, 304)

to_tensor = transforms.ToTensor()


def h5_loader(path):
    h5f = h5py.File(path, "r")
    rgb_image = np.array(h5f['rgb'])

    rgb_image = np.transpose(rgb_image, (1, 2, 0))
    depth = np.array(h5f['depth'])

    return rgb_image, depth


def dense_to_sparse(depth):
    """
    Samples pixels with `num_samples`/#pixels probability in `depth`.
    Only pixels with a maximum depth of `max_depth` are considered.
    If no `max_depth` is given, samples in all pixels
    """

    vert = int(depth.shape[0] / points)
    horz = int(depth.shape[1] / points)

    # if vert%2 != 0:
    #     vert = vert - 1
    # if horz%2 != 0:
    #     horz = horz - 1
    # print("Vertical",vert)
    # print("Horizontal", horz)
    sparse_array = np.zeros(depth.shape)

    for x in range(points):
        for y in range(points):
            # print(x,y)
            sparse_array[int(((x + 1) * vert) - vert/2), int(((y + 1) * horz) - horz/2)] = depth[int(((x + 1) * vert) - vert/2), int(((y + 1) * horz)/2)]

    return sparse_array


def val_transform(rgb, depth):
    depth_np = depth
    transform = transforms.Compose([
        transforms.Resize(240.0 / iheight),
        transforms.CenterCrop(output_size),
    ])
    rgb_np = transform(rgb)
    rgb_np = np.asfarray(rgb_np, dtype='float') / 255
    depth_np = transform(depth_np)

    return rgb_np, depth_np


def create_rgbd(rgb, depth):
    sparse_depth = dense_to_sparse(depth)
    rgbd = np.append(rgb, np.expand_dims(sparse_depth, axis=2), axis=2)
    return rgbd


assert os.path.isfile(model_path), "=> no best model found at '{}'".format(model_path)
print("=> loading best model '{}'".format(model_path))
checkpoint = torch.load(model_path)
output_directory = os.path.dirname(model_path)
args = checkpoint['args']
start_epoch = checkpoint['epoch'] + 1
best_result = checkpoint['best_result']
model = checkpoint['model']
print("=> loaded best model (epoch {})".format(checkpoint['epoch']))

rgb1, depth1 = h5_loader(path1)

rgb2, depth2 = val_transform(rgb1, depth1)

depth_sparse = dense_to_sparse(depth2)

plt.figure()
plt.imshow(depth_sparse)

rgbd = create_rgbd(rgb2, depth2)

input_tensor = to_tensor(rgbd)
input_tensor = input_tensor.unsqueeze(0)

depth_tensor = to_tensor(depth_sparse)
depth_tensor = depth_tensor.unsqueeze(0)
depth_tensor = depth_tensor.unsqueeze(0)

if rgbdMode:
    input = input_tensor.cuda()
else:
    input = depth_tensor.cuda()

torch.cuda.synchronize()

with torch.no_grad():
    pred = model(input)

torch.cuda.synchronize()

plt.figure()
plt.imshow(np.squeeze(pred.cpu().numpy()), interpolation='nearest')
plt.colorbar(fraction=0.1, pad=0.04)

plt.figure()
plt.imshow(depth2)

plt.show()

# plt.figure()
# plt.imshow(rgb2)
#
#
# plt.figure()
# plt.imshow(depth_sparse)
#
# plt.show()
