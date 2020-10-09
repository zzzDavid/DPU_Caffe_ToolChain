from Caffe.caffe_proto import caffe_pb2
from google.protobuf import text_format
import os

def modify_io_layers(input_net):

    assert os.path.exists(input_net), f'{input_net} does not exist'

    net_in = caffe_pb2.NetParameter()
    with open(input_net, 'rb') as f:
        text_format.Merge(f.read(), net_in)

    io_layers = caffe_pb2.NetParameter()
    with open('/home/zhangniansong/vitis_compile/Caffe/caffe_proto/io_layer.prototxt', 'rb') as f:
        text_format.Merge(f.read(), io_layers)

    net_out = caffe_pb2.NetParameter()
    net_out.name = net_in.name

    # add input layer
    input_layer = net_out.layer.add()
    input_layer.CopyFrom(io_layers.layer[0])

    # add layers in between
    num = 0
    for i, layer in enumerate(net_in.layer):
        if layer.type != 'Input':
            new_layer = net_out.layer.add()
            new_layer.CopyFrom(layer)
            if num == 0:
                assert len(new_layer.bottom) == 1
                new_layer.bottom[0] = 'data'
                num += 1

    # if there was an fc layer, remove it
    # import ipdb; ipdb.set_trace()
    if net_out.layer[-1].type == "InnerProduct":
        fc_layer = net_out.layer[-1]
        net_out.layer.remove(fc_layer)

    # add output layers
    for i in range(1,3):
        output_layer = net_out.layer.add()
        output_layer.CopyFrom(io_layers.layer[i])
        if output_layer.name == 'fc':
            output_layer.bottom[0] = net_out.layer[-2].top[0]

    # there is a really large output conv layer in OFA's situation
    i = -1
    while True:
        if net_out.layer[i].type != "Convolution":
            i = i - 1
            continue
        net_out.layer[i].convolution_param.num_output = 100
        net_out.layer[i].name += "_new"
        break

    with open(input_net, 'w') as fp:
        fp.write(text_format.MessageToString(net_out))



if __name__ == "__main__":
    net_file = "../source/3.prototxt"
    modify_io_layers(net_file)

