#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import os

class VisionBridgeNode(Node):
    def __init__(self):
        super().__init__('vision_bridge_node')
        self.goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)
        
        # 💡 만약 로봇이 안 움직인다면 여기 x, y 좌표를 내 맵에 맞게 수정하세요!
        self.parking_coordinates = {
            "ZONE_00": {"x": 4.59, "y": -1.72, "oz": 0.0, "ow": 1.0},
            "ZONE_01": {"x": 0.684, "y": -2.05, "oz": 0.0, "ow": 1.0},
            "ZONE_02": {"x": 4.26, "y": 1.29, "oz": 1.0, "ow": 0.0},
            "ZONE_03": {"x": 0.412, "y": 0.893, "oz": 1.0, "ow": 0.0}
        }
        
        # ✨ 핵심: 0.1초마다 target_signal.txt 파일이 생겼는지 감시합니다.
        self.timer = self.create_timer(0.1, self.check_file_callback)
        self.get_logger().info("✅ 비전 브릿지 가동! 텍스트 파일 신호를 기다립니다...")

    def check_file_callback(self):
        file_path = 'target_signal.txt'
        # 파일 우체통에 편지가 들어왔는지 확인!
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    msg = f.read().strip()
                
                if msg in self.parking_coordinates:
                    self.get_logger().info(f"📥 맥북으로부터 신호 수신 완료: [{msg}]")
                    self.publish_nav2_goal(self.parking_coordinates[msg])
                
                # 로봇에게 명령을 내린 후 파일을 깨끗하게 지워서 다음 신호를 대기합니다.
                os.remove(file_path)
            except Exception:
                pass

    def publish_nav2_goal(self, zone_info):
        goal_msg = PoseStamped()
        goal_msg.header.stamp = self.get_clock().now().to_msg()
        goal_msg.header.frame_id = 'map'
        
        goal_msg.pose.position.x = zone_info["x"]
        goal_msg.pose.position.y = zone_info["y"]
        goal_msg.pose.orientation.z = zone_info["oz"]
        goal_msg.pose.orientation.w = zone_info["ow"]
        
        self.goal_pub.publish(goal_msg)
        self.get_logger().info(f"🚀 Nav2 로봇 출발! 목적지 (X: {zone_info['x']}, Y: {zone_info['y']})")

def main(args=None):
    rclpy.init(args=args)
    node = VisionBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()