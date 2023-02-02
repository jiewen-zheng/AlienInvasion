import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        # 窗口模式
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # 全屏设置
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # 设置窗口标题
        pygame.display.set_caption("Alien Invasion")

        # 创建飞船
        self.ship = Ship(self)

        # 创建子弹编组
        self.bullets = pygame.sprite.Group()
        self.fire_speed = 0
        self.auto_fire = False

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_event()
            self.ship.update()
            self._update_bullet()
            self._update_screen()

    def _check_event(self):
        """监视键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键按下"""
        if event.key == pygame.K_RIGHT:
            # 飞船向右移动
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 飞船向左移动
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            # 飞船向左移动
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            # 飞船向左移动
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_a:
            if self.auto_fire:
                self.auto_fire = False
            else:
                self.auto_fire = True

    def _check_keyup_events(self, event):
        """响应按键松开"""
        if event.key == pygame.K_RIGHT:
            # 飞船向右移动
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # 飞船向左移动
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            # 飞船向左移动
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            # 飞船向左移动
            self.ship.moving_down = False

    def _fire_bullet(self):
        """创建一颗子弹,并将其加入编组bullets中"""
        if self.auto_fire == True and self.fire_speed > 0:
            self.fire_speed -= 1
        elif len(self.bullets) < self.settings.bullets_allowed:  # 限制屏幕中出现的子弹数量
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.fire_speed = self.settings.bullet_fire_speed   # 装填开火间隔

    def _update_bullet(self):
        """更新子弹的位置, 删除消失的子弹"""
        # 更新子弹位置
        self.bullets.update()

        # 自动开火
        if self.auto_fire:
            self._fire_bullet()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""

        self.screen.fill(self.settings.bg_color)
        # 更新飞船像素位置
        self.ship.blitme()

        # 更新子弹像素位置
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
