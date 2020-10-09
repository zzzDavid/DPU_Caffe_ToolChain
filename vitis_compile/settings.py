#
model_type_supported = ["caffe", ]

#
cmd_format = "{};{}"

#
ARCH = {
        "ZCU102": "/opt/vitis_ai/compiler/arch/dpuv2/ZCU102/ZCU102.json",
}

# caffe command format
cmd_caffe_env = "source /opt/vitis_ai/conda/bin/activate vitis-ai-caffe; python -V;"
cmd_caffe_decent = "vai_q_caffe quantize \
        -model {0}/{2}.prototxt \
        -weights {0}/{2}.caffemodel \
        --gpu {3} \
        --output_dir {0}/{2}/quantize_results 2>&1 | tee {1}/{2}_decent.txt"
cmd_caffe_dnnc = "vai_c_caffe \
        -p {0}/{2}/quantize_results/deploy.prototxt \
        -c {0}/{2}/quantize_results/deploy.caffemodel \
        -a {4} \
        -e  \"{5}\" \
        --output_dir {1} \
        -n {2} 2>&1 | tee {1}/{2}_dnnc.txt"

# tensorflow command format
cmd_tensorflow_env = "source /opt/vitis_ai/conda/bin/activate vitis-ai-tensorflow; python -V;"
cmd_tensorflow_decent = "vai_q_tensorflow  quantize \
   --input_frozen_graph ./models/{0}/{1}/{2}.pb \
   --input_nodes {3} \
   --input_shapes ?,{4} \
   --output_nodes {5} \
   --input_fn {2}_input_fn.calib_input \
   --method {6} \
   --gpu {7} \
   --calib_iter {8} \
   --output_dir ./models/{0}/{1}/{2}/quantize_results/ 2>&1 | tee ./models/{0}/{1}/{2}_decent.txt"
cmd_tensorflow_dnnc = "/opt/vitis_ai/compiler/vai_c_tensorflow \
    --frozen_pb ./models/{0}/{1}/{2}/quantize_results/deploy_model.pb \
    --arch {3} \
    --output_dir dpu_elfs \
    --net_name {2} \
    --option \"{4}\" 2>&1 | tee ./models/{0}/{1}/{2}_dnnc.txt"


