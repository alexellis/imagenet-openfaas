## ImageNet for OpenFaaS

This function packages the ImageNet library trained on the Inception V3 model which is bundled with TensorFlow 2.0.

You can adapt the code to load other pre-trained models for serving and scaling over HTTP/REST.

![Example](https://pbs.twimg.com/media/FaxxLMxX0AIBXP_?format=jpg&name=medium)
> Example with image from WWF being classified

Requires:

* AMD64/Intel Operating System and CPU
* Or 64-bit ARM Operating System like Ubuntu 22.04

```bash
faas-cli deploy

curl -d https://upload.wikimedia.org/wikipedia/commons/6/61/Humpback_Whale_underwater_shot.jpg \
  http://127.0.0.1:8080/function/imagenet
```

Sample output:

```json
[                                                                                                                                              
  {                                                                                                                                            
    "name": "sea_lion",                                                                                                                        
    "score": "0.7445793"                                                                                                                       
  },                                                                                                                                           
  {                                                                                                                                            
    "name": "great_white_shark",                                                                                                               
    "score": "0.16700004"
  },
  {
    "name": "grey_whale",
    "score": "0.029751772"
  }
]
```

To get the timing, run `curl -i` and look for the header:

```
X-Duration-Seconds: 0.189897
```

Asynchronous invocations are also supported, with a Callback-Url if you want to capture the result:

```bash
curl -d https://upload.wikimedia.org/wikipedia/commons/6/61/Humpback_Whale_underwater_shot.jpg \
  -H "X-Callback-Url: https://http.bin/example" \
  http://127.0.0.1:8080/async-function/imagenet
```

