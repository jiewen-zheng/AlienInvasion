import sys

from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        # 设置窗口标题
        pygame.display.set_caption("Alien Invasion")

        # 创建游戏设置实例
        self.settings = Settings()

        # 窗口模式
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # 全屏设置
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)

        # 创建计分板实例
        self.score = ScoreBoard(self)

        # 创建飞船
        self.ship = Ship(self)

        # 创建子弹编组
        self.bullets = pygame.sprite.Group()
        self.fire_speed = 0

        # 创建外星人编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # 创建Play按钮
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_event()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_alien()

            self._update_screen()

    def _ship_hit(self):
        """响应飞船被外星人撞到。"""
        self.stats.ship_hp -= 1
        if self.stats.ship_hp <= 0:
            self.stats.game_active = False

        # 刷新生命值
        self.score.prep_shipHps()
        # 清空余下的外星人和子弹。
        self.aliens.empty()
        self.bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端的中央
        self._create_fleet()
        self.ship.center_ship()

        # 暂停
        sleep(0.5)

    def _check_event(self):
        """监视键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mous_pos = pygame.mouse.get_pos()
                self._check_paly_button(mous_pos)

    def _check_paly_button(self, mous_pos):
        """在玩家单击Play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mous_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True

            self.score.prep_score()
            self.score.prep_level()
            self.score.prep_shipHps()

    def _check_keydown_events(self, event):
        """响应按键按下"""
        if event.key == pygame.K_p:
            # 暂停游戏
            self.stats.game_active = not self.stats.game_active
        elif event.key == pygame.K_RIGHT:
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
            if self.settings.auto_fire:
                self.settings.auto_fire = False
            else:
                self.settings.auto_fire = True

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
        if self.settings.auto_fire == True and self.fire_speed > 0:
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
        if self.settings.auto_fire:
            self._fire_bullet()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

        # 检测子弹和外星人碰撞
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞。"""
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, False)

        if collisions:
            # 处理一颗子弹碰到多个外星人的情况
            for aliens in collisions.values():
                for number in range(len(aliens)):
                    # 击中外星人时其生命值按子弹伤害减少
                    aliens[number].hp -= self.settings.bullet_harm
                    if aliens[number].hp <= 0:
                        # 删除hp为0的外星人
                        self.aliens.remove(aliens[number])
                        # 按外星人类型计算得分
                        self.stats.score += self.settings.alien_points * \
                            aliens[number].type
                        # 重新渲染得分
                        self.score.prep_score()

        if not self.aliens:
            # 射杀所有外星人后重新生成一批
            self._create_fleet()
            # 加快游戏速度
            self.settings.increase_speed()

            # 提高游戏等级
            self.stats.level += 1
            self.score.prep_level()

    def _create_alien(self, number_x, number_y):
        """创建一个外星人"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien.x + \
            (alien_width + alien_width / 2) * number_x
        alien.y = alien.y + \
            (alien_height + alien_height/2) * number_y
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        if alien.rect.right <= self.settings.screen_width:  # 防止外星人超出屏幕范围
            self.aliens.add(alien)

    def _create_fleet(self):
        """创建舰群"""
        # 获取屏幕一行容纳外星人数量
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_width / 2)
        number_alien_x = int(available_space_x /
                             (alien_width + alien_width / 2))

        # 计算外星人分布的y轴
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - \
            3 * alien_height - 5 * ship_height

        number_alien_y = int(available_space_y /
                             (alien_height + alien_height / 2))

        # 创建一行外星人
        for number_y in range(number_alien_y):
            for number_x in range(number_alien_x):
                self._create_alien(number_x, number_y)

    def _check_fleet_edges(self):
        """检查舰群中所有外星人边缘"""
        for alien in self.aliens.sprites():  # 从编组中获取一个列表
            if alien.check_edges():
                alien.y += self.settings.alien_drop_speed  # 向下移动
                alien.direction *= -1  # 改变方向

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理。
                self._ship_hit()
                break

    def _update_alien(self):
        """更新外星人位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self._ship_hit()

        self._check_aliens_bottom()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 填充背景
        self.screen.fill(self.settings.bg_color)
        # 更新飞船像素位置
        self.ship.blitme()

        # 更新子弹像素位置
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # 绘制外星人
        self.aliens.draw(self.screen)

        # 显示得分
        self.score.show_score()

        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
