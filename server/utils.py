import cv2
import numpy as np

YOLO_WEIGHTS = "./yolo/yolov3.weights"
YOLO_CFG = "./yolo/yolov3.cfg"
COCO_NAMES = "./yolo/coco.names"

def load_yolo():
	"""
	load the yolo model and classes
	:return: yolo model, classes, output layers
	"""
	net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
	classes = []
	with open(COCO_NAMES, "r") as f:
		classes = [line.strip() for line in f.readlines()] 
	
	output_layers = [layer_name for layer_name in net.getUnconnectedOutLayersNames()]
	return net, classes, output_layers


def load_image(img_path): 
	"""
	Load the image and resize it to 0.4 of its original size
	:param img_path: path to the image
	:return: image, height, width, channels, original image
	"""  
	img = cv2.imread(img_path)
	org_img = img.copy()
	img = cv2.resize(img, None, fx=0.4, fy=0.4)
	height, width, channels = img.shape
	return img, height, width, channels, org_img

def detect_objects(img, net, outputLayers):
	"""
	Detect objects in the image
	:param img: image
	:param net: yolo model
	:param outputLayers: output layers
	:return: blob and outputs
	"""

	blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
	net.setInput(blob)
	outputs = net.forward(outputLayers)
	return blob, outputs

def get_box_dimensions(outputs, height, width):
	"""
	Get the dimensions of the bounding box
	:param outputs: yolo model outputs
	:param height: height of the image
	:param width: width of the image
	:return: bounding box dimensions
	"""

	boxes = []
	confs = []
	class_ids = []
	for output in outputs:
		for detect in output:
			scores = detect[5:]
			class_id = np.argmax(scores)
			conf = scores[class_id]
			if conf > 0.3:
				center_x = int(detect[0] * width)
				center_y = int(detect[1] * height)
				w = int(detect[2] * width)
				h = int(detect[3] * height)
				x = int(center_x - w/2)
				y = int(center_y - h / 2)
				boxes.append([x, y, w, h])
				confs.append(float(conf))
				class_ids.append(class_id)
	return boxes, confs, class_ids


def draw_labels(boxes, confs, class_ids, classes, img): 
	"""
	Draw the labels on the image
	:param boxes: bounding boxes
	:param confs: confidence
	:param class_ids: class ids
	:param classes: classes
	:param img: image
	:return: image with labels
	"""
	indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
	font = cv2.FONT_HERSHEY_PLAIN
	label_counter = {
		"car": 0,
		"truck": 0,
		"bus": 0,
		"motorbike": 0,
		"bicycle": 0,
		"person": 0
	}
	label_colors = {
		"car": (0, 255, 0),
		"truck": (0, 0, 255),
		"bus": (255, 0, 0),
		"motorbike": (255, 255, 0),
		"bicycle": (0, 255, 255),
		"person": (255, 0, 255)
	}

	for i in range(len(boxes)):
		if i in indexes:
			x, y, w, h = boxes[i]
			label = str(classes[class_ids[i]])
			if label in label_counter.keys():
				label_counter[label] += 1
				color = label_colors[label]
				shapes = np.zeros_like(img, np.uint8)
				cv2.rectangle(shapes, (x,y), (x+w, y+h), color, cv2.FILLED)
				alpha = 0.6
				mask = shapes.astype(bool)
				img[mask] = cv2.addWeighted(img, alpha, shapes, 1- alpha, 0)[mask]
				cv2.rectangle(img, (x,y), (x+w, y+h), color)
				cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
	return img, label_counter

def image_detect(img_path): 
	"""
	Detect objects in the image
	:param img_path: path to the image
	:return: image with labels
	"""

	model, classes, output_layers = load_yolo()
	image, height, width, channels, org_img = load_image(img_path)
	_, outputs = detect_objects(image, model, output_layers)
	boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
	b = [convert_rectangle((height, width), (org_img.shape[0],org_img.shape[1]), box) for box in boxes]
	img, label_counter = draw_labels(b, confs, class_ids, classes, org_img)
	return img, label_counter

def convert_rectangle(resized_img_shape, original_img_shape, rectangle):
	"""
	Convert rectangle from resized image to original image
	:param resized_img_shape: shape of resized image
	:param original_img_shape: shape of original image
	:param rectangle: rectangle
	:return: rectangle in original image
	"""
	print(resized_img_shape, original_img_shape, rectangle)
	scale_x = original_img_shape[1] / resized_img_shape[1]
	scale_y = original_img_shape[0] / resized_img_shape[0]
	
	center_x_resized, center_y_resized, width_resized, height_resized = rectangle
	
	center_x_original = int(center_x_resized * scale_x)
	center_y_original = int(center_y_resized * scale_y)
	width_original = int(width_resized * scale_x)
	height_original = int(height_resized * scale_y)
	x_original = int(center_x_original)
	y_original = int(center_y_original)
	
	return (x_original, y_original, width_original, height_original)

def save_image(img, path):
	"""
	Save the image
	:param img: image
	:param path: path to save the image
	:return: path
	"""

	cv2.imwrite(path, img)
	return path