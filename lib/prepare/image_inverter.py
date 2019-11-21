import cv2
import os

def invert(img_path):
  # Read the image
  img = cv2.imread(img_path, 0)
  # cv2.imwrite("./_debug/1_read.jpg", img)
  
  #TODO: Rectifiy image for reading photo's instead of scans only.

  # Threshold the image - Turn into grayscale - Further turn into black + white
  #   Info: https://en.wikipedia.org/wiki/Thresholding_(image_processing)
  (thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  # cv2.imwrite("./_debug/1_inverted.jpg", img_bin)

  # Invert the image - Turn into white text on black background.
  img_inverted = 255 - img_bin

  # Write inverted result
  # cv2.imwrite("./_debug/1_inverted.jpg", img_bin)

  return (img, img_inverted)
