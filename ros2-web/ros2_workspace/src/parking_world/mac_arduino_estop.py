import serial
import time
import os

# 🔌 맥북 아두이노 포트 설정
PORT = '/dev/cu.usbserial-130'
BAUD = 115200

try:
    py_serial = serial.Serial(PORT, BAUD, timeout=1)
    print(f"🔌 맥북 아두이노 연결 성공! ({PORT})")
except Exception as e:
    print(f"❌ 아두이노 연결 실패: {e}")
    print("포트 이름이 맞는지, 아두이노가 잘 꽂혀있는지 확인하세요.")
    exit()

print("🛑 긴급 정지 버튼 감시 시작... (종료는 Ctrl+C)")
current_state = "NORMAL"

while True:
    if py_serial.in_waiting > 0:
        # 아두이노가 보낸 데이터 읽기 (보통 버튼 누르면 "EMERGENCY", 떼면 "NORMAL")
        line = py_serial.readline().decode('utf-8', errors='ignore').strip()
        
        if line:
            print(f"📡 아두이노 신호: {line}")
            
            # 상태가 바뀌었을 때만 파일 우체통에 기록합니다.
            if line == "EMERGENCY_STOP" and current_state != "EMERGENCY_STOP":
                print("🚨 긴급 상황 발생! 도커로 정지 신호 전송!")
                with open('estop_signal.txt', 'w') as f:
                    f.write("STOP")
                current_state = "EMERGENCY_STOP"
                
            elif line == "RELEASED" and current_state == "EMERGENCY_STOP":
                print("✅ 상황 해제! 도커로 복구 신호 전송!")
                with open('estop_signal.txt', 'w') as f:
                    f.write("RESUME")
                current_state = "RELEASED"
                
    time.sleep(0.01)