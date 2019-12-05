import json
import cv2
import os, sys

# Function that writes the result in a json object
# Arguments:
#   1 - Result Array. Of the form [(i, has_value, result_image, x, w, y, h)]
#   2 - output_dir. Dir to write the images to
def write(student_filled_box, algo_result, subj_group, stream, assessment):
  
  print(algo_result, file=sys.stderr)
  # Create output Dir - Write permissions for owner / Read for everyone else. No exec permissions.
  os.mkdir('assessments', 755)
  os.mkdir('assessments/' + subj_group, 755)
  os.mkdir('assessments/' + subj_group + '/' + stream , 755)

  output_dir = 'assessments/' + subj_group + '/' + stream + '/' + 'assessment' 
  os.mkdir(output_dir, 755)

  # Prepare for reading
  data = {}
  data['reads'] = len(algo_result);
  results = []

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
      output_loc = output_dir + '/num_' + str(i);

      print(output_loc, file=sys.stderr)

      cv2.imwrite(output_loc + '.png', image)
      cv2.imwrite(output_loc + '_ml.png', result_image)

      value['loc'] = output_loc + '.png'
      value['loc_ml'] = output_loc + '_ml.png'

      value['value'] = result[8]

    results.append(value)

  data['results'] = results

  student_overview_loc = output_dir + 'student_overview.png'
  cv2.imwrite(student_overview_loc, student_filled_box)
  data['overview'] = student_overview_loc

  json_result_object = json.dumps(data)

  # Write JSON Result File
  f = open(output_dir + 'result.json', "w")
  f.write(json_result_object)
  f.close()

  return output_dir + 'result.json'