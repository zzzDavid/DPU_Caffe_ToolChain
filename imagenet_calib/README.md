# ImageNet Calibration Dataset


Contains 300 images from ImageNet dataset, no label.

This dataset is intended for Vitis quantization.


## Sample Caffe input layer configuration

```
name: "ResNet-50"
layer {
    name: "data"
    type: "ImageData"
    top: "data"
    top: "label"
    include {
        phase: TRAIN
    }
    transform_param {
        mirror: false
        mean_value: 104
        mean_value: 107
        mean_value: 123
    }
    image_data_param {
        source: "/home/you/data/imagenet_calib/calibration.txt"
        root_folder: "/home/you/data/imagenet_calib/img/"
        batch_size: 1
        shuffle: false
        new_height: 224
        new_width: 224
    }
}
```


