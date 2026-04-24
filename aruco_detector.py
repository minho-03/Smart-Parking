import cv2
import numpy as np

# 마커 ID 0~3번에 각각 주차 구역을 매칭
PARKING_ZONES = {
    0: "Zone A_01",
    1: "Zone A_02",
    2: "Zone B_01",
    3: "Zone B_02"
}

def main():
    print("카메라를 초기화하는 중입니다...")
    
    # ArUco 마커 탐지기 설정
    # DICT_4X4_50: 4x4 픽셀 구조를 가진 50개의 마커 사전
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    # 카메라 켜기
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("❌ 카메라를 열 수 없습니다. 권한을 확인해 주세요.")
        return

    print("✅ 카메라 켜짐! ArUco 마커를 카메라에 보여주세요. (종료는 'q' 키)")

    current_target = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽어올 수 없습니다.")
            break

        # 마커 인식률을 높이기 위해 이미지를 흑백으로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 마커 탐지 실행
        corners, ids, rejected = detector.detectMarkers(gray)

        # 마커가 화면에 하나라도 인식되면
        if ids is not None:
            # 인식된 마커 테두리에 네모 박스 그리기
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # 인식된 모든 마커에 대해 반복
            for i in range(len(ids)):
                marker_id = ids[i][0]
                
                # 설정한 주차장 ID(0~3) 안에 있는 마커이면
                if marker_id in PARKING_ZONES:
                    target_zone = PARKING_ZONES[marker_id]
                    
                    # 마커 근처에 목적지 텍스트 띄우기
                    cv2.putText(frame, f"Target: {target_zone}", 
                                (int(corners[i][0][0][0]), int(corners[i][0][0][1]) - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
                    if current_target != target_zone:
                        print(f"🎯 주차 명령 수신: [ID: {marker_id}] -> {target_zone} (으)로 이동합니다.")
                        current_target = target_zone  # 방금 내린 명령을 기억해둠
                else:
                        print("❌ 등록되지 않는 마커입니다.")

        # 결과 화면 보여주기
        cv2.imshow('Smart Parking Vision', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()