import serial

ser = serial.Serial('/dev/ttyACM0')
ser.baudrate=115200

while True:
    ser_bytes = ser.readline()
    ser_string = ser_bytes.decode("utf-8")
    ser_list = ser_string.split(",")

    if int(ser_list[0]) == 0:
        x1 = int(ser_list[1])
    else:
        x1 = 120

    if ser_list[2] == '0':
        x2 = int(ser_list[3])
    else:
        x2 = 120

    if ser_list[4] == '0':
        x3 = int(ser_list[5])
    else:
        x3 = 120

    if ser_list[6] == '0':
        x4 = int(ser_list[7])
    else:
        x4 = 120

    print(x1,x2,x3,x4)

