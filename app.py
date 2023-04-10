import streamlit as st
import cv2
import torch
from utils.hubconf import custom
import numpy as np
import tempfile
import time
from collections import Counter
import json
import pandas as pd
from model_utils import get_yolo, color_picker_fn, get_system_stat
from ultralytics import YOLO


p_time = 0

st.sidebar.title('设置')
# Choose the model
model_type = st.sidebar.selectbox(
    '选择 模型 版本', ('模型','YOLOv8', 'YOLOv7')
)

st.title(f'{model_type} 预测')
sample_img = cv2.imread('logo.jpg')
FRAME_WINDOW = st.image(sample_img, channels='BGR')
cap = None

if not model_type == '模型':
    path_model_file = st.sidebar.text_input(
        f'{model_type} 模型的位置:',
        f'/root/work/project/{model_type}.pt'
    )
    if st.sidebar.checkbox('加载 模型'):
        
        # YOLOv7 Model
        if model_type == 'YOLOv7':
            # GPU
            gpu_option = st.sidebar.radio(
                'PU Options:', ('CPU', 'GPU'))

            if not torch.cuda.is_available():
                st.sidebar.warning('GPU 暂时不可用, 所以选择 CPU', icon="⚠️")
            else:
                st.sidebar.success(
                    'GPU 可用, 性能更佳',
                    icon="✅"
                )
            # Model
            if gpu_option == 'CPU':
                model = custom(path_or_model=path_model_file)
            if gpu_option == 'GPU':
                model = custom(path_or_model=path_model_file, gpu=True)

        # YOLOv8 Model
        if model_type == 'YOLOv8':
            model = YOLO(path_model_file)

        # Load Class names
        class_labels = model.names

        # Inference Mode
        options = st.sidebar.radio(
            '选项:', ('摄像头', '图片', '视频', 'RTSP协议实时流媒体'), index=1)

        # Confidence
        confidence = st.sidebar.slider(
            '预测 置信度', min_value=0.0, max_value=1.0, value=0.25)

        # Draw thickness
        draw_thick = st.sidebar.slider(
            '拉伸 厚度:', min_value=1,
            max_value=20, value=3
        )
        
        color_pick_list = []
        for i in range(len(class_labels)):
            classname = class_labels[i]
            color = color_picker_fn(classname, i)
            color_pick_list.append(color)

        # Image
        if options == '图片':
            upload_img_file = st.sidebar.file_uploader(
                '上传 图片', type=['jpg', 'jpeg', 'png'])
            if upload_img_file is not None:
                pred = st.checkbox(f'使用 {model_type} 探测')
                file_bytes = np.asarray(
                    bytearray(upload_img_file.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, 1)
                FRAME_WINDOW.image(img, channels='BGR')

                if pred:
                    img, current_no_class = get_yolo(img, model_type, model, confidence, color_pick_list, class_labels, draw_thick)
                    FRAME_WINDOW.image(img, channels='BGR')

                    # Current number of classes
                    class_fq = dict(Counter(i for sub in current_no_class for i in set(sub)))
                    class_fq = json.dumps(class_fq, indent = 4)
                    class_fq = json.loads(class_fq)
                    df_fq = pd.DataFrame(class_fq.items(), columns=['Class', 'Number'])
                    
                    # Updating Inference results
                    with st.container():
                        st.markdown("<h2>预测 统计</h2>", unsafe_allow_html=True)
                        st.markdown("<h3>当前框架中检测到的物体</h3>", unsafe_allow_html=True)
                        st.dataframe(df_fq, use_container_width=True)
        
        # Video
        if options == '视频':
            upload_video_file = st.sidebar.file_uploader(
                '上传 视频', type=['mp4', 'avi', 'mkv'])
            if upload_video_file is not None:
                pred = st.checkbox(f'使用 {model_type} 探测')

                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(upload_video_file.read())
                cap = cv2.VideoCapture(tfile.name)
                # if pred:


        # Web-cam
        if options == '摄像头':
            cam_options = st.sidebar.selectbox('摄像头 频道',
                                            ('选择 频道', '0', '1', '2', '3'))
        
            if not cam_options == '选择 频道':
                pred = st.checkbox(f'使用 {model_type} 探测')
                cap = cv2.VideoCapture(int(cam_options))


        # RTSP
        if options == 'RTSP协议实时流媒体':
            rtsp_url = st.sidebar.text_input(
                'RTSP 地址:',
                'eg: rtsp://admin:name6666@198.162.1.58/cam/realmonitor?channel=0&subtype=0'
            )
            pred = st.checkbox(f'使用 {model_type} 探测')
            cap = cv2.VideoCapture(rtsp_url)


if (cap != None) and pred:
    stframe1 = st.empty()
    stframe2 = st.empty()
    stframe3 = st.empty()
    while True:
        success, img = cap.read()
        if not success:
            st.error(
                f"{options} 无法工作\n 请检查设置 !!",
                icon="🚨"
            )
            break

        img, current_no_class = get_yolo(img, model_type, model, confidence, color_pick_list, class_labels, draw_thick)
        FRAME_WINDOW.image(img, channels='BGR')

        # FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        
        # Current number of classes
        class_fq = dict(Counter(i for sub in current_no_class for i in set(sub)))
        class_fq = json.dumps(class_fq, indent = 4)
        class_fq = json.loads(class_fq)
        df_fq = pd.DataFrame(class_fq.items(), columns=['Class', 'Number'])
        
        # Updating Inference results
        get_system_stat(stframe1, stframe2, stframe3, fps, df_fq)