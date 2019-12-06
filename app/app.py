from lib import extract_numbers
import cv2
import numpy as np
import sys

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf

# pre-load TensforFlow Model
tf_interpreter = tf.lite.Interpreter(model_path="model/handwriting_read.tflite")

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.before_request
def log_request_info():
    app.logger.debug('Files: %s', request.files)

@app.route('/', methods=["POST"])
@cross_origin()
def mark():
  print('APP.PY: Hit the post route successfully', file=sys.stderr)
  # headers = {"Content-Type": "application/json"}
  # return "Test Worked!"

  # user_file is the name value in input element
  if request.method == 'POST' and len(request.files) > 0:
    
    subj_group = request.values.get("subjectGroupId");
    stream = request.values.get("streamId");
    assessment = request.values.get("assessmentId");

    results = {}

    uploaded_files = request.files.getlist("files")

    print('APP.PY: These files going to openCV: ', file=sys.stderr)
    print(uploaded_files, file=sys.stderr)
    # Process all files
    for file in uploaded_files:

      img = cv2.imdecode(np.fromstring(file.read(), np.uint8), 0)
      res = extract_numbers.run(img, subj_group, stream, assessment, 0, tf_interpreter)

      results['1'] = res
    
    print('APP.PY: Finished processing the files successfully. The Result: ', file=sys.stderr)
    print(results, file=sys.stderr)

    return results['1']
    
  # No files to process have been sent.
  else:
    return 'noop';

if __name__ == '__main__':
  app.run(host="0.0.0.0") #, debug=True)
