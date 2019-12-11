import json
import cv2
import os, sys

# Function that writes the result in a json object
# Arguments:
#   1 - Result Array. Of the form [(i, has_value, result_image, x, w, y, h)]
#   2 - output_dir. Dir to write the images to
def write(student_filled_box, algo_result, subj_group, stream, assessment, sheetn, base_i):

  #print('WRITE_RESULTS.PY: Starting write', file=sys.stderr)
  new_subj_group = subj_group.replace('"', "")
  new_stream = stream.replace('"', "")
  new_assessment = assessment.replace('"', "")

  # Create output Dir - Write permissions for owner / Read for everyone else. No exec permissions.
  path_1 = os.path.join('assessments', new_subj_group)
  path_2 = os.path.join(path_1, new_stream)
  path_3 = os.path.join(path_2, new_assessment)
  output_dir = os.path.join(path_3, str(sheetn))

  # os.mkdir('assessments', 755)
  # os.mkdir('assessments/' + subj_group, 755)
  # os.mkdir('assessments/' + subj_group + '/' + stream , 755)

  # output_dir = 'assessments/' + subj_group + '/' + stream + '/' + 'assessment' 

  # Check if directory exists to prevent FileExistsError - If it exists, will be overwritten by imwrite below
  if not os.path.exists(output_dir):
    os.makedirs(output_dir, 755)

  # Prepare for reading
  data = {}
  data['reads'] = len(algo_result);
  results = []

  # Structure of result (i, has_value, result_image, x, w, y, h, value?)
  for index, result in enumerate(algo_result):

    i = base_i + result[0]
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
      cv2.imwrite(output_loc + '.png', image)
      cv2.imwrite(output_loc + '_ml.png', result_image)

      value['loc'] = output_loc + '.png'
      value['loc_ml'] = output_loc + '_ml.png'

      value['value'] = result[8]

    results.append(value)

  data['results'] = results

  student_overview_loc = output_dir + '/student_overview.png'
  cv2.imwrite(student_overview_loc, student_filled_box)
  data['overview'] = student_overview_loc
  data['result_loc'] = output_dir + '/result.json'
  json_result_object = json.dumps(data)

  # Write JSON Result File
  f = open(output_dir + '/result.json', "w")
  f.write(json_result_object)
  f.close()

  #print('WRITE_RESULTS.PY: Finished write. RES: ' + output_dir + '/result.json', file=sys.stderr)

  return json_result_object