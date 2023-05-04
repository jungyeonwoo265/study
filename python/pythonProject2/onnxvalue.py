#  onnx 모델에 대한 예상 입력및 출력 세무 정보 가져오기
from tensorflow.python.client import session
import json
import onnxruntime

# labels_file = "automl_models/labels.json"
# with open(labels_file) as f:
#     classes = json.load(f)
# print(classes)
try:
    session = onnxruntime.InferenceSession("model.onnx")
    print("ONNX model loaded...")
except Exception as e:
    print("Error loading ONNX file: ", str(e))


sess_input = session.get_inputs()
sess_output = session.get_outputs()
print(f"No. of inputs : {len(sess_input)}, No. of outputs : {len(sess_output)}")

for idx, input_ in enumerate(range(len(sess_input))):
    input_name = sess_input[input_].name
    input_shape = sess_input[input_].shape
    input_type = sess_input[input_].type
    print(f"{idx} Input name : { input_name }, Input shape : {input_shape}, \
    Input type  : {input_type}")

for idx, output in enumerate(range(len(sess_output))):
    output_name = sess_output[output].name
    output_shape = sess_output[output].shape
    output_type = sess_output[output].type
    print(f" {idx} Output name : {output_name}, Output shape : {output_shape}, \
    Output type  : {output_type}")

