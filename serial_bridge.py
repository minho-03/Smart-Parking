import serial
import time

ARDUINO_PORT = '/dev/cu.usbserial-110' 
BAUD_RATE = 115200

def main():
    print(f"[{ARDUINO_PORT}] 아두이노와 연결을 시도합니다...")
    try:
        # 시리얼 포트 열기
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) # 연결 안정화를 위한 2초 대기
        print("✅ 통신 브릿지 연결 성공! 스위치를 눌러보세요. (종료는 Ctrl+C)")

        while True:
            # 아두이노에서 넘어온 데이터가 있다면
            if ser.in_waiting > 0:
                # 데이터를 한 줄 읽어서 문자열로 변환 (엔터 공백 제거)
                line = ser.readline().decode('utf-8').strip()
                
                # 수신된 데이터에 따른 동작 제어
                if line == "EMERGENCY_STOP":
                    print("🚨 [E-STOP 활성화] 가제보 로봇 강제 정지 신호 발생!!")
                    # 향후 이 부분에 ROS2 '/emergency_stop' 토픽 발행 코드가 들어갑니다.
                elif line == "RELEASED":
                    print("🟢 [E-STOP 해제] 시스템 정상 상태 복귀.")
                    
    except serial.SerialException as e:
        print(f"❌ 포트 연결 오류: {e} (포트 이름이 맞는지, 시리얼 모니터가 켜져 있는지 확인하세요)")
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

        
if __name__ == '__main__':
    main()