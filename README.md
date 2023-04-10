# YOLO Streamlit Dashbord
使用带有 Streamlit 的 YOLO 模型（**YOLOv7** 和 **YOLOv8**）显示预测的视频、图像和网络摄像头

### Sample Streamlit YOLOv7 Dashboard English
Streamlit Dashboard: https://naseemap47-streamlit-yolov7-app-deploy-bfr4xt.streamlitapp.com/

## Docker
dockerhub: https://hub.docker.com/repository/docker/v1eerie/streamlit-yolo

#### 1. Pull Docker Image
```
docker pull v1eerie/streamlit-yolo
```
#### 2. Change permistion
```
sudo xhost +si:localuser:root
```
#### 3. RUN Docker Image
```
docker run --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix --ipc=host --device=/dev/video0:/dev/video0 -p 8502 -it --rm v1eerie/streamlit-yolo
```

## 🚀 New Update (10/02/2023)
Integrated new YOLOv8 model, now you can run YOLOv8 model on RTSP, Webcam, Video and Image

## Streamlit Options
### Modes
 - RTSP
 - Webcam
 - Video
 - Image
 
 ## Sample Streamlit Dashboard Output
 
 [out.webm](https://user-images.githubusercontent.com/88816150/193816239-b351c3d6-1d9a-4820-87b5-0cfec1ad5d90.webm)

 ## StepUp
```
git clone https://github.com/v1eerie/streamlit-yolov7.git
cd streamlit-yolov7
```
Install dependency
```
pip3 install -r requirements.txt
```
Run **Streamlit**
```
streamlit run app.py
```

