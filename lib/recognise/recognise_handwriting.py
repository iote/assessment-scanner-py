import numpy as np
import cv2

def recognise(results, tf_interpreter):
  
  # Load TFLite model and allocate tensors.
  tf_interpreter.allocate_tensors()

  # Get input and output tensors.
  input_details = tf_interpreter.get_input_details()
  output_details = tf_interpreter.get_output_details()

  final_res = []
  # Results tuple structure (idx, has_value, img_data, x, w, y, h)
  for (i, (idx, has_value, img, img_prep, x, w, y, h)) in enumerate(results):
    if(has_value):
      # ML Kit model expects 3-dim color space
      subject = cv2.cvtColor(img_prep, cv2.COLOR_GRAY2RGB)
      tf_interpreter.set_tensor(input_details[0]['index'], np.array([subject]))
      tf_interpreter.invoke()
      output_data = tf_interpreter.get_tensor(output_details[0]['index'])
    
      final_res.append((idx, has_value, img, img_prep, x, w, y, h, output_data[0].tolist()))
      
    else:
      final_res.append((idx, has_value, img, img_prep, x, w, y, h))

  return final_res