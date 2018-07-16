#coding=utf-8
import sys
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os
datagen = ImageDataGenerator(
        rotation_range=5,  #旋转
        width_shift_range=0.1, #平移
        height_shift_range=0.1,
        shear_range=0.2,  #裁剪
        zoom_range=0.2,  #缩放
        horizontal_flip=True, #镜像
        fill_mode='nearest')  #填充方式
images_dir="F:\\work_related\\Data\\blood_files-0403\\blood_val"
images=os.listdir(images_dir)
for image in images:
    image_name=image.split(".jpg")[0]
    img_path=os.path.join(images_dir,image)
    img = load_img(img_path)  # 这是一个PIL图像
    x = img_to_array(img)  # 把PIL图像转换成一个numpy数组，形状为(3, 150, 150)
    x = x.reshape((1,) + x.shape)  # 这是一个numpy数组，形状为 (1, 3, 150, 150)

    # 下面是生产图片的代码
    # 生产的所有图片保存在 `preview/` 目录下
    i = 0
    for batch in datagen.flow(x, batch_size=1,
                              save_to_dir='F:\\work_related\\Data\\blood_files-0403\\blood_val_aug', save_prefix=image_name, save_format='jpg'):
        i += 1

        if i > 3:
            print ("done！")
            break  # 否则生成器会退出循环