# Farmer’s App for Groundnut Foliar Disease Detection using Deep Learning
This application is developed using Tensorflow framework (a deep learning framework, managed by Google) over Resnet inception V2 model architecture. Using our own collected dataset of 1,500 images (https://www.kaggle.com/muhammadazeemabbas/groundnut-leaves-dataset) of diseased and healthy plants collected in field conditions, a deep convolutional neural network is trained to first detect leaves of the plant and another trained model detects disease spots on every leaf. The trained model achieves an accuracy of 96.35% on cross validation technique.

Sample images for testing purpose are provided as 1.jpg and 2.jpg.

## Running on Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1_qe9nRjAH35KgM4M3Gb4rcu5xmm7B5RY?usp=sharing)

The code currently using ngrok for running Flask application on the Google Colab. If you are using this code on your local machine then comment these lines of codes:
1. routes.py - from flask_ngrok import run_with_ngrok
2. routes.py - run_with_ngrok(app)

## Trained models

Trained model for leave detection is available in /object_detection/inference_graph/frozen_inference_graph_leaf.pb
Trained model for diease spots detection is available in /object_detection/inference_graph/frozen_inference_graph_spot.pb

# Model Training
1. Step 1: Label images
2. Step 2: Create Tfrecord
3. Step 3: Use Transfer learning to train the model (VGG16 performed best)
4. Step 4: Export the trained model to .pb file
5. Step 5: Perform prediction using trained models in a Flask App.

### Statistics
Plants files are stored as 4.jpg
leaves files are stored as 4_1.jpg, 4_2.jpg
Spots files are stored as 4_1_10.jpg (where 10 is number of spots on the leave 1 of plant 4)

# Watch the application in Action
[![Watch the video](https://static.toiimg.com/thumb/resizemode-4,msid-64590538,imgsize-318552,width-720/64590538.jpg)](https://youtu.be/J95sIcTsKAs)
