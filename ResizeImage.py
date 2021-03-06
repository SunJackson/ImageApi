from PIL import Image
import cv2

num = 2
image = cv2.imread("/home/sun/duola/text-detection-ctpn/data/demo/captcha-image.jpeg")  # 读取系统的内照片
x, y, _ = image.shape
img = cv2.resize(image, (int(y * num), int(x * num)), interpolation=cv2.INTER_CUBIC)
cv2.imwrite('./demo/crop_resize.jpeg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
