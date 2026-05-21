#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import os

class EstopBridgeNode(Node):
    def __init__(self):
        super().__init__('estop_bridge_node')
        
        # 💡 다양한 조종 채널에 정지 명령을 동시 다발적으로 쏘기 위해 퍼블리셔 2개 준비
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.cmd_vel_teleop_pub = self.create_publisher(Twist, '/cmd_vel_teleop', 10)
        
        self.is_emergency = False
        
        # 1. 우체통 확인용 타이머 (0.1초마다 편지 확인)
        self.file_timer = self.create_timer(0.1, self.check_file_callback)
        
        # 2. 🚨 긴급 정지 폭격용 타이머 (0.01초마다 = 100Hz로 Nav2를 압도함)
        self.stop_timer = self.create_timer(0.01, self.enforce_stop_callback)
        
        self.get_logger().info("✅ 브릿지 가동! 강력한 100Hz 브레이크가 장착되었습니다.")

    def check_file_callback(self):
        file_path = 'estop_signal.txt'
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    msg = f.read().strip()
                
                # 버튼이 눌렸을 때
                if msg == "STOP" and not self.is_emergency:
                    self.get_logger().error("🚨🚨 긴급 정지! 자율주행 모터를 강제 차단합니다! 🚨🚨")
                    self.is_emergency = True
                    
                # 버튼을 뗐을 때 (다시 정상 주행 가능)
                elif msg == "RESUME" and self.is_emergency:
                    self.get_logger().info("✅ 브레이크 해제. 로봇이 다시 주행할 수 있습니다.")
                    self.is_emergency = False
                
                # 우체통 비우기
                os.remove(file_path)
            except Exception:
                pass

    def enforce_stop_callback(self):
        # 긴급 정지 상태일 때만 0.01초(1초에 100번)마다 속도 0을 난사해서 자율주행 명령을 씹어먹습니다.
        if self.is_emergency:
            twist = Twist()
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.linear.z = 0.0
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = 0.0
            
            # 메인 모터와 우선순위가 높은 수동조종(teleop) 모터 양쪽에 모두 정지 신호 쏘기
            self.cmd_vel_pub.publish(twist)
            self.cmd_vel_teleop_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = EstopBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()