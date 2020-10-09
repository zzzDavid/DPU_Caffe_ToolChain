import json
import os
import subprocess
import requests
import argparse
import settings
from glob import glob
from shutil import copyfile
from Caffe.modify_layer import modify_io_layers


parser = argparse.ArgumentParser()
parser.add_argument(
    '-s',
    '--source',
    help="source directory where model files are in PATH",
    type=str,
    default='/home/zhangniansong/NAS/aw_nas/results_zns/hardwares/0-dpu/'
)
parser.add_argument(
    '-r',
    '--result',
    help="result directory where output files are in PATH",
    type=str,
    default='./results'
)

parser.add_argument(
    '-g',
    '--gpu',
    help="which gpu to use",
    type=int,
    default=3
)

args = parser.parse_args()

model_type = "caffe"
caffe_dir = args.source
result_dir = args.result
gpu_index = args.gpu

# make source directory if not exist
# pwd = os.getcwd()
# source_dir = os.path.join(pwd, 'source')
# if not os.path.isdir(source_dir):
#     os.makedirs(source_dir)

source_dir = args.source

# copy files from caffe model source folder
# path looks like this: caffe_dir/0/pytorch_to_caffe/0.caffemodel(.prototxt)
# model_names = os.listdir(caffe_dir)
# for idx in model_names:
#     immediate_parent = os.path.join(caffe_dir, idx, 'pytorch_to_caffe')
#     weights = os.path.join(immediate_parent, "0-dpu-{}.caffemodel".format(idx))
#     netfile = os.path.join(immediate_parent, "0-dpu-{}.prototxt".format(idx))
#     if os.path.exists(weights):
#         copyfile(weights, os.path.join(source_dir, "{}.caffemodel".format(idx) ) )
#     else:
#         print("no weights file found: " + weights)
#     if os.path.exists(netfile):
#         dst_netfile = os.path.join(source_dir, "{}.prototxt".format(idx) )
#         copyfile(netfile,  dst_netfile)
#         modify_io_layers(dst_netfile)
#     else:
#         print("no prototxt file found: " + netfile)


f = open("./{}.json".format(model_type), encoding='utf-8')
content = f.read()
params = json.loads(content)
params["source_directory"] = source_dir
params["result_directory"] = result_dir
params["gpu_index"] = gpu_index
# print(params)

# print(glob(os.path.join(source_dir, '*.prototxt')))

# this is a one-time thing
for item in glob(os.path.join(source_dir, '*.prototxt')):
    modify_io_layers(os.path.join(source_dir,item))

for item in glob(os.path.join(source_dir, '*.prototxt')):

    item = os.path.basename(item)
    item = item.split(".")[0]

    tmp_path = os.path.join(source_dir, item)
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    
    elf_path = os.path.join(result_dir, "dpu_" + item + ".elf")
    if os.path.exists(elf_path): 
        print(elf_path + " already exists")
    else:
        try:
            caffe_env = settings.cmd_caffe_env
            caffe_decent = settings.cmd_caffe_decent.format(params["source_directory"],
                                                            params["result_directory"],
                                                            item,
                                                            params["gpu_index"])
            print(caffe_decent)
            subprocess.run(caffe_env+caffe_decent, shell=True, check=True, executable="/bin/bash")
            caffe_dnnc = settings.cmd_caffe_dnnc.format(params["source_directory"],
                                                        params["result_directory"],
                                                        item,
                                                        params["gpu_index"],
                                                        settings.ARCH[params["ARCH"]],
                                                        # params["mode"]
                                                        "{'mode': '" + params["mode"] + "'}")
            print(caffe_dnnc)                                            
            subprocess.run(caffe_env+caffe_dnnc, shell=True, check=True, executable="/bin/bash")
        except Exception as e:
            print(str(e))
            continue

        # sent the elf file to dpu
        # try:
        #     file_path = "{}/dpu_{}.elf".format(params["result_directory"], item)
        #     file = open(file_path, "rb")
        #     res = requests.post(url="http://192.168.6.144:8055/test_latency/test_latency/",
        #                         files={"file": file},
        #                         data={"kernel_name": item})
        #     file.close()
        #     with open("{}/dpu_{}.txt".format(params["result_directory"], item), "wb") as f:
        #         f.write(res.content)
        # except Exception as e:
        #     print(str(e))
