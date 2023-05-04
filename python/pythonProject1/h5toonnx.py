# h5 to pb
import tensorflow as tf
import os

model = tf.keras.models.load_model("C:\\Users\\Kiot\\Desktop\\eyes\\model.h5", compile=False)
model.save('./model', save_format="tf")

# pb to onnx

os.system('python -m tf2onnx.convert --saved-model ./model/ --output model.onnx  --opset 13')