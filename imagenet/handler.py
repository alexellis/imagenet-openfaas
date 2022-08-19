
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions
import numpy as np
import tensorflow as tf   
import requests
import os, tempfile
import json

# import the models for further classification experiments
from tensorflow.keras.applications import (
        # vgg16
        resnet50,
        # mobilenet,
        #inception_v3
    )

# tf.logging.set_verbosity(tf.logging.ERROR)
tf.get_logger().setLevel('ERROR')

model = resnet50.ResNet50(weights='imagenet')

def handle(event, context):
    url = event.body
    r = requests.get(url)

    import os, tempfile
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        tmp_file.write(r.content)
    finally:
        tmp_file.close()

    image = load_img(tmp_file.name, target_size=(224, 224))
    input_arr = img_to_array(image)
    batch = np.array([input_arr])  # Convert single image to a batch.

    processed_image = resnet50.preprocess_input(batch.copy())
    predictions = model.predict(processed_image)
    label_vgg = decode_predictions(predictions)

    res = []
    for prediction_id in range(len(label_vgg[0])):
        res.append({"name": str(label_vgg[0][prediction_id][1]), "score": str(label_vgg[0][prediction_id][2])})

    os.unlink(tmp_file.name)
    return {
        "statusCode": 200,
        "body": json.dumps(res)
    }

