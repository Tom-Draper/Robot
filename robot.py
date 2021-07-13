import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Sensor:
    def __init__(self, length):
        self.length = length


class Robot:
    def __init__(self, plot_size):
        self.x = plot_size//2
        self.y = plot_size//2
        
        self.direction = 90  # Upwards
        
        self.sensor_left = Sensor(10)
        self.sensor_centre = Sensor(10)
        self.sensor_right = Sensor(10)
        
    def move(self, vector):
        self.x += vector.x
        self.y += vector.y
    
    def calcNextMove(self):
        return Vector(1, 0)



class Obstacles:
    def __init__(self, plot_size):
        self.coords = set()
        self.obstacles = [[(60, 60), (60, 70), (70, 70), (70, 60)]]
        
        self.addOuterWalls(plot_size)
        
        for obstacle in self.obstacles:
            self.addObstacle(obstacle)
    
    def addOuterWalls(self, plot_size):
        left = ((0, y) for y in range(plot_size+1))
        right = ((100, y) for y in range(plot_size+1))
        bottom = ((x, 0) for x in range(plot_size+1))
        top = ((x, 100) for x in range(plot_size+1))
        
        self.coords.add(left)
        self.coords.add(right)
        self.coords.add(bottom)
        self.coords.add(top)
    
    def addObstacle(self, obstacle):
        for i in range(len(obstacle)):
            if i != len(obstacle)-1:
                first = obstacle[i]
                second = obstacle[i+1]
                
                step = max(abs(first[0] - second[0]), abs(first[1] - second[1]))
                xs = np.arange(start=first[0], stop=second[0], step=step)
                ys = np.arange(start=first[1], stop=second[1], step=step)
                
                for x, y in zip(xs, ys):
                    self.coords.add((x, y))
        
        # Finally, join the last and first element to complete the obstacle
        first = obstacle[-1]
        second = obstacle[0]
        
        step = max(abs(first[0] - second[0]), abs(first[1] - second[1]))
        xs = np.arange(start=first[0], stop=second[0], step=step)
        ys = np.arange(start=first[1], stop=second[1], step=step)
        
        for x, y in zip(xs, ys):
            self.coords.add((x, y))
                    

def display_obstacles():
    # Plot outer walls    
    plt.plot([0, 0], [0, 100], color='g')
    plt.plot([0, 0], [100, 0], color='g')
    plt.plot([100, 0], [100, 100], color='g')
    plt.plot([0, 100], [100, 100], color='g')
    
    for obstacle in obstacles.obstacles:        
        plt.plot([coord[0] for coord in obstacle] + [obstacle[0][0]], [coord[1] for coord in obstacle] + [obstacle[0][1]])
        


def animate(i):
    plt.clf()
    
    # Plot Robot
    plt.plot([robot.x], [robot.y], '.', color='b', markersize=6)
    
    display_obstacles()

    plt.xlim(0, plot_size)
    plt.ylim(0, plot_size)
    
    move_vector = robot.calcNextMove()
    robot.move(move_vector)


plot_size = 100
robot = Robot(plot_size)
obstacles = Obstacles(plot_size)

fig = plt.figure()

ani = animation.FuncAnimation(fig, animate, interval=1000) 
plt.show()