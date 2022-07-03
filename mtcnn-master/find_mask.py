import cv2
import os
import numpy as np
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model = tf.keras.models.load_model('DenseNet121.h5')

img_path = ['./image/withmask.jpg', './image/two_face.jpg']
processed_img = []
prediction = []

for i in range(2):
    img = cv2.cvtColor(cv2.imread(img_path[i]), cv2.COLOR_BGR2RGB)
    processed_img.append(cv2.resize(img, (128, 128)))
    processed_img[i] = np.reshape(processed_img[i], [1, 128, 128, 3])
    processed_img[i] = processed_img[i] / 255.0

    prediction.append(model.predict(processed_img[i]))


print(prediction)