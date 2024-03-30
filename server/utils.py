import cv2
import numpy as np
import urllib.request

YOLO_WEIGHTS = "./yolo/yolov3.weights"
YOLO_CFG = "./yolo/yolov3.cfg"
COCO_NAMES = "./yolo/coco.names"

class YOLO:
	model = None
	classes = None
	output_layers = None
	
	def load_yolo(self):
		"""
		load the yolo model and classes
		"""
		self.net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
		self.classes = []
		with open(COCO_NAMES, "r") as f:
			self.classes = [line.strip() for line in f.readlines()] 
		
		self.output_layers = [layer_name for layer_name in self.net.getUnconnectedOutLayersNames()]


	def load_image(self, img_path): 
		"""
		Load the image and resize it to 0.4 of its original size
		:param img_path: path to the image
		:return: image, height, width, channels, original image
		"""  
		img = cv2.imread(img_path)
		org_img = img.copy()
		img = cv2.resize(img, None, fx=0.4, fy=0.4)
		height, width, _ = img.shape
		return img, height, width, org_img

	def detect_objects(self,img):
		"""
		Detect objects in the image
		"""

		blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
		self.net.setInput(blob)
		outputs = self.net.forward(self.output_layers)
		return outputs

	def get_box_dimensions(self, outputs, height, width):
		"""
		Get the dimensions of the bounding box
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


	def draw_labels(self, boxes, confs, class_ids, classes, img): 
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

	def image_detect(self,img_path): 
		"""
		Detect objects in the image
		:param img_path: path to the image
		:return: image with labels
		"""
		image, height, width, org_img = self.load_image(img_path)
		outputs = self.detect_objects(image)
		boxes, confs, class_ids = self.get_box_dimensions(outputs, height, width)
		b = [self.convert_rectangle((height, width), (org_img.shape[0],org_img.shape[1]), box) for box in boxes]
		img, label_counter = self.draw_labels(b, confs, class_ids, self.classes, org_img)
		return img, label_counter

	def convert_rectangle(self, resized_img_shape, original_img_shape, rectangle):
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


def download_file(url, destination):
	response = urllib.request.urlopen(url)
	total_size = int(response.headers['Content-Length'])
	bytes_downloaded = 0
	block_size = 1024  # Adjust the block size as needed
	print(f"Total size: {round(total_size / block_size ** 2,2)} MB")
	
	with open(destination, 'wb') as file:
		while True:
			buffer = response.read(block_size)
			if not buffer:
				break
			bytes_downloaded += len(buffer)
			file.write(buffer)
			status = f" {round( bytes_downloaded / block_size ** 2,2)} / {round(total_size / block_size ** 2,2)} MB downloaded"
			print(status, end='\r')  # Print progress without new line
	
	print()  # Print a new line after download completes