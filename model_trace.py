import tvm
from tvm import relay

import h5py

import os
import numpy as np

import torch
import torchvision

import dataloaders.transforms as transforms

path1 = '/home/ebad/spadRGBD/data/nyudepthv2/train/cafe_0001a/00001.h5'
model_path = '/home/ebad/spadRGBD/results/rgbd40/model_best.pth.tar'

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

    print("Points",points)

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

points = 40

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

rgbd = create_rgbd(rgb2, depth2)

input_tensor = to_tensor(rgbd)
input_tensor = input_tensor.unsqueeze(0)

depth_tensor = to_tensor(depth_sparse)
depth_tensor = depth_tensor.unsqueeze(0)
depth_tensor = depth_tensor.unsqueeze(0)

print("Input Tensor",input_tensor.shape)
print("Depth Tensor",depth_tensor.shape)


model = model.eval()
scripted_model = torch.jit.trace(model, input_tensor.cuda()).eval()

print(scripted_model.graph)


torch.jit.save(scripted_model,"/home/ebad/spadRGBD/modelrgbd40.pt")