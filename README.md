# tilt-raspi-firebase
Python software that is aimed to run on a Raspberry Pi to access Tilt Data and store it in Firebase Database.

## Prerequisites

1. Raspberry Pi with Bluetooth LE support - tested on _B3_ but _Zero W_ should be ok.
2. [Tilt Hydrometer](https://tilthydrometer.com/products/brewometer).

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
   1. Create a project
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
   3. From [service accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) create key in json format and put it in same directory as `.py` files
   4. Update configuration in `firebasesend.py` file
   ```python
   config = {
     "apiKey": "apiKey",
     "authDomain": "projectId.firebaseapp.com",
     "databaseURL": "https://databaseName.firebaseio.com",
     "storageBucket": "projectId.appspot.com",
     "serviceAccount": "path/to/serviceAccountCredentials.json"
   }
   ```

sudo python tiltblescan.py
