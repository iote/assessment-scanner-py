import sys
from lib import extract_numbers

 # Remove all annoying "future warnings"
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf

# Arguments:
# -t or --target-file: Target file for read
def is_target_param_id(arg):
  return arg == '-t' or arg == '--target-file'

# -o or --output-folder: Folder to write output to
def is_output_param_id(arg):
  return arg == '-o' or arg == '--output-folder'

tf_interpreter = tf.lite.Interpreter(model_path="subs/model/handwriting_read.tflite")
print('app_started')
# Execute Script.
args = input()

# Loop on input - React when target is not exit.
while (args != 'exit'):

  target = 0
  output_folder = 0
        # Debug signs { }
  # print('Input received: {' + args + '}')

  # Retrieve args from command - Expects "mark|-t|....|-o|....|
  split = args.split('|')
  for idx, arg in enumerate(split):
    if (idx == 0):
      if (arg == 'mark'):
        print('Mark command received. Unpacking params.')
      else:
        raise Exception('Invalid command. Cannot Execute so shutting down..')

    # -- Option 1: UnEven
    # This is supposed to be an argument identifier
    elif (idx % 2 == 1):
      if is_target_param_id(arg):
        target = split[idx + 1]

      elif is_output_param_id(arg):
        output_folder = split[idx + 1]

      else:
        raise Exception('Unkown argument identifier: ' + arg + '. Expected argument identifier -t or --target || -o or --output-folder.')

    # -- Option 2: Even
    # This is supposed to be an argument value
    elif is_target_param_id(arg) or is_output_param_id(arg):
      raise Exception('Did not provide value for argument identifier ' + split[idx - 1])

  # 3 - Check if both have been set.
  if (target == 0):        raise Exception('Cannot Execute. Target File param not set. Set target file with argument -t or --target-file following the file loc.')
  if (output_folder == 0): raise Exception('Cannot Execute. Output Folder param not set. Set output folder with argument -o or --output-folder following the folder loc.')

  # Execute script and return results via stdout
  # print('Calling run with target {' + target + '} and output_folder {' + output_folder + '}')
  extract_numbers.run(target, output_folder, tf_interpreter)
  print('mark_done')

  # Wait for next command.
  print('await')
  args = input()

print('exit')
