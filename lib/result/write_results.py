import json
import cv2
from google.cloud import storage
from tempfile import TemporaryFile

# Function that writes the result in a json object
# Arguments:
#   1 - Result Array. Of the form [(i, has_value, result_image, x, w, y, h)]
#   2 - output_dir. Dir to write the images to
def write(student_filled_box, algo_result, output_dir):

  data = {}
  data['reads'] = len(algo_result);
  results = []

  client = storage.Client()
  bucket = client.get_bucket('assessment-results')

  # Structure of result (i, has_value, result_image, x, w, y, h, value?)
  for index, result in enumerate(algo_result):

    i = result[0]
    has_value    = result[1]
    image        = result[2]
    result_image = result[3]
    x            = result[4]
    w            = result[5]
    y            = result[6]
    h            = result[7]

    value = {
        'index': i,

        'position': {
          'topLeft':     { 'x': x, 'y': y},
          'topRight':    { 'x': x + w, 'y': y},
          'bottomLeft':  { 'x': x, 'y': y + h },
          'bottomRight': { 'x': x + w, 'y': y + h},
        },
        'isNull': not has_value,
    }

    if (has_value):
      output_loc = output_dir + 'num_' + str(i)

      save_image(image, bucket, output_loc + '.jpg')
      # cv2.imwrite(output_loc + '.png', image)
      value['loc'] = output_loc + '.jpg'

      # TODO - ML Pipeline
      # save_image(result_image, bucket, output_loc + '_ml.png')
      # cv2.imwrite(output_loc + '_ml.png', result_image)
      # value['loc_ml'] = output_loc + '_ml.png'

      value['value'] = result[8]

    results.append(value)

  data['results'] = results

  student_overview_loc = output_dir + 'student_overview.jpg'
  # cv2.imwrite(student_overview_loc, student_filled_box)
  save_image(student_filled_box, bucket, student_overview_loc)

  data['overview'] = student_overview_loc

  # Write JSON Result File
  result_loc = output_dir + 'result.json'
  save_json(data, bucket, result_loc)

  return result_loc


def save_image(image, bucket, file_name):
  with TemporaryFile() as gcs_image:
    image.tofile(gcs_image)
    gcs_image.seek(0)
    blob = bucket.blob(file_name)
    blob.upload_from_file(gcs_image)

def save_json(json_data, bucket, file_name):
  with TemporaryFile() as gcs_file:
    gcs_file.write(json.dumps(json_data))

    gcs_file.seek(0)
    blob = bucket.blob(file_name)
    blob.upload_from_file(gcs_file)