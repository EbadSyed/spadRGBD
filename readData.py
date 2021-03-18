import serial
import os
import torch.optim
import numpy as np
import matplotlib.pyplot as plt
import dataloaders.transforms as transforms

model_path = '/home/ebad/sparse-to-dense.pytorch/results/d20/model_best.pth.tar'

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 115200
ser.timeout = 1

tanTheta = 0.4434

iheight, iwidth = 630, 630  # raw image size
output_size = (228, 304)

transform = transforms.Compose([
    transforms.Resize(240.0 / iheight),
    transforms.CenterCrop(output_size),
])

baseMat = np.zeros((5,5))

np.set_printoptions(threshold=np.inf)

to_tensor = transforms.ToTensor()

assert os.path.isfile(model_path), "=> no best model found at '{}'".format(model_path)
print("=> loading best model '{}'".format(model_path))
checkpoint = torch.load(model_path)
output_directory = os.path.dirname(model_path)
args = checkpoint['args']
start_epoch = checkpoint['epoch'] + 1
best_result = checkpoint['best_result']
model = checkpoint['model']
print("=> loaded best model (epoch {})".format(checkpoint['epoch']))

while True:
    ser.flushInput()
    ser.flushOutput()

    ser_bytes = ser.readline()
    ser_string = ser_bytes.decode("utf-8")
    ser_list = ser_string.split(",")

    try:
        if int(ser_list[0]) == 0:
            x1 = int(ser_list[1])
            if x1 > 113:
                x1 = 113
        else:
            x1 = 113

        if ser_list[2] == '0':
            x2 = int(ser_list[3])
            if x2 > 113:
                x2 = 113
        else:
            x2 = 113

        if ser_list[4] == '0':
            x3 = int(ser_list[5])
            if x3 > 113:
                x3 = 113
        else:
            x3 = 113

        if ser_list[6] == '0':
            x4 = int(ser_list[7])
            if x4 > 113:
                x4 = 113
        else:
            x4 = 113

        data = np.zeros((228,304))

        data[57, 76] = x2
        data[171, 76] = x1
        data[57, 228] = x4
        data[171, 228] = x3

        depth_tensor = to_tensor(data)
        depth_tensor = depth_tensor.unsqueeze(0)
        depth_tensor = depth_tensor.unsqueeze(0)

        input = depth_tensor.cuda()

        torch.cuda.synchronize()

        with torch.no_grad():
            pred = model(input)

        torch.cuda.synchronize()

        pred = np.squeeze(pred.cpu().numpy())
        print(pred.shape)
        a1 = pred[51:63, 70:82]
        print(a1.shape)
        a2 = pred[165:177, 70:82]
        print(a2.shape)
        a3 = pred[51:63, 170:182]
        print(a3.shape)
        a4 = pred[165:177, 170:182]
        print(a4.shape)

        a1a2 = np.concatenate([a1, a2], axis=1)
        a3a4 = np.concatenate([a3, a4], axis=1)

        result_combined = np.concatenate([a1a2, a3a4])

        plt.imshow(pred, cmap='magma', vmin=10, vmax=113)
        plt.colorbar(fraction=0.1, pad=0.04)
        plt.waitforbuttonpress()
        plt.close()
    except:
        print("Input Garbage")
