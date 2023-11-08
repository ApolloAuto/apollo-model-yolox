<div align="center"><img src="assets/logo.png" width="350"></div>
<img src="assets/sunnyvale.jpeg" >

## Introduction
YOLOX is an anchor-free version of YOLO, with a simpler design but better performance! It aims to bridge the gap between research and industrial communities.
For more details, please refer to our [report on Arxiv](https://arxiv.org/abs/2107.08430).

This repo is an implementation of PyTorch version YOLOX, there is also a [MegEngine implementation](https://github.com/MegEngine/YOLOX).

<img src="assets/git_fig.png" width="1000" >

## Updates!!
* 【2023/11/08】 We employ YOLOX(commit id ac58e0a5e68e57454b7b9ac822aced493b553c53) as the first stage in [Apollo](https://github.com/ApolloAuto/apollo) camera_detection_multi_stage component.
* 【2023/02/28】 We support assignment visualization tool, see doc [here](./docs/assignment_visualization.md).
* 【2022/04/14】 We support jit compile op.
* 【2021/08/19】 We optimize the training process with **2x** faster training and **~1%** higher performance! See [notes](docs/updates_note.md) for more details.
* 【2021/08/05】 We release [MegEngine version YOLOX](https://github.com/MegEngine/YOLOX).
* 【2021/07/28】 We fix the fatal error of [memory leak](https://github.com/Megvii-BaseDetection/YOLOX/issues/103)
* 【2021/07/26】 We now support [MegEngine](https://github.com/Megvii-BaseDetection/YOLOX/tree/main/demo/MegEngine) deployment.
* 【2021/07/20】 We have released our technical report on [Arxiv](https://arxiv.org/abs/2107.08430).

## Quick Start

<details>
<summary>Installation</summary>

Step1. Install YOLOX from source.
```shell
# clone code
git clone git@github.com:ApolloAuto/apollo-model-yolox.git

cd apollo-model-yolox

# creat conda env
conda create -n apollo_yolox python=3.8
conda activate apollo_yolox

# install requirements
pip3 install -r requirements.txt
```

</details>

<details>
<summary>Demo</summary>

Step1. Download a pretrained model from the benchmark table.

|Model |size | Params<br>(M) |[Datasets](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d)| [Class](yolox/data/datasets/voc_classes.py)| weights |
| ------  |:---: | :---: | :----: | :----: |:----: |
|[YOLOX-voc-s](./exps/example/yolox_voc/yolox_voc_s.py) |640 | 8.9 | KITTI   | 6| [link](https://github.com/ApolloAuto/apollo-model-yolox/releases/download/model/best_kitti_ckpt.pth) |
|[YOLOX-voc-s](./exps/example/yolox_voc/yolox_voc_s.py) |640 | 8.9 | L4      | 8| [link](https://github.com/ApolloAuto/apollo-model-yolox/releases/download/model/best_L4_ckpt.pth) |

Step2. For example, here we use best_L4_ckpt model:

```shell
python tools/demo.py image -n yolox-s -c /path/to/your/best_L4_ckpt.pth --path sample/ --conf 0.25 --nms 0.45 --tsize 640 --save_result --device [cpu/gpu]
```
then you will find result under path `YOLOX_outputs/yolox_s/`.

</details>

<details>
<summary>Reproduce our results on KITTI</summary>

Step1. Prepare KITTI dataset
```shell
cd <YOLOX_HOME>
ln -s /path/to/your/KITTI ./datasets/KITTI
```

Step2. Tools for kitti type datasets
We provide tools for KITTI type datasets which can help to trans it to VOC type : [readme](datasets/README.md)

Step3. change kitti configs
- class number: 8 to 6
1. change [voc_classes.py](yolox/data/datasets/voc_classes.py) to KITTI class.
2. modify [yolox_voc_s.py](exps/example/yolox_voc/yolox_voc_s.py) todo items.
3. modify [voc.py](yolox/data/datasets/voc.py) line 119 change jpg to png
```python
self._imgpath = os.path.join("%s", "JPEGImages", "%s.jpg") # to png
```

Step4. Reproduce our results on KITTI:

```shell
python3 tools/train.py -f exps/example/yolox_voc/yolox_voc_s.py -d 0 -b 16
```
or resume
```shell
python3 tools/train.py -f exps/example/yolox_voc/yolox_voc_s.py -d 0 -b 16 -c /path/to/your/latest_ckpt.pth --resume
```

* -d: number of gpu devices
* -b: total batch size, the recommended number for -b is num-gpu * 8
* --fp16: mixed precision training
* --cache: caching imgs into RAM to accelarate training, which need large system RAM.
* -c: checkpoint file path

<details>
<summary>Export</summary>

We support batch testing for fast evaluation:

```shell
python tools/export_onnx.py --input data -n yolox-s -c YOLOX_outputs/yolox_voc_s/latest_ckpt.pth  --output-name yolox.onnx

```
* --input: onnx model input blob name.
* -c: path of model.
* --output-name: the file name of covert model

</details>


**Multi Machine Training**

We also support multi-nodes training. Just add the following args:
* --num\_machines: num of your total training nodes
* --machine\_rank: specify the rank of each node

Suppose you want to train YOLOX on 2 machines, and your master machines's IP is 123.123.123.123, use port 12312 and TCP.

On master machine, run
```shell
python tools/train.py -n yolox-s -b 128 --dist-url tcp://123.123.123.123:12312 --num_machines 2 --machine_rank 0
```
On the second machine, run
```shell
python tools/train.py -n yolox-s -b 128 --dist-url tcp://123.123.123.123:12312 --num_machines 2 --machine_rank 1
```

**Logging to Weights & Biases**

To log metrics, predictions and model checkpoints to [W&B](https://docs.wandb.ai/guides/integrations/other/yolox) use the command line argument `--logger wandb` and use the prefix "wandb-" to specify arguments for initializing the wandb run.

```shell
python tools/train.py -n yolox-s -d 8 -b 64 --fp16 -o [--cache] --logger wandb wandb-project <project name>
                         yolox-m
                         yolox-l
                         yolox-x
```

An example wandb dashboard is available [here](https://wandb.ai/manan-goel/yolox-nano/runs/3pzfeom0)

**Others**

See more information with the following command:
```shell
python -m yolox.tools.train --help
```

</details>


<details>
<summary>Evaluation</summary>

We support batch testing for fast evaluation:

```shell
python -m yolox.tools.eval -n  yolox-s -c yolox_s.pth -b 64 --exp_file exps/example/yolox_voc/yolox_voc_s.py -d 8 --conf 0.001 [--fp16] [--fuse]
                               yolox-m
                               yolox-l
                               yolox-x
```
* --fuse: fuse conv and bn
* -d: number of GPUs used for evaluation. DEFAULT: All GPUs available will be used.
* -b: total batch size across on all GPUs

To reproduce speed test, we use the following command:
```shell
python -m yolox.tools.eval -n  yolox-s -c yolox_s.pth -b 1 --exp_file exps/example/yolox_voc/yolox_voc_s.py -d 1 --conf 0.001 --fp16 --fuse
                               yolox-m
                               yolox-l
                               yolox-x
```

</details>


<details>
<summary>Tutorials</summary>

*  [Training on custom data](docs/train_custom_data.md)
*  [Caching for custom data](docs/cache.md)
*  [Manipulating training image size](docs/manipulate_training_image_size.md)
*  [Assignment visualization](docs/assignment_visualization.md)
*  [Freezing model](docs/freeze_module.md)

</details>

## Deployment


1. [MegEngine in C++ and Python](./demo/MegEngine)
2. [ONNX export and an ONNXRuntime](./demo/ONNXRuntime)
3. [TensorRT in C++ and Python](./demo/TensorRT)
4. [ncnn in C++ and Java](./demo/ncnn)
5. [OpenVINO in C++ and Python](./demo/OpenVINO)
6. [Accelerate YOLOX inference with nebullvm in Python](./demo/nebullvm)

## Cite YOLOX
If you use YOLOX in your research, please cite our work by using the following BibTeX entry:

```latex
 @article{yolox2021,
  title={YOLOX: Exceeding YOLO Series in 2021},
  author={Ge, Zheng and Liu, Songtao and Wang, Feng and Li, Zeming and Sun, Jian},
  journal={arXiv preprint arXiv:2107.08430},
  year={2021}
}
```
## In memory of Dr. Jian Sun
Without the guidance of [Dr. Jian Sun](http://www.jiansun.org/), YOLOX would not have been released and open sourced to the community.
The passing away of Dr. Jian is a huge loss to the Computer Vision field. We add this section here to express our remembrance and condolences to our captain Dr. Jian.
It is hoped that every AI practitioner in the world will stick to the concept of "continuous innovation to expand cognitive boundaries, and extraordinary technology to achieve product value" and move forward all the way.

<div align="center"><img src="assets/sunjian.png" width="200"></div>
没有孙剑博士的指导，YOLOX也不会问世并开源给社区使用。
孙剑博士的离去是CV领域的一大损失，我们在此特别添加了这个部分来表达对我们的“船长”孙老师的纪念和哀思。
希望世界上的每个AI从业者秉持着“持续创新拓展认知边界，非凡科技成就产品价值”的观念，一路向前。
