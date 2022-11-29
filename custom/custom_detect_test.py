import cv2
import numpy as np
import tensorflow as tf
import tensorflow.compat.v1 as tf
import PIL
def k_classification(image, height, width, central_fraction=0.975):

  with tf.name_scope('eval_image'):
    # image = Image.open(SAVE_PATH)
    # image = np.array(image)
    if image.dtype != tf.float32:
      image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    image = tf.image.central_crop(image, central_fraction=central_fraction)
    image = tf.expand_dims(image, 0)
    image = tf.compat.v1.image.resize_bilinear(image, [height, width], align_corners=False)
    image = tf.squeeze(image, [0])
    image = tf.subtract(image, 0.5)
    image = tf.multiply(image, 2.0)
    image.set_shape([height, width, 3])
    #image = np.expand_dims(image, axis=0)
    np_arr = image.numpy()
    img = PIL.Image.fromarray((np_arr*255).astype(np.uint8))
    img = np.array(img.getdata()).reshape(img.size[0], img.size[1], 3).astype(np.uint8)
    imgsave = PIL.Image.fromarray(img)
    img = np.expand_dims(image, axis =0)
    print(f'K 입력 받은 데이터 셋 : {img.shape}')

    return img

def o_classification(image):
    

    ori = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (299, 299))
    ori = cv2.resize(ori, (224,224))
    ori_blur = cv2.medianBlur(ori, 3)
    ori_img = cv2.cvtColor(ori_blur, cv2.COLOR_GRAY2BGR)
    image = np.expand_dims(image, axis=0)
    ori_img =np.expand_dims(ori_img,axis=0)
    print(f'O 입력 받은 데이터 셋 : {type(ori_img)}')

    return ori_img


image = cv2.imread('/home/super/bang/origin/train/C2/0014__3_.jpg')

def dummy():
  dummy_image = np.zeros((299, 299, 3), dtype = np.uint8)
  orientation_image = cv2.cvtColor(dummy_image,cv2.COLOR_BGR2GRAY)
  dummy_image = np.expand_dims(dummy_image, axis = 0)
  print(type(dummy_image))

k_classification(image,299,299)

o_classification(image)

dummy()