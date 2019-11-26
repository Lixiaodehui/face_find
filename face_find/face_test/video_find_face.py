# OpenCv 调用摄像头
# 默认调用笔记本摄像头

# Author:  coneypo
# Blog:   http://www.cnblogs.com/AdaminXie
# GitHub:  https://github.com/coneypo/Dlib_face_cut
# Mail:   coneypo@foxmail.com

import dlib
import cv2
import os
import compare_face as fc
import datetime
import numpy as np

#人脸68特征读取
person_num_list = []

detector = dlib.get_frontal_face_detector()

face_rec = fc.face_recognition()  # 创建对象


def getAllFace68():

    # 图片所在路径
    imgs_path = 'test/'
    filelist = os.listdir(imgs_path)
    # 使用 detector 检测器来检测图像中的人脸
    for img_path in filelist:
        img = cv2.imread(imgs_path + img_path)
        face_rec.inputPerson2(name=img_path, img_bgr=img)  # name中写第一个人名字，img_name为图片名字，注意要放在faces文件夹中
        vector = face_rec.create128DVectorSpace()  # 提取128维向量，是dlib.vector类的对象
        person_data1 = fc.savePersonData(face_rec, vector)  # 将提取出的数据保存到data文件夹，为便于操作返回numpy数组，内容还是一样的
        # print(person_data1)
        person_num_list.append(person_data1)

def comparePersonData1(data1):

    if np.all(data1!=None):
        # for v1, v2 in data1, data2:
            # diff += (v1 - v2)**2
        j = 0
        for allperson in person_num_list:
            diff = 0
            j += 1
            data2 = allperson
            for i in range(len(data1)):
                diff += (data1[i] - data2[i])**2
            diff = np.sqrt(diff)

            print(diff)
            if(diff < 0.45):
                print ("It's the *********** same  *********** person")
                break
            else:
                print ("It's not the same person")




#获取所有人脸特征
getAllFace68()
url = "rtsp://admin:sailing@172.20.36.200"
cap = cv2.VideoCapture(0)

# cap = cv2.VideoCapture(url)

# cap.set(propId, value)
# 设置视频参数: propId - 设置的视频参数, value - 设置的参数值
cap.set(3, 480)

# cap.isOpened() 返回 true/false, 检查摄像头初始化是否成功
print("检查摄像头初始化是否成功",cap.isOpened())

# cap.read()
""" 
返回两个值
  先返回一个布尔值, 如果视频读取正确, 则为 True, 如果错误, 则为 False; 
  也可用来判断是否到视频末尾;

  再返回一个值, 为每一帧的图像, 该值是一个三维矩阵;

  通用接收方法为: 
    ret,frame = cap.read();
    ret: 布尔值;
    frame: 图像的三维矩阵;
    这样 ret 存储布尔值, frame 存储图像;

    若使用一个变量来接收两个值, 如:
      frame = cap.read()
    则 frame 为一个元组, 原来使用 frame 处需更改为 frame[1]
"""

while cap.isOpened():
    ret_flag, img_camera = cap.read()
    cv2.imshow("camera", img_camera)

    # 每帧数据延时 1ms, 延时为0, 读取的是静态帧
    k = cv2.waitKey(1)

    # 取灰度
    img_gray = cv2.cvtColor(img_camera, cv2.COLOR_RGB2GRAY)

    # 人脸数
    faces = detector(img_gray, 0)


    # # 按下 's' 保存截图
    # if k == ord('s'):
    #     cv2.imwrite("test.jpg", img_camera)
    # 待会要写的字体
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 按下 'q' 退出
    if k == ord('q'):
        break
    else:
        # 检测到人脸
        if len(faces) > 0:
            # 记录每次开始写入人脸像素的宽度位置
            faces_start_width = 0

            for face in faces:
                # 绘制矩形框
                cv2.rectangle(img_camera, tuple([face.left(), face.top()]), tuple([face.right(), face.bottom()]),
                              (0, 255, 255), 2)

                height = face.bottom() - face.top()
                width = face.right() - face.left()

                ### 进行人脸裁减 ###
                # 如果没有超出摄像头边界
                if (face.bottom() < 480) and (face.right() < 640) and \
                        ((face.top() + height) < 480) and ((face.left() + width) < 640):
                    # 填充
                    for i in range(height):
                        for j in range(width):
                            img_camera[i][faces_start_width + j] = \
                                img_camera[face.top() + i][face.left() + j]

                    # 更新 faces_start_width 的坐标
                    faces_start_width += width

                    # cv2.putText(img_camera, "Faces in all: " + str(len(faces)), (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
                    # +datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')
                    face_rec.inputPerson2(name='抓拍', img_bgr=img_camera)  # name中写第一个人名字，img_name为图片名字，注意要放在faces文件夹中
                    vector = face_rec.create128DVectorSpace()  # 提取128维向量，是dlib.vector类的对象
                    person_data2 = fc.savePersonData(face_rec, vector)  # 将提取出的数据保存到data文件夹，为便于操作返回numpy数组，内容还是一样的

                    comparePersonData1(person_data2)


# 释放所有摄像头
cap.release()

# 删除建立的所有窗口
cv2.destroyAllWindows()

