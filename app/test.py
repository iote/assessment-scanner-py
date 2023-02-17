from lib import extract_numbers
import cv2

# import warnings filter tc ignore all future warnings
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf

print('Testing app with test input located at _test/input.png. Writing results to _debug')
tf_interpreter = tf.lite.Interpreter(model_path="model/handwriting_read.tflite")
#
# Configure target image here
img = cv2.imread('../_test/test_6.jpg', 0)

# Run the test
extract_numbers.run(img, 'some_subject', 'class_1', 'stream_1', 1, tf_interpreter, 1)

print('Test done. Check _debug folder.')

