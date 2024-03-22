import cv2
import numpy as np

YOLO_WEIGHTS = "yolov3.weights"
YOLO_CFG = "yolov3.cfg"
COCO_NAMES = "coco.names"

def load_yolo():
	net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
	classes = []
	with open(COCO_NAMES, "r") as f:
		classes = [line.strip() for line in f.readlines()]
	layers_names = net.getLayerNames()
	output_layers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
	colors = np.random.uniform(0, 255, size=(len(classes), 3))
	return net, classes, colors, output_layers