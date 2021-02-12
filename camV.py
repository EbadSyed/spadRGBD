import pyrealsense2 as rs
import numpy as np
import cv2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import skimage.io as io

from time import sleep

# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe = rs.pipeline()

# Build config object and stream everything
cfg = rs.config()

# Enable streams you are interested in
cfg.enable_stream(rs.stream.pose)
cfg.enable_stream(rs.stream.fisheye, 1)
cfg.enable_stream(rs.stream.fisheye, 2)

# Start streaming
pipe.start(cfg)

try:
    for _ in range(10):
        frames = pipe.wait_for_frames()

        # Left fisheye camera frame
        left = frames.get_fisheye_frame(1)
        left_data = np.asanyarray(left.get_data())

        # Right fisheye camera frame
        right = frames.get_fisheye_frame(2)
        right_data = np.asanyarray(right.get_data())

        fig = plt.figure(figsize=[40.0, 30.0])

        plt.subplot(121)
        plt.imshow(left_data, cmap='gray', vmin=0, vmax=255)
        plt.subplot(122)
        plt.imshow(right_data, cmap='gray', vmin=0, vmax=255)

        plt.waitforbuttonpress(timeout=2)
        plt.close()


        print('Left frame', left_data.shape)
        print('Right frame', right_data.shape)

        # Positional data frame
        pose = frames.get_pose_frame()
        if pose:
            pose_data = pose.get_pose_data()
            print('\nFrame number: ', pose.frame_number)
            print('Position: ', pose_data.translation)
            print('Velocity: ', pose_data.velocity)
            print('Acceleration: ', pose_data.acceleration)
            print('Rotation: ', pose_data.rotation)
finally:
    pipe.stop()
