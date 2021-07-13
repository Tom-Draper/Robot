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
    def __init__(self, robot, length=10, rotation=0):
        self.length = length
        self.rotation = rotation  # 0 for centre, 1.57 for left, -1.57 for right
        
        # Calculate sensor direction vector
        sensor_x, sensor_y = robot.direction.rotated(rotation)
        # Calculate initial ending point of this sensor using robot's initial position
        end_x = robot.x + (length * sensor_x)
        end_y = robot.y + (length * sensor_y)
        self.end_point = Vector(end_x, end_y)


class Robot:
    def __init__(self, speed=1, start_x=50, start_y=50, direction=None, display_size=10, colour='b', sensor_centre_size=10, sensor_mid_size=10, sensor_wide_size=10):
        self.speed = speed
        self.x = start_x
        self.y = start_y
        
        self.direction = Vector(0, 1)
        
        self.sensor_left = Sensor(self, sensor_wide_size, 1.5708)  # 90 degree left
        self.sensor_mid_left = Sensor(self, sensor_mid_size, 0.7853)  # 45 degree left
        self.sensor_centre = Sensor(self, sensor_centre_size, 0)
        self.sensor_mid_right = Sensor(self, sensor_mid_size, -0.7853)  # 45 degree right
        self.sensor_right = Sensor(self, sensor_wide_size, -1.5708)  # 90 degree right
        
        self.sensors = [self.sensor_left, self.sensor_mid_left, self.sensor_centre, self.sensor_mid_right, self.sensor_right]
        
        self.display_size = display_size  # Display size
        self.colour = colour
        
        # List to hold references to robot's graph components so they can be 
        # individually removed with each animation loop
        self.graph_components = []
    
    def checkSensor(self, sensor, max_robot_rotation, obstacles):
        # Get vector direction for this sensor
        sensor_x, sensor_y = self.direction.rotated(sensor.rotation)

        current_location = (self.x, self.y)
        sensor_end = (self.x + sensor.length * sensor_x, self.y + sensor.length * sensor_y)
                
        points = interval_range(current_location, sensor_end)
        
        sensor.end_point = Vector(sensor_end[0], sensor_end[1])
        for i, point in enumerate(points):
            if point in obstacles.coords:
                print("FOUND OBSTACLE")
                # Overwrite with the point where the sensor hits the obstacle
                sensor.end_point = Vector(point[0], point[1])
                # Suggest rotate right, harder rotate the closer the obstacle
                rotation = (max_robot_rotation / 2) + (max_robot_rotation / 2) * (1 - (i / len(points)))
                return rotation
            
        return 0
  
    def checkSensors(self, obstacles):
        # Sum all of the suggested rotations give by each sensor
        rotation = 0
        if random.randint(0, 1) == 0:
            rotation += self.checkSensor(self.sensor_centre, 1.2, obstacles)
        else:
            rotation += self.checkSensor(self.sensor_centre, -1.2, obstacles)
        rotation += self.checkSensor(self.sensor_mid_left, -0.85, obstacles)
        rotation += self.checkSensor(self.sensor_mid_right, 0.85, obstacles)
        rotation += self.checkSensor(self.sensor_left, -0.6, obstacles)
        rotation += self.checkSensor(self.sensor_right, 0.6, obstacles)
        return rotation
            
    def move(self, obstacles):
        # print("MOVING", self.direction.x, self.direction.y)
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed
        
        rotation = self.checkSensors(obstacles)
                
        # If no rotation suggested, random walk
        if rotation == 0:
            rotation = 0.08 * np.random.randn()
        
        # print("ROTATING BY:", rotation)
        self.direction.rotate(rotation)


class Obstacles:
    def __init__(self, plot_size):
        self.coords = set()
        self.obstacles = [[(55, 55), (55, 65), (65, 65), (65, 55)], 
                          [(10, 80), (20, 80), (20, 40)],
                          [(55, 15), (55, 25), (80, 25), (80, 15)], 
                          ]
        
        # self.obstacles = [ [(10, 10), (10, 45), (45, 45), (45, 10)],
        #                   [(55, 55), (55, 90), (90, 90), (90, 55)],
        #                   [(10, 55), (10, 90), (45, 90), (45, 55)],
        #                   [(55, 10), (55, 45), (90, 45), (90, 10)]
        #                   ]
        
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
                p1 = obstacle[i]
                p2 = obstacle[i+1]
                                
                points = interval_range(p1, p2)
                
                for point in points:
                    self.coords.add(point)
        
        # Finally, join the last and first point to complete the obstacle
        p1 = obstacle[-1]
        p2 = obstacle[0]
        
        points = interval_range(p1, p2)
        
        for point in points:
            self.coords.add(point)


def interval_range(p1, p2):
    """Create a list of the integer (x,y) points between two 2D points."""
    
    n_intervals = int(max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1])))
    
    if p1[0] != p2[0]:
        x_step = (p2[0] - p1[0])/n_intervals
    else:
        x_step = 0
        
    if (p1[1] != p2[1]):
        y_step = (p2[1] - p1[1])/n_intervals
    else:
        y_step = 0

    if x_step == 0:
        # Single value duplicated as many times as we need for ys
        xs = [p1[0]] * max(1, n_intervals)
    else:
        xs = np.arange(start=p1[0], stop=p2[0], step=x_step)
        
    if y_step == 0:
        # Single value duplicated as many times as we need for xs 
        ys = [p1[1]] * max(1, n_intervals)
    else:
        ys = np.arange(start=p1[1], stop=p2[1], step=y_step)
        
    # Round each value to the nearest integer
    xs = map(int, xs)
    ys = map(int, ys)
    
    points = list(zip(xs, ys))
    return points


def display_obstacles(obstacles):    
    for obstacle in obstacles.obstacles:        
        plt.plot([coord[0] for coord in obstacle] + [obstacle[0][0]], [coord[1] for coord in obstacle] + [obstacle[0][1]])
    
def display_sensors(robot):
    graph_components = []
    for sensor in robot.sensors:
        component, = plt.plot([robot.x, sensor.end_point.x], [robot.y, sensor.end_point.y], color='r')
        graph_components.append(component)

    return graph_components

def graph_robot(robot):
    robot.graph_components = display_sensors(robot)
    robot_plot, = plt.plot([robot.x], [robot.y], '.', color=robot.colour, markersize=robot.display_size)
    robot.graph_components.append(robot_plot)
    
def animate(i, robots, obstacles):
    for robot in robots:
        # Remove the previous robot plot
        for sensor in robot.graph_components:
            sensor.remove()
            
        robot.move(obstacles)
        
        graph_robot(robot)
        

def setup():
    plot_size = 100
    robot1 = Robot(start_x=plot_size//2, start_y=plot_size//2, colour='b')
    robot2 = Robot(start_x=20, start_y=20, colour='g')
    robots = [robot1, robot2]
    
    obstacles = Obstacles(plot_size)
    
    fig = plt.figure()

    # Set up
    display_obstacles(obstacles)
    plt.xlim(0, plot_size)
    plt.ylim(0, plot_size)
    plt.gca().set_aspect('equal', adjustable='box')
    
    for robot in robots:
        graph_robot(robot)
    
    return fig, robots, obstacles

if __name__ == "__main__":
    fig, robots, obstacles = setup()

    ani = animation.FuncAnimation(fig, animate, fargs=(robots, obstacles), interval=50) 

    plt.show()

