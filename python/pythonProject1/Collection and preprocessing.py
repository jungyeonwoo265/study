# 데이터 수집 및 전처리
import os
import cv2
import numpy as np

date_dir = "C:\\Users\\Kiot\\Desktop\\train"

imb_size = (224, 224)
num_frames = 16
classes = ['Closed', 'Open']

data = []
for i, cls in enumerate(classes):
    class_dir = os.path.join(date_dir, cls)
    for filename in os.listdir(class_dir):
        file_path = os.path.join(class_dir, filename)
        cap = cv2.VideoCapture(file_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # print(classes[i], ": ", frame_count)
        if frame_count < num_frames:
            continue
        frames = []
        for j in range(num_frames):
            frame_idx = int(frame_count/num_frames * j)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            frame = cv2.resize(frame, imb_size)
            print(f"{filename}: {j} : {len(frame)}")
            frames.append(frame)
        data.append({'class': i, 'frames': frames})
        cap.release()

x = np.array([np.array(d['frames']) for d in data])
y = np.array([d['class'] for d in data])

# 데이터 분할
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 모델 구성
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense

model = Sequential()

# Convolutional layer 1
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(img_size[0], img_size[1], 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Convolutional layer 2
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Convolutional layer 3
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Flatten the output from convolutional layers
model.add(Flatten())

# Fully connected layer
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))

# Output layer with 5 neurons for 5 dance classes
model.add(Dense(5, activation='softmax'))

# Compile the model with categorical_crossentropy loss function and adam optimizer
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Print the model summary
model.summary()
