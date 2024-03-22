import utils
import cv2

img,_ = utils.image_detect("test1.jpg")
cv2.imshow("output", img)
cv2.waitKey(0)
cv2.destroyAllWindows()