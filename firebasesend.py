import tiltblescan
import time
import pyrebase

temp_and_sg = tiltblescan.extract_temp_and_sg()

config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com",
  "serviceAccount": "path/to/serviceAccountCredentials.json"
}

db = pyrebase.initialize_app(config).database()

temperature_correction = db.child("calibration").child("temperature").get().val()

temp_in_c_uncalibrated = float((int(temp_and_sg[0]) - 32) * (5/9))
temp = temp_in_c_uncalibrated + temperature_correction
temp = "{0:.2f}".format(temp)

sg_correction = db.child("calibration").child("sg").get().val()
sg = float(temp_and_sg[1]) / 1000 + sg_correction
plato = (-1 * 616.868) + (1111.14 * sg) - (630.272 * sg**2) + (135.997 * sg**3)
plato = "{0:.2f}".format(plato)

batch_no = db.child("batch").get().val()
print("temp correction: {} sg correction: {} batch: {}".format(temperature_correction,sg_correction,batch_no))
print("temp F: {} sg uncal: {}".format(temp_and_sg[0],temp_and_sg[1]))
print("temp C: {} sg: {} plato: {}".format(temp, sg, plato))

data = {"temp": temp, "plato": plato}
db.child("measurements").child(batch_no).child(int(time.time())).set(data)