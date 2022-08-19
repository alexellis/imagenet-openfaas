## ImageNet for OpenFaaS

This function requires a PC and does not work on a Raspberry Pi.

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

