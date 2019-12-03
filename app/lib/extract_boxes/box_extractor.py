import cv2
import numpy as np

# Uses morphological transformations to remove everything except the outsets of the boxes.
#   Then contour finding algorithms can provide the exact location of each of the boxes.
def extract_boxes(img, img_inverted):
  # Define the kernel length. Numpy.array.shape returns a tuple of the array lenghts in each dimension i.e. (x-length, y-length)
  # The // operation defines the accuracy. The higher the number in the second param, the more accurate.
  kernel_length_verticle = np.array(img).shape[1]//40
  kernel_length_horizontal = np.array(img).shape[0]//50

   # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
  #   - Will basically create a pixel array of full horizontal lines ___
  hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length_horizontal, 1))

  # Morphological operation to detect horizontal lines from an image
  img_temp2 = cv2.erode(img_inverted, hori_kernel, iterations=3)
  horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
  # cv2.imwrite("./_debug/2_horizontal_lines.jpg", horizontal_lines_img)

  # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
  # See https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
  #   - Will basically create a pixel array of full vertical lines ||||||||||||||
  verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length_verticle))

  # Morphological operation to detect vertical lines from an image
  img_temp1 = cv2.erode(img_inverted, verticle_kernel, iterations=3)
  verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
  # cv2.imwrite("./_debug/3_verticle_lines.jpg", verticle_lines_img)

  # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
  alpha = 0.5
  beta = 1.0 - alpha
  # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
  only_boxes = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
  # cv2.imwrite("./_debug/4_combined.jpg", only_boxes)

  # A kernel of (3 X 3) ones to refine the combined image.
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
  only_boxes = cv2.erode(~only_boxes, kernel, iterations=2)
  # cv2.imwrite("./_debug/5_combined_eroded.jpg", only_boxes)
  
  (thresh, only_boxes) = cv2.threshold(only_boxes, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  # cv2.imwrite("./_debug/6_prepared.jpg", only_boxes)

  return only_boxes
