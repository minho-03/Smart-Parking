#!/bin/bash
echo "🚀 도커: 비전 브릿지 & 브레이크 브릿지 동시 가동!"

# ROS 2 환경 세팅
source ../../install/setup.bash

# 두 브릿지 노드를 동시에 실행
python3 vision_bridge_node.py &
PID1=$!
python3 estop_bridge_node.py &
PID2=$!

# 종료 시 한 번에 꺼지도록 설정
trap "kill $PID1 $PID2; echo '🛑 도커 브릿지 종료 완료'; exit" SIGINT
wait