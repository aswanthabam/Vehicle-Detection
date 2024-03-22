import utils

if __name__ == "__main__":
	print("Downloading YOLO V3 weights .... This might taka a while")
	url = "https://github.com/patrick013/Object-Detection---Yolov3/raw/master/model/yolov3.weights"
	utils.download_file(url, f"./yolo/yolov3.weights")