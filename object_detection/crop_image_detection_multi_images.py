######## Image Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 1/15/18
# Description:
# This program uses a TensorFlow-trained neural network to perform object detection.
# It loads the classifier and uses it to perform object detection on an image.
# It draws boxes, scores, and labels around the objects of interest in the image.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## but I changed it to make it more understandable to me.

# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

def detect_and_crop():

    # Grab path to current working directory
    CWD_PATH = os.getcwd()

    # Name of the directory containing the object detection module we're using
    MODEL_NAME = 'inference_graph'
    #DIR_NAME = 'D:/PythonProjects/flask_app/flask_app/plants/'
    DIR_NAME = os.path.join(CWD_PATH,'flask_app','static','plants')
    DIR_Leaves = os.path.join(CWD_PATH,'flask_app','static','leaves')

    # Path to frozen detection graph .pb file, which contains the model that is used
    # for object detection.
    PATH_TO_CKPT = os.path.join(CWD_PATH,'object_detection',MODEL_NAME,'frozen_inference_graph_leaf.pb')

    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,'object_detection','training','groundNut_Leaf.pbtxt')


    # Path to image
    #PATH_TO_DIR = os.path.join(CWD_PATH,DIR_NAM_NAME)
    PATH_TO_DIR = DIR_NAME

    # Number of classes the object detector can identify
    NUM_CLASSES = 1

    # Load the label map.
    # Label maps map indices to category names, so that when our convolution
    # network predicts `5`, we know that this corresponds to `king`.
    # Here we use internal utility functions, but anything that returns a
    # dictionary mapping integers to appropriate string labels would be fine
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    # Define input and output tensors (i.e. data) for the object detection classifier

    # Input tensor is the image
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Load image using OpenCV and
    # expand image dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    for filename in os.listdir(PATH_TO_DIR):
        if(os.path.isdir(PATH_TO_DIR+"/"+filename)==True):
            continue
        if(filename.endswith(".jpg")):
            image = cv2.imread(PATH_TO_DIR+"/"+filename)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_expanded = np.expand_dims(image_rgb, axis=0)

            # Perform the actual detection by running the model with the image as input
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_expanded})


            ################## Cropping the Detected Part #####

            # Draw the results of the detection (aka 'visulaize the results')
            coordinates = vis_util.return_coordinates(
                                    image,
                                    np.squeeze(boxes),
                                    np.squeeze(classes).astype(np.int32),
                                    np.squeeze(scores),
                                    category_index,
                                    use_normalized_coordinates=True,
                                    line_thickness=8,
                                    min_score_thresh=0.60)
            #print(coordinates)
            i = 1
            for rect in coordinates:
                #print(rect)
                filename, file_extension = os.path.splitext(os.path.basename(filename))
                iCrop = (filename+"_"+str(i)+".jpg")
                img = image[rect[0]:rect[1],rect[2]:rect[3]]
                cv2.imwrite(DIR_Leaves+"/"+iCrop,img)
                i +=1