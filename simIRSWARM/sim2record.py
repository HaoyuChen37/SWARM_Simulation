import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import keyboard

class BoidSimulation:
    def __init__(self):
        # 定义Boid类
        class Boid:
            def __init__(self, x, y, velocity):
                self.position = np.array([x, y])
                self.velocity = velocity

            def update(self, boids, separation_weight=0.5, alignment_weight=0.5, cohesion_weight=1.0):
                separation_force = np.array([0.0, 0.0])
                alignment_force = np.array([0.0, 0.0])
                cohesion_force = np.array([0.0, 0.0])
                neighbors = []

                # 计算邻居
                for boid in boids:
                    if boid != self:
                        distance = np.linalg.norm(self.position - boid.position)
                        if distance < 10:  # 邻居范围
                            neighbors.append(boid)

                # 计算分离力
                for boid in neighbors:
                    distance = np.linalg.norm(self.position - boid.position)
                    if distance < 5:  # 排斥距离
                        separation_force += (self.position - boid.position) / distance

                # 计算对齐力
                if neighbors:
                    avg_velocity = np.mean([boid.velocity for boid in neighbors], axis=0)
                    alignment_force = avg_velocity

                # 计算聚集力
                if neighbors:
                    avg_position = np.mean([boid.position for boid in neighbors], axis=0)
                    cohesion_force = avg_position - self.position

                # 应用力
                self.velocity += (
                    separation_force * separation_weight +
                    alignment_force * alignment_weight +
                    cohesion_force * cohesion_weight
                )

                # 限制速度
                speed = np.linalg.norm(self.velocity)
                if speed > 0.1:  # 最大速度限制
                    self.velocity = self.velocity / speed * 0.1

                # 更新位置
                self.position += self.velocity

        # 初始化小车
        self.num_boids = 5  # 一个手动控制的小车和四个自动跟随的小车
        self.boids = [
            Boid(np.random.uniform(-2, 2), np.random.uniform(-2, 2), np.random.uniform(-0.5, 0.5, 2)) for _ in range(self.num_boids)
        ]

        # 创建图形和子图
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        # 创建小车点
        self.boid_points = [self.ax.plot(boid.position[0], boid.position[1], 'ro')[0] for boid in self.boids]

    def update(self, frame):
        # 更新手动控制的小车位置
        if keyboard.is_pressed('up'):
            self.boids[0].position[1] += 0.1
        if keyboard.is_pressed('down'):
            self.boids[0].position[1] -= 0.1
        if keyboard.is_pressed('left'):
            self.boids[0].position[0] -= 0.1
        if keyboard.is_pressed('right'):
            self.boids[0].position[0] += 0.1

        # 更新自动跟随的小车位置
        for boid in self.boids[1:]:
            boid.update(self.boids)

        # 更新图形
        for boid, point in zip(self.boids, self.boid_points):
            point.set_data([boid.position[0]], [boid.position[1]])

        return self.boid_points

    def run(self):
        ani = animation.FuncAnimation(self.fig, self.update, frames=range(100), interval=50, blit=True)
        # 保存动画为GIF文件
        ani.save('boid_simulation.gif', writer='imagemagick', fps=10)
        plt.show()

# 运行仿真
simulation = BoidSimulation()
simulation.run()