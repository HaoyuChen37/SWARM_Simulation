import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 小车类
class Car:
    def __init__(self, id, x, y, vx=0, vy=0):
        self.id = id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self, control_x, control_y, speed_limit=1.0):
        self.vx += control_x
        self.vy += control_y
        # 限制速度
        speed = np.sqrt(self.vx**2 + self.vy**2)
        if speed > speed_limit:
            self.vx = (self.vx / speed) * speed_limit
            self.vy = (self.vy / speed) * speed_limit
        self.x += self.vx
        self.y += self.vy

# 仿真环境类
class Simulation:
    def __init__(self, num_cars, set_dis):
        self.num_cars = num_cars
        self.set_dis = set_dis
        # 合理设置初始位置
        angles = np.linspace(0, 2 * np.pi, num_cars, endpoint=False)
        self.cars = [Car(i, set_dis * np.cos(angle), set_dis * np.sin(angle)) for i, angle in enumerate(angles)]
        self.fig, self.ax = plt.subplots()
        self.scats = [self.ax.scatter(car.x, car.y, label=f'Car {car.id}') for car in self.cars]
        self.ax.set_xlim(-20, 20)
        self.ax.set_ylim(-20, 20)
        self.ax.legend()

    def calculate_control(self, car):
        control_x = 0
        control_y = 0
        k = 0.01  # 调整比例系数
        for other_car in self.cars:
            if other_car.id != car.id:
                dx = other_car.x - car.x
                dy = other_car.y - car.y
                true_dis = np.sqrt(dx**2 + dy**2)
                r = np.array([dx, dy]) / true_dis if true_dis != 0 else np.array([0, 0])
                error = true_dis - self.set_dis
                control = k * error * r
                control_x += control[0]
                control_y += control[1]
        return control_x, control_y

    def update(self, frame):
        for car in self.cars:
            control_x, control_y = self.calculate_control(car)
            car.update(control_x, control_y)
        for scat, car in zip(self.scats, self.cars):
            scat.set_offsets([car.x, car.y])
        return self.scats

    def run(self):
        ani = animation.FuncAnimation(self.fig, self.update, frames=range(100), interval=50, blit=True)
        plt.show()

# 运行仿真
if __name__ == "__main__":
    sim = Simulation(num_cars=5, set_dis=2.0)
    sim.run()