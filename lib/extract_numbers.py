import cv2
import numpy as np

from lib.prepare import image_inverter, machine_read_preparer
from lib.extract_boxes import box_extractor, number_extractor, contour_sorter, contour_drawer
from lib.result import write_results
from lib.recognise import recognise_handwriting

def run(img_for_box_extraction_path, subj_group, stream, assessment, tf_interpreter):

  # 1) Read the image and invert to white text on black background.
  (img, img_inverted) = image_inverter.invert(img_for_box_extraction_path)

  only_boxes = box_extractor.extract_boxes(img, img_inverted)

  # Find contours for image, which will detect all the boxes
  contours, _ = cv2.findContours(only_boxes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  # Sort all the contours by top to bottom.
  #(contours, boundingBoxes) = contour_sorter.sort_contours(contours, method="top-to-bottom")

  # Iterate all contours and retrieve the read area + extracted numbers.
  # Returned format (read_area_image, [(student_number_sorted, x, w, y, h)])
  (student_filled_box, extracted_nums) = number_extractor.extract_numbers(img, contours)

  # print(extracted_nums)

  # Prepare Result Array. Of the form (i, has_value, result, x, w, y, h)
  result = []
  for (i, num) in enumerate(extracted_nums):
    result.append(machine_read_preparer.prepare_for_ml(*num, i))

  # Recognise handwriting
  result_ml = recognise_handwriting.recognise(result, tf_interpreter)
  
  # Create Result Directory


  result_loc = write_results.write(student_filled_box, result_ml, subj_group, stream, assessment)

  return result_loc
