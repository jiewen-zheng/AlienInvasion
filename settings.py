class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""

        # 屏幕设置
        self.screen_width = 1024
        self.screen_height = 768
        self.bg_color = (150, 150, 230)

        # 飞船设置
        self.ship_speed = 0.8  # 飞船速度
        self.ship_limit = 4  # 飞船数量限制

        # 子弹设置
        self.bullet_speed = 1.2  # 子弹飞行速度
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (80, 80, 80)    # 子弹颜色
        self.bullet_fire_speed = 50 + \
            int(1.0 / self.bullet_speed)  # 自动开火速度，越小越快
        self.bullets_allowed = 10   # 屏幕允许存在子弹数量
        self.auto_fire = False  # 自动开火

        # 外星人设置
        self.alien_hp = 1  # 外星人生命值
        self.alien_speed = 1.0  # 外星人移动速度
        self.alien_drop_speed = 50  # 外星人碰墙后下落速度
        self.alien_direction = 1  # 外星人最初移动方向，为1表示向右移，为-1表示向左移。

    def get_ship_speed(self):
        return self.ship_speed
