  #! /usr/bin/env python
# importing ros stuffs
import rospy
from std_srvs.srv import *
import time
from time import sleep
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseActionGoal
from actionlib_msgs.msg import GoalStatusArray
from my_srv.srv import Finalassignment
target_reached_status = 0
def clbk_move_base_status(msg):
    global target_reached_status
    if (len(msg.status_list) > 0):
        if msg.status_list[0].status == 3:
	    target_reached_status = 1
def main():
    rospy.init_node('final_user_req')                               
    global target_reached_status, wall_follower_client
random_index_service = rospy.ServiceProxy('/finalassignment', Finalassignment)
    move_base_status = rospy.Subscriber('/move_base/status', GoalStatusArray, clbk_move_base_status, queue_size = 1)
    new_target_pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size = 1)
    wall_follower_client = rospy.ServiceProxy('/wall_follower_switch', SetBool)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
random_targets = [(-4,-3), (-4,2), (-4,7), (5,-7), (5,-3), (5,1)]
print("\nStarting...\n")
rate = rospy.Rate(20)
while not rospy.is_shutdown():
print("""\nInput option integer from 1 to 4:
|1| To move random in the environment with given values
|2| Robot should move as the input target position
|3| Robot will follow the walls
|4| To Stop at last position
x = int(raw_input("\nEnter a number from 1 to 4 corresponding to the chosen robot behavior: "))
if (x == 1):
resp = wall_follower_client(False)
resp = random_index_service(1,6)
rand_index = resp.target_index
print("\nNew position Target: (" + str(random_targets[rand_index -1][0]) + ", " + str(random_targets[rand_index -1][1]) + ")")
MoveBase_msg = MoveBaseActionGoal()
MoveBase_msg.goal.target_pose.header.frame_id = "map"
MoveBase_msg.goal.target_pose.pose.orientation.w = 1
MoveBase_msg.goal.target_pose.pose.position.x = random_targets[rand_index -1][0]
MoveBase_msg.goal.target_pose.pose.position.y = random_targets[rand_index -1][1]
new_target_pub.publish(MoveBase_msg)
print('\nRobot moves to the target position.')
sleep(15)
target_reached_status = 0
while(target_reached_status == 0):
sleep(1)
print('\nRobot reached the target.')
elif (x == 2):
resp = wall_follower_client(False)
print("""\nGiven Target coordinates:
1. (-4,-3)
2. (-4,2)
3. (-4,7) 
4. (5,-7)
5. (5,-3)
6. (5,1)""")
user_input = int(raw_input("\nEnter the desired target coordinates: "))
            print("\nnew target position is ("+ str(random_targets[user_input-1][0]) + ", " + str(random_targets[user_input-1][1]) + ")")
MoveBase_msg = MoveBaseActionGoal()
MoveBase_msg.goal.target_pose.header.frame_id = "map"
MoveBase_msg.goal.target_pose.pose.orientation.w = 1
MoveBase_msg.goal.target_pose.pose.position.x = random_targets[user_input-1][0]
MoveBase_msg.goal.target_pose.pose.position.y = random_targets[user_input-1][1]
new_target_pub.publish(MoveBase_msg)
print('\nRobot moves to the position.')
sleep(15)
target_reached_status = 0
while(target_reached_status == 0):
sleep(1)
print('\nRobot reached the position.')
elif (x == 3):
resp = wall_follower_client(True)
print('\nRobot demonstrates the wall-follower.')
elif (x == 4):
resp = wall_follower_client(False)
twist_msg = Twist()
twist_msg.linear.x = 0
twist_msg.angular.z = 0
pub.publish(twist_msg)
print('\nRobot stopped.')
else: 
continue
rate.sleep()
if _name_ == '_main_':
    main()       
 
