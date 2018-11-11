# Tensorflow Implementation 识别低俗图片

 [低俗图片分类器](https://github.com/yahoo/open_nsfw) Tensorflow 实现.

使用[Caffe to TensorFlow](https://github.com/ethereon/caffe-tensorflow) 提取原有caffe weights. 保持在目录文件中： `data/open_nsfw-weights.npy`.

## Prerequisites

兼容 `Python 3.6` and `Tensorflow 1.x` 。

模型的实现在 `model.py` 中。

[TensorFlow 可以支持 AVX, FMA, SSE 二进制安装包](https://github.com/lakshayg/tensorflow-build)

直接从网址安装：（如果使用 Python3.6.3，使用以下链接安装 tensorflow 1.4）
```
pip install --ignore-installed --upgrade "https://github.com/lakshayg/tensorflow-build/raw/master/tensorflow-1.4.0-cp36-cp36m-macosx_10_12_x86_64.whl"
```

### Usage

```
> python classify_cheesy_csv.py

Results for 'test.jpg'
	SFW score:	0.9355766177177429
	NSFW score:	0.06442338228225708
```

__Note:__ 目前只支持 jpeg 图片。

`classify_cheesy_csv.py` 主要参数:

```
usage: classify_cheesy_csv.py 

  - MODEL_WEIGHTS
                        加载训练好的模型权重参数文件
  - 图像加载方式 {yahoo,tensorflow}
                        Caffe 或 tensorflow 加载方式
  - 图像输入类型 {tensor,base64_jpeg}
                        张量 或 byte数据 模式
```


* 不同的加载方式： jpeg 和 resizing 实现不同。 See [this issue](https://github.com/mdietrichstein/tensorflow-open_nsfw/issues/2#issuecomment-346125345) for details.

__Note:__  分类结果和图片加载方式有关 !

__-t/--input_type__

如果使用图片的输入类型：`base64_jpeg` ,  就需要使用 `tensorflow` 图像加载方式。


### Tools

The `tools` folder contains some utility scripts to test the model.

__export_graph.py__

Exports the tensorflow graph and checkpoint. Freezes and optimizes the graph per default for improved inference and deployment usage (e.g. Android, iOS, etc.). Import the graph with `tf.import_graph_def`.

__export_savedmodel.py__

Exports the model using the tensorflow serving export api (`SavedModel`). The export can be used to deploy the model on [Google Cloud ML Engine](https://cloud.google.com/ml-engine/docs/concepts/prediction-overview), [Tensorflow Serving]() or on mobile (haven't tried that one yet).

__create_predict_request.py__

Takes an input image and spits out an json file suitable for prediction requests to a Open NSFW Model deployed on [Google Cloud ML Engine](https://cloud.google.com/ml-engine/docs/concepts/prediction-overview) (`gcloud ml-engine predict`).


### fork from 

```
[mdietrichstein/tensorflow-open_nsfw](https://github.com/mdietrichstein/tensorflow-open_nsfw)
```
