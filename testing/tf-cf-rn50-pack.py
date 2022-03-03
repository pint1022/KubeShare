#reference https://adventuresinmachinelearning.com/introduction-resnet-tensorflow-2/

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import datetime as dt
from time import time
import argparse
import datetime
import os

from tensorflow.compat.v1.keras.backend import set_session
from tensorflow.compat.v1 import Session, ConfigProto, GPUOptions
tf_config = ConfigProto(gpu_options=GPUOptions(allow_growth=True))
session = Session(config=tf_config)
set_session(session)

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--epochs', default=5, type=int, metavar='N',
                    help='number of total epochs to run')
parser.add_argument('-b', '--batch', default=256, type=int,
                    help='batch size')
parser.add_argument('-m', '--memory', default=5000, type=float,
                    help='memory limit (max 12196 on titan)')
args = parser.parse_args()

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=args.memory)])
    except RuntimeError as e:
        print(e)

#load CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
x_train = x_train.astype('float32') / 256
x_test = x_test.astype('float32') / 256


#build the ResNet network
inputs = keras.Input(shape=(32, 32, 3)) # based on cifar10 image size
x = layers.Conv2D(32, 3, activation='relu')(inputs)
x = layers.Conv2D(64, 3, activation='relu')(x)
x = layers.MaxPooling2D(3)(x)


def res_net_block(input_data, filters, conv_size):
  x = layers.Conv2D(filters, conv_size, activation='relu', padding='same')(input_data)
  x = layers.BatchNormalization()(x)
  x = layers.Conv2D(filters, conv_size, activation=None, padding='same')(x)
  x = layers.BatchNormalization()(x)
  x = layers.Add()([x, input_data])
  x = layers.Activation('relu')(x)
  return x

num_res_net_blocks = 50
for i in range(num_res_net_blocks):
    x = res_net_block(x, 64, 3)

x = layers.Conv2D(64, 3, activation='relu')(x)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(256, activation='relu')(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(10, activation='softmax')(x)

res_net_model = keras.Model(inputs, outputs)

#for other purpose to replace res_net_block
def non_res_block(input_data, filters, conv_size):
  x = layers.Conv2D(filters, conv_size, activation='relu', padding='same')(input_data)
  x = layers.BatchNormalization()(x)
  x = layers.Conv2D(filters, conv_size, activation='relu', padding='same')(x)
  x = layers.BatchNormalization()(x)
  return x

##output to tensorboard
log_dir = 'rlogs/cf_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, profile_batch = '500,520')
callbacks = [
## Write TensorBoard logs to `/tmp/logs` directory
#  keras.callbacks.TensorBoard(log_dir='~/tmp/logs/{}'.format(dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")), write_images=True),
  tensorboard_callback,
]

res_net_model.compile(optimizer=keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['acc'])
start = time()
with tf.device("/gpu:0"):
  res_net_model.fit(x_train, y_train, batch_size=args.batch, epochs=args.epochs, validation_data=(x_test, y_test), shuffle=True, callbacks=callbacks)

print("======== training time {} sec".format(time()-start))
