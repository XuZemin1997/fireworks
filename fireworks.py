import tkinter as tk
from PIL import Image, ImageTk
from time import time, sleep
from random import choice, uniform, randint
from math import sin, cos, radians

# 模拟重力
GRAVITY = 0.1

# 颜色选项
# colors = ['red', 'blue', 'yellow', 'green', 'purple', 'orange', 'seagreen']
colors = ['red', 'blue', 'yellow', 'white', 'green', 'orange', 'purple', 'seagreen', 'indigo', 'cornflowerblue']

'''
particle类
粒子在空中随机生成，变成一个圈、下坠、消失
属性：
- id: 粒子的id
- x, y: 粒子的坐标
- vx, vy: 在坐标方向的变化速度
- total: 总数
- age: 粒子存在时长
- color: 粒子颜色
- cv: 画布
- lifespan: 最高存在时长
'''


class Particle:
    def __init__(self, cv, idx, total, explosion_speed, x=0., y=0., vx=0., vy=0., size=1.5, color='red', lifespan=2,
                 **kwargs):
        self.id = idx
        self.x = x
        self.y = y
        self.initial_speed = explosion_speed
        self.vx = vx
        self.vy = vy
        self.total = total
        self.age = 0
        self.color = color
        self.cv = cv
        self.cid = self.cv.create_oval(
            x - size, y - size, x + size, y + size,
            fill=self.color)
        self.lifespan = lifespan

    def update(self, dt):
        self.age += dt

        # 粒子范围扩大
        if self.alive() and self.expand():
            move_x = cos(radians(self.id * 360 / self.total)) * self.initial_speed
            move_y = sin(radians(self.id * 360 / self.total)) * self.initial_speed
            self.cv.move(self.cid, move_x, move_y)
            self.vx = move_x / (float(dt) * 1000)

        # 以自由落体坠落
        elif self.alive():
            move_x = cos(radians(self.id * 360 / self.total))
            self.cv.move(self.cid, self.vx + move_x, self.vy + GRAVITY * dt)
            self.vy += GRAVITY * dt

        # 移除超过最高时长的粒子
        elif self.cid is not None:
            cv.delete(self.cid)
            self.cid = None

    # 粒子是否处于扩散状态
    def expand(self):
        return self.age <= 1.2

    # 粒子是否存活
    def alive(self):
        return self.age <= self.lifespan


# 循环调用保持不停
def simulate(cv):
    t = time()
    explode_points = []         # 用于保存同时绽放的烟花的数组
    wait_time = randint(5, 80)          # 下一轮烟花绽放的等待时间
    numb_explode = randint(10, 15)          # 同时绽放的烟花数量

    # 创建一个所有粒子同时扩大的二维列表
    for point in range(numb_explode):
        objects = []
        x_cordi = randint(50, 1100)          # 绽放烟花所处的x坐标
        y_cordi = randint(50, 200)           # 绽放烟花所处的y坐标
        speed = uniform(0.5, 1.5)            # 粒子扩散速度
        size = uniform(0.5, 3)               # 粒子半径大小
        # color = choice(colors)               # 粒子颜色
        explosion_speed = uniform(0.2, 1)       # 粒子扩散速度
        total_particles = randint(15, 60)       # 一个烟花含有的粒子数量
        for i in range(1, total_particles):
            color = choice(colors)  # 粒子颜色
            r = Particle(cv, idx=i, total=total_particles, explosion_speed=explosion_speed, x=x_cordi, y=y_cordi,
                         vx=speed, vy=speed, size=size, color=color, lifespan=uniform(0.6, 1.75))
            objects.append(r)
        explode_points.append(objects)

    total_time = .0
    # 1.8s内一直扩大
    while total_time < 1.8:
        sleep(0.01)
        tnew = time()
        t, dt = tnew, tnew - t
        for point in explode_points:
            for item in point:
                item.update(dt)
        cv.update()
        total_time += dt
    # 循环调用
    root.after(wait_time, simulate, cv)

def close(*ignore):
    # 退出程序关闭窗口
    global root
    root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("烟花绽放效果")
    cv = tk.Canvas(root, height=600, width=1200)

    # 绘制一个黑色背景
    cv.create_rectangle(0, 0, 1200, 800, fill='black')

    # image = Image.open("./常州落日.jpg")
    # photo = ImageTk.PhotoImage(image)
    # cv.create_image(0, 0, image=photo, anchor='nw')
    cv.pack()
    root.protocol("WM_DELETE_WINDOW", close)
    root.after(100, simulate, cv)
    root.mainloop()
