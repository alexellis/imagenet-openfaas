
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions
import numpy as np
import tensorflow as tf   
import requests
import os, tempfile, io, time
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

    startDL = time.time()
    image_path = ""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        headers = {"User-Agent": "imagenet-openfaas (+https://github.com/alexellis/imagenet-openfaas)"}
        with requests.get(url, stream=True, timeout=10, headers=headers) as res:
            try:
                shutil.copyfileobj(res.raw, f)
                image_path = f.name
            finally:
                f.close()

            # Some images may not download correctly, or could result in a 404
            if res.status_code == 200:
                if res.headers['Content-Type'] != None and not res.headers['Content-Type'] in ('image/jpeg','image/png'):
                    return {
                        "statusCode": "400",
                        "body": "bad image mime type {}".format(res.headers['Content-Type'] )
                    }

                image = None
                try:
                    image = load_img(image_path, target_size=(224, 224))
                except Exception as err:
                    print(err)
                    return {
                        "statusCode": "500",
                        "body": "can't load image: {}".format(err)
                    }

                dlDuration = time.time() - startDL

                inferStart = time.time()
                input_arr = img_to_array(image)
                batch = np.array([input_arr])  # Convert single image to a batch.

                processed_image = resnet50.preprocess_input(batch.copy())
                predictions = model.predict(processed_image)
                label_vgg = decode_predictions(predictions)

                results = []
                for prediction_id in range(len(label_vgg[0])):
                    results.append({"name": str(label_vgg[0][prediction_id][1]), "score": str(label_vgg[0][prediction_id][2])})
                
                inferDuration = time.time() - inferStart

                try:
                    os.unlink(image_path)
                except Exception as err:
                    print("Unable to remove {} error {}".format(image_path, err))

                return {
                    "statusCode": 200,
                    "body": json.dumps(results),
                    "headers": {
                    "Content-Type": "application/json",
                    "X-Download-Time": "{:.2f}".format(dlDuration),
                    "X-Inference-Time": "{:.2f}".format(inferDuration)
                    }  
                }
            else:
                return {
                    "statusCode": res.status_code,
                    "body": res.content
                }
