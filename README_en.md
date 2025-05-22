# Baseline

[简体中文](README.md) | English

Baseline Usage:
```bash
bash run.sh
```

docker: <br/>
Driver Version: 560.35.03<br/>
```bash
docker pull registry.cn-hangzhou.aliyuncs.com/clg_test/ai:1.0
```

## Challenge Specifications<br/>
## Contest Rules
1) The project development directory must be located in the /workspace/I2VModelAcceleration/ directory. The startup script should be named run.sh. In the submitted image, use evaluate.py and generate_videos.py from the baseline, maintaining consistency with the baseline. The test data directory structure should also match the baseline.<br/>
2) Do not include test data in the uploaded image. Avoid uploading models related to I2V.py in the baseline. If other models are used, their directory names should not be in the same path as the original I2V.py.<br/>
3) The platform allows submitting images via image addresses. Push your local image to Alibaba Cloud Container Registry or Dockerhub, set it as a public image, and enter the image address on the competition platform's submission page. The platform will pull and run the image, and results can be checked on the results page after execution. When pushing to Alibaba Cloud Container Registry or Dockerhub, avoid using competition - related terms in the image repository name to prevent leakage.<br/>
4) No network access is available within the container when running the image. Install all dependent software and packages in the image.<br/>
5) To allocate resources fairly, the average generation time per video should not exceed 10 minutes. Exceeding this limit will automatically stop the program, and results will not be accepted.<br/>
6) Try to keep the Docker image size under 25G. It is recommended to use example images or images from the pytorch/pytorch:2.x.x-cuda1x.x-cudnn8-devel series.<br/>
7) Do not generate static or near - static videos, as this will invalidate your results.<br/>
8) Refer to the baseline data for formatting requirements. Use a fixed generation seed of 42 when generating videos.<br/>
<br/>



## Computation Resources<br/>
CPU: 16 cores <br/>
Memory: 64GB <br/>
GPU: 24GB (NVIDIA GeForce RTX 4090)<br/>
<br/>


## Alibaba Cloud Docker Registry(Recommend):<br/>
1. Create Your Account and select individual account: https://cr.console.aliyun.com/ap-southeast-1/instances.<br/>
2. select [Instance of Personal Edition] and select [Create ACR Personal Edition].<br/>
3. select [Create Repository]. Create Namespace and Repository Name, and select Public Repository type, and choose [Local Repository].<br/>
4. Log in to Alibaba Cloud Docker Registry Locally:<br/>
```bash
$ docker login --username=[accountId] registry-intl.ap-southeast-1.aliyuncs.com
$ docker tag [ImageId] registry-intl.ap-southeast-1.aliyuncs.com/[namespace]/[repositoryName]:[tag]
$ docker push registry-intl.ap-southeast-1.aliyuncs.com/[namespace]/[repositoryName]:[tag]
Please replace the [accountId], [namespace], [repositoryName], [ImageId] and [tag] parameters based on your image.
```
5. submit your image: registry-intl.ap-southeast-1.aliyuncs.com/[namespace]/[repositoryName]:[tag].<br/>

## Reference <br/>
This baseline is mainly inspired by [DiffSynth-Studio](https://github.com/modelscope/DiffSynth-Studio/tree/main/examples/wanvideo) and [VBench](https://github.com/Vchitect/VBench/tree/master/vbench2_beta_i2v).
<br/>