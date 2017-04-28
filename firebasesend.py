import tiltblescan
import time
import pyrebase

config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com",
  "serviceAccount": "path/to/serviceAccountCredentials.json"
}
def send_data_for_tilt(current_tilt, temp_and_sg):
        temperature_correction = db.child("calibration/" + current_tilt).child("temperature").get().val()

        temp_in_c_uncalibrated = float((int(temp_and_sg[0]) - 32) * (5/9))
        temp = temp_in_c_uncalibrated + temperature_correction
        temp = "{0:.2f}".format(temp)

        sg_correction = db.child("calibration/" + current_tilt).child("sg").get().val()
        sg = float(temp_and_sg[1]) / 1000 + sg_correction
        plato = (-1 * 616.868) + (1111.14 * sg) - (630.272 * sg**2) + (135.997 * sg**3)
        plato = "{0:.2f}".format(plato)

        batch_no = db.child("batch/" + current_tilt).get().val()
        print("Data for tilt: {}".format(current_tilt))
        print("Temp correction: {}, SG correction: {}, batch: {}".format(temperature_correction, sg_correction,batch_no))
        print("Temp F: {}, SG uncal: {}".format(temp_and_sg[0],temp_and_sg[1]))
        print("Temp C: {}, SG: {} plato: {}".format(temp, sg, plato))

        data = {"temp": temp, "plato": plato}
        db.child("measurements").child(current_tilt + "/" + str(batch_no)).child(int(time.time())).set(data)

        
db = pyrebase.initialize_app(config).database()

devices = db.child("aliases").get()

devices_addresses = [device.key() for device in devices.each()]
devices_aliases = [device.val() for device in devices.each()]

devices_to_skip = []

for scan_result in tiltblescan.print_beacons():
    result_split = scan_result.split(",")
    
    device_addr = result_split[0]
    
    if device_addr in devices_to_skip:
        continue
    
    if device_addr in devices_addresses:
        devices_to_skip.append(device_addr)
        temp_and_sg = result_split[2:4]
        device_alias = devices_aliases[devices_addresses.index(device_addr)]
        
        if int(temp_and_sg[1]) > 900 and int(temp_and_sg[1]) < 1200:
            send_data_for_tilt(device_alias, temp_and_sg)
