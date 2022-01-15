# -*- coding: utf-8 -*-
from driver import led, mpu6050
import RPi.GPIO as Pin
import time as utime
import math
import tool.filter

# ==========================================================
# Constants setting
# ==========================================================
# GPIO mode(Dummy)
Pin.setmode(Pin.BCM)

# Zero point adjust button pin(Dummy)
ADJUST_START_PIN = Pin.setup(16, Pin.IN, pull_up_down=Pin.PUD_DOWN)

# Sampling frequency
SAMPLING_HZ = 100

# Maximum display period(sec)
RETENTION_SECONDS = 60 * 10

# Saved data size
DATA_SIZE = SAMPLING_HZ

# InvenSense MPU-6050 Six-Axis (Gyro + Accelerometer) I2C
ACC = mpu6050.mpu6050(0x68)

# LED setting(Dummy)
LED = led.Led()

# Frequency filter
FILTER = tool.filter.Filter(SAMPLING_HZ)


# ==========================================================
# Variable setting
# ==========================================================
# Data from A/D
row_data = [[0] * DATA_SIZE, [0] * DATA_SIZE, [0] * DATA_SIZE]

# Adjusted data
offsetted_data = [[0] * DATA_SIZE, [0] * DATA_SIZE, [0] * DATA_SIZE]

# Filterd data
filtered_data = [[0.0] * DATA_SIZE, [0.0] * DATA_SIZE, [0.0] * DATA_SIZE]
__composite_gal = [0.0] * DATA_SIZE

# 3-axis adjust value
offset = [0.0, 0.0, 0.0]

# Adujusting time( offset_counter / sampling rate = sec)
offset_counter = DATA_SIZE * 5

# The system is adjusted
is_offsetted = False

# Seismic intensity class
sic = 0

# Latest Seismic intensity class and time
latest_sic = 0
latest_time = utime.time()

# Loop counter
frame = 0


def get_seismic_intensity_class(scale: float):
    """
    Scale to seismic intensity class
    """
    if 6.5 <= scale:
        return 9
    elif 6.0 <= scale:
        return 8
    elif 5.5 <= scale:
        return 7
    elif 5.0 <= scale:
        return 6
    elif 4.5 <= scale:
        return 5
    elif 3.5 <= scale:
        return 4
    elif 2.5 <= scale:
        return 3
    elif 1.5 <= scale:
        return 2
    elif 0.5 <= scale:
        return 1
    else:
        return 0


def read_acceleration(axis: int):
    # Read 3-axis data from acceleration sensor
    accel_data = ACC.get_accel_data()
    if axis == 0:
      a = accel_data['x']
    if axis == 1:
      a = accel_data['y']
    if axis == 2:
      a = accel_data['z']

    index = frame % len(row_data[axis])

    # Remove outliers
    if 0 < a < 4096 and a != 1024 and a != 2048 and a != 3072:
        row_data[axis][index] = a
    else:
        row_data[axis][index] = int(offset[axis])

    # Set offset value if not adjusted.
    if is_offsetted == False:
        offset[axis] = sum(row_data[axis]) / len(row_data[axis])
    offsetted_data[axis][index] = int(row_data[axis][index] - offset[axis])


def set_filtered_data(axis: int):
    # Calculate with the latest 5 frames.
    offsetted_dataset = [0.0] * 5
    for i in range(len(offsetted_dataset)):
        index = (frame - len(offsetted_dataset) + i + 1) % len(row_data[axis])
        # G to Gal.
        # offsetted_dataset[i] = offsetted_data[axis][index] / 1024 * 980
        offsetted_dataset[i] = offsetted_data[axis][index] * 100
    index = frame % len(row_data[axis])
    filtered_data[axis][index] = FILTER.exec(offsetted_dataset).pop()


def set_composite_gal():
    # Vector composition of 3-axis data
    index = frame % len(filtered_data[0])
    __composite_gal[index] = math.sqrt(
        filtered_data[0][index] ** 2 +
        filtered_data[1][index] ** 2 +
        filtered_data[2][index] ** 2
    )


# ==========================================================
# Main
# ==========================================================
print("START")
LED.wakeup()
while True:
    start_time = utime.time_ns()

    # read 3-axis data
    for axis in range(3):
        read_acceleration(axis)
        set_filtered_data(axis)
    set_composite_gal()

    # LED updated every second
    if frame % SAMPLING_HZ == 0:
        __gal = sorted(__composite_gal)[-int(SAMPLING_HZ * 0.3)]
        print("Gal:", __gal)
        if 0 < __gal:
            scale = round(2.0 * math.log10(__gal) + 0.94, 2)
            sic = get_seismic_intensity_class(scale)
            print("SIC:", scale, "(", sic, ")")

            # Record seismic intensity.
            if is_offsetted and (latest_time < utime.time() - RETENTION_SECONDS or latest_sic <= sic):
                latest_time = utime.time()
                latest_sic = sic

            # Turn on LEDs
            if is_offsetted:
                LED.brink_scale(sic, latest_sic)

        else:
            LED.clear()
    elif frame % (SAMPLING_HZ/4) == 0 and sic < latest_sic and is_offsetted:
        # Blink the LED corresponding to the seismic intensity of past earthquakes.
        LED.toggle(latest_sic)
    elif is_offsetted == False:
        # Make the LED wave during zero point correction.
        v = int(offset_counter * 100 / (SAMPLING_HZ * 5)) % 10
        LED.brink_scale(v, v)

    # Initialize the frame after 60 seconds
    if SAMPLING_HZ * 60 <= frame:
        frame = 0

    frame += 1
    current_time = utime.time_ns()
    sleep_time = 1 / SAMPLING_HZ - (current_time - start_time)/1000000.0
    if 0 < sleep_time:
        utime.sleep(sleep_time)

    if offset_counter <= 0 and is_offsetted == False:
        is_offsetted = True
        print("offset complete!!")
    elif 0 < offset_counter:
        offset_counter -= 1

    if 0 == 1 and is_offsetted:
        # When the zero point adjust button is pressed, the correction is started.
        is_offsetted = False
        offset_counter = SAMPLING_HZ * 5
        latest_time = utime.time()
        latest_sic = 0
        print("offset start!!")
