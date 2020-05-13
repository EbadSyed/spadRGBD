import cv2
import numpy as np
import h5py

import skimage.io as io

import dataloaders.transforms as transforms
np.set_printoptions(threshold=np.inf)

iheight, iwidth = 480, 640 # raw image size
output_size = (228, 304)

num_samples = 20
max_depth = np.inf


path1 = '/home/ebad/sparse-to-dense.pytorch/data/nyudepthv2/train/cafe_0001a/00001.h5'


def h5_loader(path):
    h5f = h5py.File(path, "r")
    rgb_image = np.array(h5f['rgb'])

    rgb_image = np.transpose(rgb_image, (1, 2, 0))
    depth = np.array(h5f['depth'])
    np.savetxt("foo.csv", depth, delimiter=",")

    return rgb_image, depth


def dense_to_sparse(depth):
    """
    Samples pixels with `num_samples`/#pixels probability in `depth`.
    Only pixels with a maximum depth of `max_depth` are considered.
    If no `max_depth` is given, samples in all pixels
    """
    print("Depth Type",type(depth),depth.size,depth.shape[0])

    vert = int(depth.shape[0]/20)
    horz = int(depth.shape[1]/20)

    sparse_array = np.zeros(depth.shape)

    for x in range(20):
        for y in range(20):
            sparse_array[x*vert,y*horz] = depth[x*vert,y*horz]

    return sparse_array
    # mask_keep = depth > 0
    # if max_depth is not np.inf:
    #     mask_keep = np.bitwise_and(mask_keep, depth <= max_depth)
    # n_keep = np.count_nonzero(mask_keep)
    # if n_keep == 0:
    #     io.imshow(mask_keep, interpolation='nearest')
    #     io.show()
    #     return mask_keep
    # else:
    #     prob = float(num_samples) / n_keep
    #     io.imshow(np.bitwise_and(mask_keep, np.random.uniform(0, 1, depth.shape) < prob), interpolation='nearest')
    #     io.show()
    #     return np.bitwise_and(mask_keep, np.random.uniform(0, 1, depth.shape) < prob)


rgb1, depth1 = h5_loader(path1)
depth_sparse = dense_to_sparse(depth1)
io.imshow(depth_sparse,interpolation='nearest')
io.show()

print(np.amax(depth_sparse))

io.imshow(depth1)
# io.imshow(rgb1/255)
io.show()

# cv2.imshow('', rgb1)
# cv2.waitKey()

