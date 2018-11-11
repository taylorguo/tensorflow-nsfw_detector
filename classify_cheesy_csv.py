#!/usr/bin/env python
# Coding: UTF-8
import sys,os
import argparse
import tensorflow as tf

from model import OpenNsfwModel, InputType
from image_utils import create_tensorflow_image_loader
from image_utils import create_yahoo_image_loader

import numpy as np

model_weights = "data/open_nsfw-weights.npy"

IMAGE_LOADER_TENSORFLOW = "tensorflow"
IMAGE_LOADER_YAHOO = "yahoo"
image_loader = IMAGE_LOADER_TENSORFLOW


def main():
    
    model = OpenNsfwModel()

    with tf.Session() as sess:

        # input_type = InputType[args.input_type.upper()]
        input_type = InputType.TENSOR   ############### 
        model.build(weights_path=model_weights, input_type=input_type)

        fn_load_image = None

        if input_type == InputType.TENSOR:
            if image_loader == IMAGE_LOADER_TENSORFLOW:
                fn_load_image = create_tensorflow_image_loader(sess)
            else:
                fn_load_image = create_yahoo_image_loader()
        elif input_type == InputType.BASE64_JPEG:
            import base64
            fn_load_image = lambda filename: np.array([base64.urlsafe_b64encode(open(filename, "rb").read())])

        sess.run(tf.global_variables_initializer())
        
        ##########
        result_list = []
        from os_utils import get_file_list
        file_list = get_file_list("dataset") 

        remark = []

        for file in file_list:
            input_image_file = os.path.join(".",file)  

            if input_image_file[-4::] == ".png":
                from skimage import io
                from skimage.color import rgba2rgb
                im = io.imread(file)
                im_rgb = rgba2rgb(im)
                io.imsave("current_temp.jpeg", im_rgb)
                input_file = "current_temp.jpeg"
            else: 
                input_file = file

            image = fn_load_image(input_file)

            predictions = \
                sess.run(model.predictions,
                        feed_dict={model.input: image})
            # print(predictions[0])
            result_list.append(predictions[0][1])
            print("Results for '{}'".format(input_file))
            print("\tSFW score:\t{}\n\tNSFW score:\t{}".format(*predictions[0]))
            if predictions[0][1] >= 0.03: 
                print("\t低俗图片")
                remark.append("低俗")
            else: 
                print("\t不是低俗图片")
                remark.append("正常")

            print(predictions[0][1])
            
            os.system("rm -rf current_temp.jpeg")
        
        result_dict = {"image_list":file_list, "result_list":result_list, "remark":remark}

    return result_dict

        
if __name__ == "__main__":
    
    result = main()
    # print(result)

    i = 0
    while i < len(result["image_list"]):
        import csv
        with open("result.csv", "a") as f:
            csv_write = csv.writer(f)
            csv_write.writerow([i+1, result["image_list"][i], result["result_list"][i], result["remark"][i]])
        i += 1

