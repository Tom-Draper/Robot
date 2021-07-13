import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def rotate(self, angle):
        new_x = self.x * np.cos(angle) - self.y * np.sin(angle)
        new_y = self.x * np.sin(angle) + self.y * np.cos(angle)
        
        self.x = new_x
        self.y = new_y
    
    def rotated(self, angle):
        new_x = self.x * np.cos(angle) - self.y * np.sin(angle)
        new_y = self.x * np.sin(angle) + self.y * np.cos(angle)
        
        return new_x, new_y


class Sensor:
    def __init__(self, length=10, rotation=0):
        self.length = length
        self.end_point = None
        self.rotation = rotation  # 0 for centre, 1.57 for left, -1.57 for right


class Robot:
    def __init__(self, speed=1, start_x=50, start_y=50, direction=Vector(0, 1), sensor_centre_size=10, sensor_mid_size=10, sensor_wide_size=10):
        self.speed = speed
        self.x = start_x
        self.y = start_y
        
        self.direction = direction
        
        self.sensor_left = Sensor(sensor_wide_size, 1.5708)  # 90 degree left
        self.sensor_mid_left = Sensor(sensor_mid_size, 0.7853)  # 45 degree left
        self.sensor_centre = Sensor(sensor_centre_size, 0)
        self.sensor_mid_right = Sensor(sensor_mid_size, -0.7853)  # 45 degree right
        self.sensor_right = Sensor(sensor_wide_size, -1.5708)  # 90 degree right
        
        self.size = 6  # Display size
    
    def checkSensor(self, sensor, max_robot_rotation):
        # Get vector directino of this sensor
        sensor_x, sensor_y = robot.direction.rotated(sensor.rotation)

        current_location = (self.x, self.y)
        sensor_end = (self.x + (sensor.length * sensor_x), self.y + (sensor.length * sensor_y))
                
        xs, ys = interval_range(current_location, sensor_end)
        
        sensor.end_point = sensor_end
        for i, (x, y) in enumerate(zip(xs, ys)):
            if (int(round(x)), int(round(y))) in obstacles.coords:
                print("FOUND OBSTACLE")
                sensor.end_point = (x, y)
                # Suggest rotate right, harder rotate the closer the obstacle
                return max_robot_rotation * (1 - (i/len(xs)))
            
        return 0
  
    def checkSensors(self):
        # Sum all of the suggested rotations give by each sensor
        rotation = 0
        if random.randint(0, 1) == 0:
            rotation += self.checkSensor(self.sensor_centre, 1)
        else:
            rotation += self.checkSensor(self.sensor_centre, -1)
        rotation += self.checkSensor(self.sensor_mid_left, -0.8)
        rotation += self.checkSensor(self.sensor_mid_right, 0.8)
        rotation += self.checkSensor(self.sensor_left, -0.6)
        rotation += self.checkSensor(self.sensor_right, 0.6)
        return rotation
            
    def move(self):
        rotation = self.checkSensors()
        
        # If no rotation suggested, random walk
        if rotation == 0:
            rotation = 0.05 * np.random.randn()
        
        # print("ROTATING BY:", rotation)
        robot.direction.rotate(rotation)

        # print("MOVING", self.direction.x, self.direction.y)
        
        self.x += self.direction.x * speed
        self.y += self.direction.y * speed



class Obstacles:
    def __init__(self, plot_size):
        self.coords = set()
        self.obstacles = [[(55, 55), (55, 65), (65, 65), (65, 55)], 
                          [(10, 80), (20, 80), (20, 40)],
                          [(55, 15), (55, 25), (80, 25), (80, 15)], 
                          ]
        
        self.obstacles = [ [(10, 10), (10, 45), (45, 45), (45, 10)],
                          [(55, 55), (55, 90), (90, 90), (90, 55)],
                          [(10, 55), (10, 90), (45, 90), (45, 55)],
                          [(55, 10), (55, 45), (90, 45), (90, 10)]
                          ]
        
        self.addOuterWalls(plot_size)
        
        for obstacle in self.obstacles:
            self.addObstacle(obstacle)
            
    def addOuterWalls(self, plot_size):
        left = tuple((0, y) for y in range(plot_size+1))
        right = tuple((100, y) for y in range(plot_size+1))
        bottom = tuple((x, 0) for x in range(plot_size+1))
        top = tuple((x, 100) for x in range(plot_size+1))
        
        self.coords.update(left)
        self.coords.update(right)
        self.coords.update(bottom)
        self.coords.update(top)
    
    def addObstacle(self, obstacle):
        for i in range(len(obstacle)):
            if i != len(obstacle)-1:
                first = obstacle[i]
                second = obstacle[i+1]
                                
                xs, ys = interval_range(first, second)
                
                for x, y in zip(xs, ys):
                    self.coords.add((int(round(x)), int(round(y))))
        
        # Finally, join the last and first element to complete the obstacle
        first = obstacle[-1]
        second = obstacle[0]
        
        xs, ys = interval_range(first, second)
        
        for x, y in zip(xs, ys):
            self.coords.add((int(round(x)), int(round(y))))


def interval_range(first, second):
    n_intervals = int(max(abs(first[0] - second[0]), abs(first[1] - second[1])))
    
    if first[0] != second[0]:
        x_step = (second[0] - first[0])/n_intervals
    else:
        x_step = 0
        
    if (first[1] != second[1]):
        y_step = (second[1] - first[1])/n_intervals
    else:
        y_step = 0

    if x_step == 0:
        # Single value duplicated as many times as we need for ys
        xs = [first[0]] * max(1, n_intervals)
    else:
        xs = np.arange(start=first[0], stop=second[0], step=x_step)
        
    if y_step == 0:
        # Single value duplicated as many times as we need for xs 
        ys = [first[1]] * max(1, n_intervals)
    else:
        ys = np.arange(start=first[1], stop=second[1], step=y_step)

    return xs, ys


def display_obstacles():    
    for obstacle in obstacles.obstacles:        
        plt.plot([coord[0] for coord in obstacle] + [obstacle[0][0]], [coord[1] for coord in obstacle] + [obstacle[0][1]])

def display_sensors():
    plt.plot([robot.x, robot.x + (robot.sensor_centre.length * robot.direction.x)], 
             [robot.y, robot.y + (robot.sensor_centre.length * robot.direction.y)], 
             color='r')
    
    rotated_left_x, rotated_left_y = robot.direction.rotated(robot.sensor_mid_left.rotation)
    plt.plot([robot.x, robot.x + (robot.sensor_mid_left.length * rotated_left_x)], 
            [robot.y, robot.y + (robot.sensor_mid_left.length * rotated_left_y)], 
            color='r')
    
    rotated_right_x, rotated_right_y = robot.direction.rotated(robot.sensor_mid_right.rotation)
    plt.plot([robot.x, robot.x + (robot.sensor_mid_right.length * rotated_right_x)], 
            [robot.y, robot.y + (robot.sensor_mid_right.length * rotated_right_y)], 
            color='r')
    
    rotated_left_x, rotated_left_y = robot.direction.rotated(robot.sensor_left.rotation)
    plt.plot([robot.x, robot.x + (robot.sensor_left.length * rotated_left_x)], 
            [robot.y, robot.y + (robot.sensor_left.length * rotated_left_y)], 
            color='r')
    
    rotated_right_x, rotated_right_y = robot.direction.rotated(robot.sensor_right.rotation)
    plt.plot([robot.x, robot.x + (robot.sensor_right.length * rotated_right_x)], 
            [robot.y, robot.y + (robot.sensor_right.length * rotated_right_y)], 
            color='r')
    
# def display_sensors():
#     plt.plot([robot.x, robot.sensor_centre.end_point[0]], 
#              [robot.y, robot.sensor_centre.end_point[1]], 
#              color='r')
    
#     plt.plot([robot.x, robot.sensor_left.end_point[0]], 
#             [robot.y, robot.sensor_left.end_point[1]], 
#             color='r')
    
#     plt.plot([robot.x, robot.sensor_right.end_point[0]], 
#             [robot.y, robot.sensor_right.end_point[1]], 
#             color='r')


def animate(i):
    robot.move()

    plt.clf()
    
    display_obstacles()
    display_sensors()
    # Plot Robot
    plt.plot([robot.x], [robot.y], '.', color='b', markersize=robot.size)

    plt.xlim(0, plot_size)
    plt.ylim(0, plot_size)
    plt.gca().set_aspect('equal', adjustable='box')
    



speed = 1.5
plot_size = 100
robot = Robot(speed=speed, start_x=plot_size//2, start_y=plot_size//2)
robot = Robot(speed=speed, start_x=7, start_y=7)
obstacles = Obstacles(plot_size)

fig = plt.figure()

ani = animation.FuncAnimation(fig, animate, interval=1000) 

plt.show()