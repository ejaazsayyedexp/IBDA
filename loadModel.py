from tensorflow.keras.models import model_from_json

def loadModel():
    model_path = './assets/model_json.json'
    model_weights = './assets/model_weights.h5'
    file = open(model_path,"r")
    model_json = file.read()
    file.close()

    model = model_from_json(model_json)
    model.load_weights(model_weights)

    return model
