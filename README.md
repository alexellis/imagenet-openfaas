## ImageNet for OpenFaaS

This function requires a PC and does not work on a Raspberry Pi.

```bash
faas-cli deploy

curl -d https://upload.wikimedia.org/wikipedia/commons/6/61/Humpback_Whale_underwater_shot.jpg \
  http://127.0.0.1:8080/function/imagenet
```

