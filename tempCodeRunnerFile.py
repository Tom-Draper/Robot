lay_sensors():
#     plt.plot([robot.x, robot.x + (robot.sensor_centre.length * robot.direction.x)], 
#              [robot.y, robot.y + (robot.sensor_centre.length * robot.direction.y)], 
#              color='r')
    
#     rotated_left_x, rotated_left_y = robot.direction.rotated(robot.sensor_mid_left.rotation)
#     plt.plot([robot.x, robot.x + (robot.sensor_mid_left.length * rotated_left_x)], 
#             [robot.y, robot.y + (robot.sensor_mid_left.length * rotated_left_y)], 
#             color='r')
    
#     rotated_right_x, rotated_right_y = robot.direction.rotated(robot.sensor_mid_right.rotation)
#     plt.plot([robot.x, robot.x + (robot.sensor_mid_right.length * rotated_right_x)], 
#             [robot.y, robot.y + (robot.sensor_mid_right.length * rotated_right_y)], 
#             color='r')
    
#     rotated_left_x, rotated_left_y = robot.direction.rotated(robot.sensor_left.rotation)
#     plt.plot([robot.x, robot.x + (robot.sensor_left.length * rotated_left_x)], 
#             [robot.y, robot.y + (robot.sensor_left.length * rotated_left_y)], 
#             color='r')
    
#     rotated_right_x, rotated_right_y = robot.direction.rotated(robot.sensor_right.rotation)
#     plt.plot([robot.x, robot.x + (robot.sensor_right.length * rotated_right_x)], 
#             [robot.y, robot.y + (robot.sensor_right.length * rotated_right_y)], 
#             color='r')