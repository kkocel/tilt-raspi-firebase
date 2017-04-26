# tilt-raspi-firebase
Python software that is aimed to run on a Raspberry Pi to access Tilt Data and store it in Firebase Database.

## Prerequisites

1. Raspberry Pi with Bluetooth LE support - tested on _B3_ but _Zero W_ should be ok.
2. [Tilt Hydrometer](https://tilthydrometer.com/products/brewometer).

![Raspberry Pi and Tilt Hydrometer immersed in water](.git/img/tilt.jpg?raw=true "Raspberry Pi and Tilt Hydrometer immersed in water")

## Installation

1. Install latest [raspian](https://www.raspberrypi.org/downloads/raspbian/).
2. Install following components:
```shell
sudo apt-get install python-dev
sudo apt-get install libbluetooth-dev
sudo pip3 install pybluez
sudo pip3 install pyrebase
```
3. Grab [blescan.py](https://raw.githubusercontent.com/kkocel/tilt-raspi-firebase/master/blescan.py), [tiltblescan.py](https://raw.githubusercontent.com/kkocel/tilt-raspi-firebase/master/tiltblescan.py) and [firebasesend.py](https://raw.githubusercontent.com/kkocel/tilt-raspi-firebase/master/firebasesend.py) using _wget_ or similar software.
4. Configure [Firebase](https://console.firebase.google.com/)
   1. Create a project.
   2. Import initial database structure:
      ```json
      {
        "batch" : 1,
        "calibration" : {
          "sg" : 0.006,
          "temperature" : 0
        },
        "measurements" : []
      }
      ```
   3. From [service accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) create key in json format and put it in same directory as `.py` files.
   4. Update configuration section in `firebasesend.py` file:
   ```python
   config = {
     "apiKey": "apiKey",
     "authDomain": "projectId.firebaseapp.com",
     "databaseURL": "https://databaseName.firebaseio.com",
     "storageBucket": "projectId.appspot.com",
     "serviceAccount": "path/to/serviceAccountCredentials.json"
   }
   ```
   
   Where: 
   
   `apiKey` and `projectId` can be found in Firebase project settings.
   
   `databaseURL` can be found in `Database` section in Firebase console.
   
   `serviceAccountCredentials.json` is previously generated key in json format. Keep in mind to provide full path here in order to run this script periodically by _cron_.

## Running and automating

If everything was configured properly run:
```bash
sudo python3 tiltblescan.py
```

Output should be similar to:
```bash
temp correction: 0 sg correction: 0.006 batch: 1
temp F: 84 sg uncal: 1036
temp C: 28.89 sg: 1.042 plato: 10.48
```

Before putting Tilt into fermenter remember to [calibrate](#Calibration), then to sanitize it and set appropriate batch number in your Firebase DB.

### Cron

Collecting data from tilt hydrometer and saving it in Firebase can be automated using `cron`.

Eg. To run script for every five minutes edit crontab file by calling `crontab -e` and add following line"
```
*/5 * * * * sudo /usr/bin/python /home/pi/firebasesend.py
```

## Calibration

In order to get best measurements tilt hydrometer needs to be calibrated before putting it into fermenter. 

### SG Calibration

Put tilt hydrometer in water and read SG using provided [mobile application](https://tilthydrometer.com/pages/app). 

If SG differs from 1.000 then put appropriate value in `calibration > sg` section in your Firebase DB. 

Eg. For `0.996` put `0.004` as offset that would be added to measurement.

### Temperature Calibration

After about 10 minutes in water you can calibrate temperature. Use electronic thermometer and similarly put offset value in `calibration > temperature`.

## Storing and reading data

This script stores each measurement on a path in Firebase: `measurements/1/1492706249`.

In above case `1` is a batch number and `1492706249` is an unix timestamp in GMT. 

Every measurement has two values - plato degrees and temperature in celesius:

```json
  "1492706249" : {
    "plato" : "10.48",
    "temp" : "28.89"
  }
```

**IMPORTANT!** Remember to update batch number before each fermentation process. Failing to do so will result in data inconsistency in your database.

## Acknowledgements

Bluetooth scanning and parsing data from tilt is based on code from: https://github.com/jimmayhugh/TiltRPi

Thanks to https://github.com/mjarco for porting ble scanner to python3
