import cv2
import numpy as np
from tensorflow.keras.preprocessing import image

def preprocess_image(img_path):
  img = cv2.imread(img_path,cv2.COLOR_BGR2RGB)
  img = cv2.resize(img,(200,200),interpolation=cv2.INTER_AREA)
  img = image.img_to_array(img)
  img = np.expand_dims(img,axis=0)
  img/=255.
  return img