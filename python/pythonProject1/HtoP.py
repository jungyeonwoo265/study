from tensorflow import keras

model = keras.models.load_model("C:\\Users\\Kiot\\Desktop\\eyes\\model.h5", compile=False)

export_path = 'C:\\Users\\Kiot\\Desktop\\PB'
model.save(export_path, save_format='tf')