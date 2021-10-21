import cv2   #importing cv2 to read image
image = cv2.imread("img.jpg")  #write image name to be uploaded.
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #this line converts image into grayscale format 
inverted_image = 255 - gray_image
blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
inverted_blurred = 255 - blurred
pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
cv2.imshow("Original Image", image)
cv2.imshow("Pencil Sketch of image", pencil_sketch)
cv2.waitKey(0)  # this is used to stop the image.exe file to wait for sometime and then close the file.
