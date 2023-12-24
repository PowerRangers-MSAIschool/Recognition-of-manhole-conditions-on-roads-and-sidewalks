from django.shortcuts import render

from django.views.decorators import gzip
from django.http import StreamingHttpResponse, JsonResponse
from ultralytics import YOLO
import cv2

model = YOLO("./model/best.pt")
video_path = "./static/test_video/test1.mp4"
detect_status = dict(manhole_closed = None, manhole_hole = None, person= None)

# ------------------------------------------------
def video(request):
    try:
        # output을 HttpResponse에 주게 되고
        # stream()은 비디오캡처 후 객체인식 후 return
        output = stream()
        return StreamingHttpResponse(output, content_type="multipart/x-mixed-replace;boundary=frame")
    except: # This is bad! replace it with proper handling
        print("error..")
        pass

def stream():
    cap=cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        # frame_ = detect(ret, frame)
        results = model.track(frame, persist=True)
        if not ret:
            cap=cv2.VideoCapture(video_path)
            ret, frame = cap.read()
        
        frame_ = results[0].plot()
        for r in results :
            boxes = r.boxes.xyxy
            cls = r.boxes.cls
            conf = r.boxes.conf
            cls_dict = r.names
 
            detect_status.update({'manhole_closed':'False', 'manhole_hole': 'False', 'person': 'False'})  
            for box, cls_number, conf in zip(boxes, cls, conf) :
                conf_number = float(conf.item())
                cls_number_int = int(cls_number.item())
                cls_name = cls_dict[cls_number_int]
                x1, y1, x2, y2 = box
                
                if cls_number_int == 0:
                    detect_status['manhole_closed'] = 'True'
                elif cls_number_int == 1:
                    detect_status['manhole_hole'] = 'True'
                elif cls_number_int == 2:
                    detect_status['person'] = 'True'

            with open('./temp/detect_status.txt', 'w', encoding='UTF-8') as f:
                for item, status in detect_status.items(): 
                    f.write(f'{item} : {status}\n')
               
            cv2.imwrite('./temp/detect_image.jpg', frame_)
            if cv2.waitKey(1)==27:
                break
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('./temp/detect_image.jpg', 'rb').read() + b'\r\n')  
                

def read_detect_status_file():
    file_path = './temp/detect_status.txt'
    with open(file_path, 'r') as file:
        content = file.readlines()

    read_dict = {}
    for line in content:
        key, value = line.strip().split(' : ')
        read_dict[key] = value
    read_dict['sound']= 'False'
    return read_dict


def send_status(request):
    status_dict = read_detect_status_file()
    # manhole_hole과 person이 모두 1인 경우에 대한 조건 확인
    if status_dict['manhole_hole'] == 'True' and status_dict['person'] == 'True':
        # 원하는 처리 수행
        status_dict['sound']= 'True'
    else:
        pass
    return JsonResponse(status_dict)