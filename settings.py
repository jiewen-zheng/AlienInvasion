class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""

        # 屏幕设置
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (150, 150, 230)

        # 飞船设置
        self.ship_speed = 0.6  # 飞船速度

        # 子弹设置
        self.bullet_speed = 0.5  # 子弹飞行速度
        self.bullet_width = 4
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)    # 子弹颜色
        self.bullet_fire_speed = 100 + \
            int(1.0 / self.bullet_speed)  # 自动开火速度，越小越快
        self.bullets_allowed = 10   # 屏幕允许存在子弹数量

    def get_ship_speed(self):
        return self.ship_speed
