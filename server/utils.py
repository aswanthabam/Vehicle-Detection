import cv2
import numpy as np

YOLO_WEIGHTS = "./yolo/yolov3.weights"
YOLO_CFG = "./yolo/yolov3.cfg"
COCO_NAMES = "./yolo/coco.names"

def load_yolo():
	net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
	classes = []
	with open(COCO_NAMES, "r") as f:
		classes = [line.strip() for line in f.readlines()] 
	
	output_layers = [layer_name for layer_name in net.getUnconnectedOutLayersNames()]
	colors = np.random.uniform(0, 255, size=(len(classes), 3))
	return net, classes, colors, output_layers


def load_image(img_path):   
	img = cv2.imread(img_path)
	img = cv2.resize(img, None, fx=0.4, fy=0.4)
	height, width, channels = img.shape
	return img, height, width, channels

def detect_objects(img, net, outputLayers):			
	blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
	net.setInput(blob)
	outputs = net.forward(outputLayers)
	return blob, outputs

def get_box_dimensions(outputs, height, width):
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


def draw_labels(boxes, confs, colors:list, class_ids, classes, img): 
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
				cv2.rectangle(shapes, (x,y), (x+w, y+h), color)
				alpha = 0.00001
				mask = shapes.astype(bool)
				img[mask] = cv2.addWeighted(img, alpha, shapes, 1- alpha, 0)[mask]
				cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
	return img, label_counter

def image_detect(img_path): 
	model, classes, colors, output_layers = load_yolo()
	image, height, width, channels = load_image(img_path)
	blob, outputs = detect_objects(image, model, output_layers)
	boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
	img, label_counter = draw_labels(boxes, confs, colors, class_ids, classes, image)
	return img, label_counter
	
def save_image(img, path):
	cv2.imwrite(path, img)
	return path