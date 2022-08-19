
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions
import numpy as np
import tensorflow as tf   
import requests
import os, tempfile, io
import json
import shutil

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
    # The URL is in the request body
    url = event.body

    image_path = ""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        with requests.get(url, stream=True) as res:
            try:
                shutil.copyfileobj(res.raw, f)
                image_path = f.name
            finally:
                f.close()

    # Fetch the image from the URL
    r = requests.get(url, timeout=10)

    # Some images may not download correctly, or could result in a 404
    if r.status_code == 200:
        image = None
        try:
            image = load_img(image_path, target_size=(224, 224))
        except Exception as err:
            print(err)
            return {
                "statusCode": "500",
                "body": err
            }

        input_arr = img_to_array(image)
        batch = np.array([input_arr])  # Convert single image to a batch.

        processed_image = resnet50.preprocess_input(batch.copy())
        predictions = model.predict(processed_image)
        label_vgg = decode_predictions(predictions)

        res = []
        for prediction_id in range(len(label_vgg[0])):
            res.append({"name": str(label_vgg[0][prediction_id][1]), "score": str(label_vgg[0][prediction_id][2])})

        os.unlink(image_path)
        return {
            "statusCode": 200,
            "body": json.dumps(res),
            "headers": {
               "Content-Type": "application/json"
            }  
        }
    else:
        return {
            "statusCode": r.status_code,
            "body": r.content
        }
