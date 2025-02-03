import matplotlib.pyplot as plt
import matplotlib.animation as animation
import keyboard
import numpy as np

# 初始化小车的位置
car_x, car_y = 0, 0
# 设置移动步长
step_size = 0.1

# 创建图形和子图
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)  # 设置x轴范围
ax.set_ylim(-10, 10)  # 设置y轴范围
ax.set_aspect('equal')  # 保持比例
ax.grid(True)  # 显示网格

# 创建一个小车（用一个点表示）
car, = ax.plot([car_x], [car_y], 'ro')  # 注意这里将car_x和car_y作为列表传递

def update(frame):
    global car_x, car_y
    # 检测键盘输入
    if keyboard.is_pressed('up'):
        car_y += step_size
    if keyboard.is_pressed('down'):
        car_y -= step_size
    if keyboard.is_pressed('left'):
        car_x -= step_size
    if keyboard.is_pressed('right'):
        car_x += step_size
    
    # 更新小车的位置
    car.set_data([car_x], [car_y])  # 注意这里将car_x和car_y作为列表传递
    return car,

# 创建动画
ani = animation.FuncAnimation(fig, update, interval=50, cache_frame_data=False)

# 显示图形
plt.show()