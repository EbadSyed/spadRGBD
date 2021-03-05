import serial

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate=115200

tanTheta = 0.4434

while True:
    ser_bytes = ser.readline()
    ser_string = ser_bytes.decode("utf-8")
    ser_list = ser_string.split(",")

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

    y1 = int(x1 * tanTheta)
    y2 = int(x2 * tanTheta)
    y3 = int(x3 * tanTheta)
    y4 = int(x4 * tanTheta)

    print(x1,x2,x3,x4)
    print(y1,y2,y3,y4)
