import cv2
import numpy as np
# import imutils
# from matplotlib import pyplot as plt
# import matplotlib.patches as patches

def prepare_for_ml(img, x, w, y, h, i):

  # When the image is slightly turned, Canny detection can detect some residu of the borders. We therefore add slight border removal to the image.
  reduce_border_noise = img[5 : h - 5, 5 : w - 5]
  # cv2.imwrite("./_debug/border_reduced_" + str(i) + ".jpg", reduce_border_noise)
  # Bugfix - If image at border it would go out of bounds upon reading from the border-reduced version. Therefore add adequate white padding.
  add_white_padding = np.pad(reduce_border_noise, pad_width=40, mode='constant', constant_values=255)

  mesh = cv2.threshold(add_white_padding, 145, 255, cv2.THRESH_BINARY)[1];
  mesh_i = 255 - mesh

  edges = cv2.Canny(mesh_i, 145, 255)
  bounding_box = cv2.boundingRect(edges)

  (x1_sq, y1_sq, w_sq, h_sq) = to_bounding_square(*bounding_box)

  # Compare images
  # plt.subplot(121),plt.imshow(reduce_border_noise,cmap = 'gray')
  # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
  # plt.subplot(122), plt.imshow(edges, cmap='gray')
  # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
  # ax = plt.gca()
  # ax.add_patch(patches.Rectangle((bounding_box[0],bounding_box[1]),bounding_box[2],bounding_box[3],linewidth=1,edgecolor='r',facecolor='none'))
  # plt.show()

  # Cut out the square from the image. Since MNIST has 2px padding on all sides, add the padding to the cut-out.
  padding = int((w_sq / 28) * 2) # Scale padding to current image size. Current size / 28 -> Find the scale down factor | * 2 - two pixels wide

  left_x = x1_sq - padding
  f_width = w_sq + (padding * 2) # padding * 2 since
  left_y = y1_sq - padding
  f_height = h_sq + (padding * 2)
  squared_centered = add_white_padding[left_y:left_y + f_height, left_x : left_x + f_width]

  # cv2.imwrite("./_debug/skeleton" + str(i) + ".jpg", squared_centered)

  # Prepare the result for return
  result = squared_centered
  if result.size != 0:
    #Invert the image (black background)
              # Warning: Set is trained on 28x28px images yet inference expects 224x224 images.
              # Set this parameter to 28x28 if you are exporting for training purposes.
    resized = cv2.resize(result, (224, 224))
    inverted = 255 - cv2.threshold(resized, 180, 255, cv2.THRESH_BINARY)[1]
    # cv2.imwrite("./_debug/inverted_test_" + str(i) + ".jpg", inverted)
    result = inverted

  has_value = squared_centered.size != 0
  return (i, has_value, squared_centered, result, x, w, y, h)

# Takes in a bounding rect and returns a perfectly centered square around the bounding box
def to_bounding_square(x1, y1, w, h):
  # Get the square_rest i.e. the difference between width and height (square_rest is what will need to be added to the smallest size to get a square)
  r = abs(w - h)

  if r == 0:
    return (x1, y1, w, h)
  # Look at which bound needs to be padded. Since it's a rectangle, width is either > height or opposite, or they are the same.
  # We assume the most likely, since handwritten recognition, is that h > w
  elif h > w:
    return (int(x1 - (r/2)), y1, w + r, h)
  else:
    return (x1, int(y1 - (r/2)), w, h + r)
