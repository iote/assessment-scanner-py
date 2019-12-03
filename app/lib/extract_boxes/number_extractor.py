import cv2
import numpy as np

# Uses morphological transformations to remove everything except the outsets of the boxes.
#   Then contour finding algorithms can provide the exact location of each of the boxes.
def extract_numbers(img, contours):

  idx = 0
  foundOuterBox = False

  #output inits
  student_filled_box = False
  parent_boxes = []
  extracted_nums = []

  for num, c in enumerate(contours):
    # Returns the location and width,height for every contour
    x, y, w, h = cv2.boundingRect(c)
    # print("x: " + str(x) + "| y: " + str(y) + "| h: " + str(h) + "| w: " + str(w))

    # Take sub-image. Use a rectangular bounding box to slice -> [y_take_from = y : y_take_till = y + h,
    #                                                             x_take_from = x : x_take_till = x + w ]
    new_img = img[y:y + h, x:x + w]
    # cv2.imwrite('_debug/scan_' + str(num) + '.png', new_img)

    #The second detected is always the box, after detecting the full page.
    if num == 1:
      student_filled_box = new_img
      foundOuterBox = True
      # cv2.imwrite(cropped_dir_path + 'student_filled.png', new_img)

    elif num > 2: #foundOuterBox and abs(w - h) < 50:
      # Algo will always read the contour twice.
      # Once with borders and once without, since a border itself has two borders. The inner and outer border.
      parent = list(filter(lambda parent_coords : (parent_coords[0] < x) and ((parent_coords[0] + parent_coords[2]) > (x + w)) and (parent_coords[1] < y) and ((parent_coords[1] + parent_coords[3]) > (y + h)), parent_boxes))
      
      if len(parent) > 0:
        idx += 1
        extracted_nums.append((new_img, x, w, y, h))
        # cv2.imwrite('_debug/extracted_' + str(idx) + '.png', new_img)

      else:
        parent_boxes.append((x, y, w, h))
        # cv2.imwrite('_debug/parent_' + str(idx + 1) + '.png', new_img)

  # Put in correct order
  extracted_nums.reverse()

  return (student_filled_box, extracted_nums)