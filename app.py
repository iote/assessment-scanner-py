from lib import extract_numbers

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf

# pre-load TensforFlow Model
tf_interpreter = tf.lite.Interpreter(model_path="subs/model/handwriting_read.tflite")

from flask import Flask
app = Flask(__name__)

@app.route('/')
def mark:
  #user_file is the name value in input element
  if request.method == 'POST' and len(request.files) > 0:
    
    results = [];
    # Process all files
    for file in request.files:
      res = extract_numbers.run(file, output_folder, tf_interpreter)
      results.append(res)
      return results
    
  # No files to process have been sent.
  elif:
    return 'noop';


if __name == '__main__':
  app.run(host='0.0.0.0', port='1080') #debug=True, 
