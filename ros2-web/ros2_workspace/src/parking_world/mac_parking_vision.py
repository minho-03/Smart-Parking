import cv2
import time
import os

print("🌐 도커와 텍스트 파일 공유 통신 준비 완료")

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ 맥북 카메라를 열 수 없습니다!")
    exit()

print("📸 맥북 카메라 활성화 성공! 마커를 보여주세요. (종료는 Q키)")
current_target = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        for i in range(len(ids)):
            marker_id = ids[i][0]
            
            if marker_id in [0, 1, 2, 3]:
                target_name = f"ZONE_0{marker_id}"
                
                cv2.putText(frame, f"Send: {target_name}", 
                            (int(corners[i][0][0][0]), int(corners[i][0][0][1]) - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                if current_target != target_name:
                    print(f"🎯 마커 {marker_id} 감지! 텍스트 파일로 신호 전송 ➔ {target_name}")
                    
                    # ✨ 핵심: 네트워크 대신 텍스트 파일(우체통)에 목적지를 적어둡니다!
                    with open('target_signal.txt', 'w') as f:
                        f.write(target_name)
                        
                    current_target = target_name

    cv2.imshow('Mac WebCam - Parking Vision', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()