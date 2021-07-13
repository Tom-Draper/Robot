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
    def __init__(self, length):
        self.length = length


class Robot:
    def __init__(self, plot_size):
        self.x = plot_size//2 + 5
        self.y = plot_size//2
        
        self.direction = Vector(0, 1)  # Upwards
        
        self.sensor_left = Sensor(10)
        self.sensor_centre = Sensor(10)
        self.sensor_right = Sensor(10)
        
        self.size = 6  # Display size
        
    def checkCentreSensor(self, obstacles):
        # Check central sensor
        first = (self.x, self.y)
        second = (self.x + (self.sensor_centre.length * self.direction.x), self.y + (self.sensor_centre.length * self.direction.y))
        
        xs, ys = interval_range(first, second)
                    
        for x, y in zip(xs, ys):
            print((int(round(x)), int(round(y))))
            if (int(round(x)), int(round(y))) in obstacles.coords:
                print("FOUND OBSTACLE")
                if random.randint(0, 1) == 0:
                    # Suggest rotate slightly left
                    return 0.7
                else:
                    # Suggest rotate slightly right
                    return -0.7
        for ob in obstacles.coords:
            print(ob)
                
        return 0
    
    def checkLeftSensor(self, obstacles):
        # Get direction vector of 90 degrees left
        rotated_left_x, rotated_left_y = robot.direction.rotated(1.57)

        first = (self.x, self.y)
        second = (self.x + (self.sensor_left.length * rotated_left_x), self.y + (self.sensor_left.length * rotated_left_y))
        
        xs, ys = interval_range(first, second)
            
        for x, y in zip(xs, ys):
            if (int(round(x)), int(round(y))) in obstacles.coords:
                print("FOUND OBSTACLE")
                # Suggest rotate sligtly right
                return -0.3

        return 0
            
    def checkRightSensor(self, obstacles):
        # Get direction vector of 90 degrees left
        rotated_right_x, rotated_right_y = robot.direction.rotated(-1.57)

        first = (self.x, self.y)
        second = (self.x + (self.sensor_left.length * rotated_right_x), self.y + (self.sensor_left.length * rotated_right_y))
        
        xs, ys = interval_range(first, second)
            
        for x, y in zip(xs, ys):
            if (int(round(x)), int(round(y))) in obstacles.coords:
                print("FOUND OBSTACLE")
                # Suggest rotate slightly left
                return 0.3
                        
        return 0
    
    def checkSensors(self, obstacles):
        rotation = 0
        rotation += self.checkCentreSensor(obstacles)
        rotation += self.checkLeftSensor(obstacles)
        rotation += self.checkRightSensor(obstacles)
        return rotation
            
    def move(self, obstacles):
        rotation = self.checkSensors(obstacles)
        
        # If no rotation suggested, random walk
        if rotation == 0:
            rotation = 0.05 * np.random.randn()
        
        print("ROTATING BY:", rotation)
        robot.direction.rotate(rotation)

        print("MOVING", self.direction.x, self.direction.y)
        
        self.x += self.direction.x
        self.y += self.direction.y



class Obstacles:
    def __init__(self, plot_size):
        self.coords = set()
        self.obstacles = [[(60, 60), (60, 70), (70, 70), (70, 60)], 
                          [(10, 25), (25, 25), (25, 10)]]
        
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
    n_intervals = max(abs(first[0] - second[0]), abs(first[1] - second[1]))
    
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
    
    rotated_left_x, rotated_left_y = robot.direction.rotated(1.57)
    plt.plot([robot.x, robot.x + (robot.sensor_left.length * rotated_left_x)], 
            [robot.y, robot.y + (robot.sensor_left.length * rotated_left_y)], 
            color='r')
    
    rotated_right_x, rotated_right_y = robot.direction.rotated(-1.57)
    plt.plot([robot.x, robot.x + (robot.sensor_right.length * rotated_right_x)], 
            [robot.y, robot.y + (robot.sensor_right.length * rotated_right_y)], 
            color='r')


def animate(i):
    plt.clf()
    
    # Plot Robot
    plt.plot([robot.x], [robot.y], '.', color='b', markersize=robot.size)
    
    display_obstacles()
    display_sensors()

    plt.xlim(0, plot_size)
    plt.ylim(0, plot_size)
    plt.gca().set_aspect('equal', adjustable='box')

    
    robot.move(obstacles)


plot_size = 100
robot = Robot(plot_size)
obstacles = Obstacles(plot_size)

fig = plt.figure()

ani = animation.FuncAnimation(fig, animate, interval=1000) 

plt.show()