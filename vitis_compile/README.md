# DECENT DNNC Batch Processing

## 说明

用于在服务器vitis docker container内批量定点编译caffe模型并发送给DPU板子测latency，配合[Auto Deploy部署工具](https://gitlab.novauto.com.cn/toolchain/auto_deploy)使用。

功能：

1. 批量编译source文件夹内的caffe模型，生成`.elf`文件
2. 将`.elf`文件发送给板子，运行部署和测试latency的程序
3. 接收latency结果txt文件，并存在results文件夹中

## 使用方法

需要在docker container内运行，工具会调用vitis对模型进行定点编译。

使用的docker image如下：
```bash
$ docker pull 192.168.3.224:8083/compiler_dnnk_rknn/vitis-ai-tools-1.0.0-gpu:latest
```

创建container的方法如下（举例）：
```bash
$ docker run -it --runtime=nvidia --name=vitis -p 8012:8012 -v /home/zhangniansong/:/home/zhangniansong/ 192.168.3.224:8083/compiler_dnnk_rknn/vitis-ai-tools-1.0.0-gpu /bin/bash
```
说明：
- `--runtime=nvidia` 使用nvidia container runtime
- `-p` 指定使用的端口
- `-v` 指定共享（挂载）的目录，冒号前是要共享给container的source目录，冒号是container内的目标目录。
- `192.168.3.224:8083/compiler_dnnk_rknn/vitis-ai-tools-1.0.0-gpu`： 这是docker image的名称

进入docker container之后cd到repo的目录下面，然后运行`main.py`即可：
```bash
$ cd /home/zhangniansong/decentdnnc_batch_processing/
$ python main.py
```
然后会提示输入模型类型(caffe)，指定source和results目录，输入之后开始定点编译等任务。


---

Update: 2020-06-21

Authors: Zhang Peiheng, Zhang Niansong
