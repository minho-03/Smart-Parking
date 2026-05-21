#!/bin/bash
echo "🚀 맥북: 카메라 비전 & 아두이노 감시 동시 가동!"

# 두 파이썬 파일을 백그라운드에서 동시에 실행
python3 mac_parking_vision.py &
PID1=$!
python3 mac_arduino_estop.py &
PID2=$!

# 터미널에서 Ctrl+C를 누르면 두 프로그램이 한 번에 깔끔하게 꺼지도록 설정
trap "kill $PID1 $PID2; echo '🛑 맥북 시스템 종료 완료'; exit" SIGINT
wait