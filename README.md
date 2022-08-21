# FREE WING なんちゃって改造版
ラズパイで動く様にした  
使用センサ：I2C MPU-6050  
https://github.com/m-rtijn/mpu6050 MIT License使用  

#### 関連記事
Raspberry Piと加速度センサーを使って地震計を作る、PiDAS for Raspberry Pi、I2Cの MPU-6050使用  
http://www.neko.ne.jp/~freewing/raspberry_pi/raspberry_pi_i2c_mpu6050_pidas_seismic_meter/  
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
```
pi@raspberrypi:~ $ cd PiDAS/
pi@raspberrypi:~/PiDAS $ python3 main.py
START
Gal: 0.0
Gal: 117.67322626350727
SIC: 5.08 ( 6 )
Gal: 0.0
Gal: 0.0
Gal: 0.0
Gal: 0.0
offset complete!!
Gal: 0.0
Gal: 0.0
Gal: 0.0
Gal: 0.0
Gal: 2.2084558413024364
SIC: 1.63 ( 2 )
Gal: 8.17165624281887
SIC: 2.76 ( 3 )
Gal: 37.252011153579
SIC: 4.08 ( 4 )
Gal: 159.87605720011197
SIC: 5.35 ( 6 )
Gal: 177.7918478913437
SIC: 5.44 ( 6 )
Gal: 128.48526056987734
SIC: 5.16 ( 6 )
Gal: 90.78479066655287
SIC: 4.86 ( 5 )
```

# PiDAS (Pinpoint Detection and Alarm System)
PiDASのソースコードです。

このシステムをまとめた同人誌は https://booth.pm/ja/items/3022619 で購入できます。


# ドキュメント・キット組立方法など
[こちら](https://nrck.github.io/PiDAS/)
