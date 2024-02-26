import pygame
import sys
import random

import grabmen_db

pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((820, 400))
        WIDTH = 4
        self.heart_img = pygame.transform.scale(pygame.image.load("grabmen_img/heart.png"), (45, 35)).convert_alpha()
        self.galka_img = pygame.transform.scale(pygame.image.load("grabmen_img/galka.png"), (40, 20)).convert_alpha()
        self.name = 'user1'
        self.mouse_button_down = False

        # Stats

        self.hp = 3
        self.coins = 0
        self.circle_speed = 3

        # Circle

        self.free_in_left = True
        self.free_in_right = True
        self.free_in_down = True
        self.free_in_up = True

        self.can_move = True

        self.circle_rect = pygame.Rect(40, 40, 40, 40)
        self.circle_rect.center = (410, 200)

        self.skin = 1

        # Enemy

        self.enemy_rect = pygame.Rect(40, 40, 40, 40)
        self.enemy_rect.center = (50, 110)

        self.catch_timer = 0

        # Lines
        self.line_1 = pygame.Rect(0, 40, 820, WIDTH)
        self.line_2 = pygame.Rect(115, 40, WIDTH, 50)
        self.line_3 = pygame.Rect(0, 140, 200, WIDTH)
        self.line_4 = pygame.Rect(120, 210, WIDTH, 100)
        self.line_5 = pygame.Rect(350, 110, WIDTH, 120)
        self.line_6 = pygame.Rect(350, 350, WIDTH, 50)
        self.line_7 = pygame.Rect(200, 270, 90, WIDTH)
        self.line_8 = pygame.Rect(500, 180, WIDTH, 80)
        self.line_9 = pygame.Rect(580, 100, WIDTH, 60)
        self.line_10 = pygame.Rect(600, 320, WIDTH, 30)
        self.line_11 = pygame.Rect(750, 100, WIDTH, 60)
        self.line_12 = pygame.Rect(600, 250, 90, WIDTH)
        self.line_13 = pygame.Rect(650, 100, 100, WIDTH)

        self.red_lines = [self.line_3, self.line_1, self.line_2, self.line_7, self.line_12, self.line_11, self.line_13]
        self.blue_lines = [self.line_5, self.line_6, self.line_4, self.line_8, self.line_9, self.line_10]

        # Starts
        self.star_img = pygame.transform.scale(pygame.image.load("grabmen_img/star.png"), (40, 40)).convert_alpha()

        self.star1 = self.star_img.get_rect(topleft=(70, 255))
        self.star2 = self.star_img.get_rect(topleft=(120, 45))
        self.star3 = self.star_img.get_rect(topleft=(610, 255))
        self.star4 = self.star_img.get_rect(topleft=(770, 50))

        # self.stars_dict = {self.star1: 0, self.star2: 1, self.star3: 2, self.star4: 3}
        self.all_stars = [self.star1, self.star2, self.star3, self.star4]
        self.stars = [self.star1, self.star2, self.star3, self.star4]  # for show

        self.star_index = 0

        # Music

        self.death_sound = pygame.mixer.Sound('grabmen_img/death.wav')
        self.coin_sound = pygame.mixer.Sound('grabmen_img/Pickup_Coin.wav')
        self.red_wall_sound = pygame.mixer.Sound('grabmen_img/wall.wav')
        self.enemy_coin_sound = pygame.mixer.Sound('grabmen_img/enemy_coin.wav')
        self.catch = pygame.mixer.Sound('grabmen_img/catch.wav')

    def make_true_move(self):
        self.free_in_left = True
        self.free_in_right = True
        self.free_in_down = True
        self.free_in_up = True

    def enemy_move(self):
        x = self.enemy_rect.center[0]
        y = self.enemy_rect.center[1]

        enemy_speed = 2

        def right():
            self.enemy_rect.x += enemy_speed

        def up():
            self.enemy_rect.y -= enemy_speed

        def down():
            self.enemy_rect.y += enemy_speed

        def left():
            self.enemy_rect.x -= enemy_speed

        if x < 250 and y == 110:
            right()
        elif y > 70 and x == 250:
            up()
        elif x < 790 and y == 70:
            right()
        elif y < 350 and x == 790:
            down()
        elif x > 630 and y == 350:
            left()
        elif y > 280 and x == 630:
            up()
        elif x > 530 and y == 280:
            left()
        elif y > 130 and x == 530:
            up()
        elif x > 430 and y == 130:
            left()
        elif y < 260 and x == 430:
            down()
        elif x > 310 and y == 260:
            left()
        elif y < 340 and x == 310:
            down()
        elif x > 80 and y == 340:
            if x == 250 + enemy_speed:
                self.enemy_rect.x -= (enemy_speed * 2)
            left()
        elif y > 170 and x == 80:
            up()
        elif x < 250 and y == 170:
            right()
        elif y < 70 and x == 250:
            up()

    def leaderboard(self):
        def draw_skin(skin_id):
            skin = grabmen_db.get_skin_info(skin_id)
            skin1_rect = pygame.Rect(40, 40, 40, 40)
            if skin_id < 5:
                skin1_rect.center = (60, 120 + (skin_id - 1) * 60)
            else:
                skin1_rect.center = (270, 120 + (skin_id - 5) * 60)

            pygame.draw.circle(self.screen, skin['color1'], skin1_rect.center, 20, width=skin['width'])
            pygame.draw.circle(self.screen, skin['color2'], skin1_rect.center, 20 - skin['width'])


            # Galka/Cost
            if not grabmen_db.user_has_skin(self.name, skin_id):
                self.screen.blit(font_40.render(f"{skin['cost']}", True, '#f25757'),
                                 (skin1_rect.topright[0] + 20, skin1_rect.topright[1] - 3))
            else:
                self.screen.blit(self.galka_img, (skin1_rect.topright[0] + 20, skin1_rect.topright[1] + 10))

            # Border
            if self.skin == skin_id:
                pygame.draw.rect(self.screen, color='#f25757', rect=(skin1_rect.x - 5, skin1_rect.y - 5, 50, 50),
                                 width=2, border_radius=5)

            # Cursor
            pressed = pygame.mouse.get_pressed()[0]
            if skin1_rect.collidepoint(pygame.mouse.get_pos()) and pressed:
                if not grabmen_db.user_has_skin(self.name, skin_id):
                    grabmen_db.buy_skin(self.name, skin_id, skin['cost'])
                else:
                    self.skin = skin_id

        go_again = False
        font_40 = pygame.font.SysFont("arial", 40)
        font_30 = pygame.font.SysFont("arial", 30)
        font_25 = pygame.font.SysFont("arial", 25)
        while not go_again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        go_again = True

            leaders = grabmen_db.leaderboard()
            self.screen.fill('#fffff3')
            # Lines
            pygame.draw.line(self.screen, '#b1ddf1', (500, 0), (500, 400), 5)
            pygame.draw.line(self.screen, '#b1ddf1', (500, 270), (840, 270), 4)

            # Store
            balance = grabmen_db.balance(self.name)
            self.screen.blit(font_40.render(f"Магазин скинов", True, '#f25757'), (40, 10))
            self.screen.blit(font_25.render(f"{balance}", True, '#80ed99'), (350, 23))

            for i in range(1, 9):
                draw_skin(i)

            # Leaderboard
            self.screen.blit(font_40.render(f"Лучшие игроки", True, '#f25757'), (540, 10))

            self.screen.blit(font_30.render(f"{leaders[0][0]}", True, '#b1ddf1'), (540, 100))
            self.screen.blit(font_30.render(f"{leaders[0][1]}", True, '#b1ddf1'), (700, 100))

            self.screen.blit(font_30.render(f"{leaders[1][0]}", True, '#80ed99'), (540, 150))
            self.screen.blit(font_30.render(f"{leaders[1][1]}", True, '#80ed99'), (700, 150))

            self.screen.blit(font_30.render(f"{leaders[2][0]}", True, '#b1ddf1'), (540, 200))
            self.screen.blit(font_30.render(f"{leaders[2][1]}", True, '#b1ddf1'), (700, 200))

            # Results
            self.screen.blit(font_25.render(f"Результат", True, '#f25757'), (540, 280))
            self.screen.blit(font_25.render(f"Рекорд", True, '#f25757'), (700, 280))

            self.screen.blit(font_40.render(f"{self.coins}", True, '#80ed99'), (540, 317))
            self.screen.blit(font_40.render(f"{grabmen_db.best_score(self.name)[0][0]}", True, '#80ed99'), (700, 317))

            pygame.display.update()

    def draw_intro(self):
        font = pygame.font.SysFont('sans', 40)
        text_welcome = font.render(f"Enter your name", True, '#f12345')

        name3 = self.name

        is_find_name = False

        while not is_find_name:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        if name3 == self.name:
                            name3 = event.unicode
                        else:
                            name3 += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        name3 = name3[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(name3) >= 2:
                            grabmen_db.add_player(name3)
                            self.name = name3
                            is_find_name = True
                            break

            self.screen.fill('#FCFBF8')

            text_name = font.render(f"{name3}", True, '#f12345')
            rect_name = text_name.get_rect()
            rect_name.center = self.screen.get_rect().center

            self.screen.blit(text_welcome, (280, 35))
            self.screen.blit(text_name, rect_name)

            pygame.display.update()

    def run(self):
        """Main game method"""
        clock = pygame.time.Clock()

        pygame.font.init()
        font = pygame.font.SysFont("sans", 40)

        self.draw_intro()

        while True:

            clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_down = True

            self.screen.fill('#FCFBF8')

            self.can_move = True
            # Circle moves

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] and self.free_in_right:
                self.circle_rect.x += self.circle_speed
                self.make_true_move()

            if keys[pygame.K_LEFT] and self.free_in_left:
                self.circle_rect.x -= self.circle_speed
                self.make_true_move()

            if keys[pygame.K_UP] and self.free_in_up:
                self.circle_rect.y -= self.circle_speed
                self.make_true_move()

            if keys[pygame.K_DOWN] and self.free_in_down:
                self.circle_rect.y += self.circle_speed
                self.make_true_move()

            # Lines
            # Red
            for line in self.red_lines:
                pygame.draw.rect(self.screen, '#AD343E', line)

            # Blue
            for line in self.blue_lines:
                pygame.draw.rect(self.screen, '#80CED7', line)

            # Lines collisions
            for line in self.blue_lines:

                c = self.circle_rect.clipline(line.bottomleft, line.topleft)
                if c:
                    r = self.circle_rect.right
                    for i in range(r - 3, r + 3):
                        if i == c[0][0]:
                            self.free_in_right = False

                    l = self.circle_rect.left
                    for i in range(l - 3, l + 3):
                        if i == c[0][0]:
                            self.free_in_left = False

                    d = self.circle_rect.bottom
                    for i in range(d - 3, d + 3):
                        if i == c[0][1]:
                            self.free_in_down = False

                    u = self.circle_rect.top
                    for i in range(u - 3, u + 3):
                        if i == c[0][1]:
                            self.free_in_up = False

            for line in self.red_lines:
                if line.colliderect(self.circle_rect):
                    self.red_wall_sound.play()
                    self.hp -= 1
                    self.circle_rect.center = (410, 200)

            # Circle blit

            skin = grabmen_db.get_skin_info(self.skin)
            pygame.draw.circle(self.screen, skin['color1'], self.circle_rect.center, 20, width=skin['width'])
            pygame.draw.circle(self.screen, skin['color2'], self.circle_rect.center, 20 - skin['width'])

            x = 2
            for i in range(self.hp):
                self.screen.blit(self.heart_img, (x + 47 * i, 2))

            # Start
            for s in self.stars:
                self.screen.blit(self.star_img, s)
                if s.colliderect(self.circle_rect):
                    self.coin_sound.play()
                    self.coins += 1
                    ind = self.stars.index(s)
                    self.stars.pop(ind)

                if s.colliderect(self.enemy_rect):
                    self.enemy_coin_sound.play()
                    ind = self.stars.index(s)
                    self.stars.pop(ind)

            if len(self.stars) <= 2:
                if random.randint(0, 1):
                    for s in self.all_stars:
                        if s not in self.stars:
                            self.stars.append(s)

            if self.hp <= 0:
                grabmen_db.add_score(self.name, self.coins)
                self.death_sound.play()
                self.leaderboard()
                self.coins = 0
                self.hp = 3

            # Score

            self.screen.blit(font.render("Score:" + str(self.coins), True, '#AD343E'), (650, -5))

            # Enemy
            pygame.draw.circle(self.screen, '#f12345', self.enemy_rect.center, 20)

            self.enemy_move()

            for star in self.stars:
                if star.colliderect(self.enemy_rect):
                    self.enemy_coin_sound.play()
                    ind = self.stars.index(star)
                    self.stars.pop(ind)

            if self.circle_rect.colliderect(self.enemy_rect):
                self.catch.play()
                self.catch_timer = 300

            if self.catch_timer > 0:
                self.circle_speed = 1
                self.catch_timer -= 1
            else:
                self.circle_speed = 3

            pygame.display.update()


if __name__ == "__main__":
    Game().run()
