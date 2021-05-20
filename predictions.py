from preprocess import preprocess_image
import numpy as np


def makePredictions(model, img_path,classes:list):
    image = preprocess_image(img_path)
    predic = model.predict(image)
    index = np.argmax(predic)
    return classes[index]