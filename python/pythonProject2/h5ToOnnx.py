# h5 to pb
import tensorflow as tf
import os

model = tf.keras.models.load_model("C:\\Users\\Kiot\\Desktop\\ebd\\jyw_model.h5", compile=False)
model.save('./model', save_format="tf")

# pb to onnx
# tf2onnx 패키지 설치 할것
os.system('python -m tf2onnx.convert --saved-model ./model/ --output jyw_model.onnx  --opset 13')