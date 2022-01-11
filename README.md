# FREE WING なんちゃって改造版
ラズパイで動く様にしたつもり  
使用センサ：I2C MPU-6050  
https://github.com/m-rtijn/mpu6050 MIT License使用  

```
sudo raspi-config nonint do_i2c 0

sudo apt-get update
sudo apt-get install -y i2c-tools

# ModuleNotFoundError: No module named 'smbus'
sudo apt-get install python3-smbus

sudo apt-get install -y git

cd
git clone https://github.com/FREEWING-JP/PiDAS
cd PiDAS

python3 main.py
```

```
$ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

# PiDAS (Pinpoint Detection and Alarm System)
PiDASのソースコードです。
このシステムをまとめた同人誌は https://booth.pm/ja/items/3022619

# ドキュメント・キット組立方法など
[こちら](https://nrck.github.io/PiDAS/)
