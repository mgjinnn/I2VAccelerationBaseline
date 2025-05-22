# I2VAccelerationBaseline

简体中文 | [English](README_en.md)

用法：
```bash
bash run.sh
```

docker: <br/>
Driver Version: 560.35.03<br/>
```bash
docker pull registry.cn-hangzhou.aliyuncs.com/clg_test/ai:1.0
```

## 参赛规范 <br/>
1) 工程开发目录需要在/workspace/I2VModelAcceleration/目录下, 启动脚本固定使用run.sh, 提交镜像中需使用baseline中的evaluate.py和generate_videos.py, 需保持和baseline一致, 测试数据目录结构保持与baseline一致. <br/>
2) 上传镜像中请勿上传测试数据，和baseline中I2V.py涉及模型，若使用其他模型目录名，请勿与原I2V.py同路径.<br/>
3) 平台提供了基于镜像地址提交镜像的方式, 将本地镜像推送至阿里云容器镜像仓库或者Dockerhub后, 设置为公开镜像, 在比赛平台提交页面中输入镜像地址. 由比赛平台拉取镜像运行, 运行结束即可在成绩页面查询评测结果. 推送至阿里云容器镜像仓库或者Dockerhub时, 镜像仓库名称尽量不关联上比赛相关的词语, 以免被检索从而泄漏.<br/>
4) 运行镜像时，容器内任何网络不可用，请将依赖的软件、包在镜像中装好. <br/>
5) 为了合理分配资源，平均单视频生成时间不超过10分钟，超出后程序自动停止，结果将不被接受.<br/>
6) Docker镜像大小请尽量勿超过25G, 推荐使用示例镜像，或者pytorch/pytorch:2.x.x-cuda1x.x-cudnn8-devel系列镜像.<br/>
7) 请勿生成静态或者趋于静态的视频，否则成绩则无效.<br/>
8) 数据格式请参考baseline中数据，生成视频时请使用固定生成种子42.<br/>
<br/>

## 资源配置：<br/>
CPU: 16核 <br/>
内存: 64 GiB <br/>
GPU: Nvidia RTX 4090, Driver Version: 560.35.03, 显存开销在24G以内 <br/>
<br/>

## 阿里云镜像仓库使用方法:<br/>
1) 注册阿里云账户: https://cr.console.aliyun.com/cn-hangzhou/instances. <br/>
2) 在工作台搜索[容器镜像服务], 进入后选择[个人实例]. <br/>
3) 创建镜像仓库、命名空间, 设置仓库名称，选择公开或私有仓库(此处选择公开),  选择本地仓库. <br/>
4) 本地登录阿里云Docker Registry示例: <br/>
```bash
$ docker login --username=[阿里云id] registry.cn-hangzhou.aliyuncs.com
$ docker tag [ImageId] registry.cn-hangzhou.aliyuncs.com/xx1/xx2:[镜像版本号]
$ docker push registry.cn-hangzhou.aliyuncs.com/xx1/xx2:[镜像版本号]
请根据实际镜像信息替换示例中的[阿里云id], [ImageId]和[镜像版本号]参数.
```
5) 在比赛提交页面提交: registry.cn-hangzhou.aliyuncs.com/xx1/xx2:[镜像版本号].
<br/>

## Reference <br/>
This baseline is mainly inspired by [DiffSynth-Studio](https://github.com/modelscope/DiffSynth-Studio/tree/main/examples/wanvideo) and [VBench](https://github.com/Vchitect/VBench/tree/master/vbench2_beta_i2v).
<br/>