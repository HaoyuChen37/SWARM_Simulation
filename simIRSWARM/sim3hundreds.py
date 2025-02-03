import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 参数设置
N = 50  # 代理的数量
width, height = 800, 600  # 群体活动空间的宽度和高度
max_speed = 5  # 代理的最大速度
max_force = 0.1  # 代理的最大转向力
perception_radius = 50  # 代理感知范围（影响范围）
repulsion_distance = 20  # 排斥作用的距离阈值
attraction_distance = 100  # 吸引作用的距离阈值
separation_coeff = 0.5  # 分离系数
alignment_coeff = 0.5  # 对齐系数
cohesion_coeff = 0.5  # 聚合系数

# 初始化代理
class Agent:
    def __init__(self, position, velocity):
        self.position = np.array(position)
        self.velocity = np.array(velocity)

    def update(self, force):
        self.velocity += force
        self.velocity = np.clip(self.velocity, -max_speed, max_speed)
        self.position += self.velocity

# 初始化群体
agents = [Agent([np.random.rand() * width, np.random.rand() * height], 
                [np.random.rand() * max_speed * 2 - max_speed, np.random.rand() * max_speed * 2 - max_speed]) 
          for _ in range(N)]

# 计算分离力
def separation(agent, neighbors):
    force = np.array([0.0, 0.0])
    count = 0
    for neighbor in neighbors:
        distance = np.linalg.norm(neighbor.position - agent.position)
        if 0 < distance < repulsion_distance:
            force -= (agent.position - neighbor.position) / distance
            count += 1
    if count > 0:
        force /= count
    return force

# 计算对齐力
def alignment(agent, neighbors):
    avg_velocity = np.array([0.0, 0.0])
    count = 0
    for neighbor in neighbors:
        distance = np.linalg.norm(neighbor.position - agent.position)
        if distance < perception_radius:
            avg_velocity += neighbor.velocity
            count += 1
    if count > 0:
        avg_velocity /= count
        avg_velocity = (avg_velocity / np.linalg.norm(avg_velocity)) * max_speed
        force = avg_velocity - agent.velocity
    else:
        force = np.array([0.0, 0.0])
    return force

# 计算聚合力
def cohesion(agent, neighbors):
    avg_position = np.array([0.0, 0.0])
    count = 0
    for neighbor in neighbors:
        distance = np.linalg.norm(neighbor.position - agent.position)
        if distance < perception_radius:
            avg_position += neighbor.position
            count += 1
    if count > 0:
        avg_position /= count
        force = avg_position - agent.position
        force = (force / np.linalg.norm(force)) * max_speed - agent.velocity
    else:
        force = np.array([0.0, 0.0])
    return force

# 更新函数
def update(frame):
    global agents
    ax.clear()
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_title("Swarm Model with Attraction/Repulsion Functions")

    for agent in agents:
        neighbors = [other for other in agents if other is not agent]
        sep_force = separation(agent, neighbors)
        ali_force = alignment(agent, neighbors)
        coh_force = cohesion(agent, neighbors)

        force = (sep_force * separation_coeff + ali_force * alignment_coeff + coh_force * cohesion_coeff)
        force = np.clip(force, -max_force, max_force)
        agent.update(force)

    # 绘制代理
    for agent in agents:
        ax.plot(agent.position[0], agent.position[1], 'bo', markersize=5)

# 设置绘图
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, frames=200, interval=50)

plt.show()