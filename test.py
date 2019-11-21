from lib import extract_numbers

# import warnings filter tc ignore all future warnings
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf

print('Testing app with test input located at _test/input.png. Writing results to _debug')
tf_interpreter = tf.lite.Interpreter(model_path="model/handwriting_read.tflite")
#
# Execute script and return results via stdout
extract_numbers.run('_test/test_6.jpg', '_debug/', tf_interpreter)

print('Test done. Check _debug folder.')
