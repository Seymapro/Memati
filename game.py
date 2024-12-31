import pygame
import random

class Oyun:
    def __init__(self):
        pygame.init()

        self.window_width = 1020
        self.window_height = 820
        
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Catch Coins, Avoid Monsters")

        self.robot = pygame.image.load("mamos.webp")
        self.coin = pygame.image.load("mama.webp")
        self.monster = pygame.image.load("gavad.webp")
        
        self.to_left = False
        self.to_right = False

        self.robot = pygame.transform.scale(self.robot, (100, 100))
        self.coin = pygame.transform.scale(self.coin, (60, 40))
        self.monster = pygame.transform.scale(self.monster, (100, 100))

        self.robot_x = self.window_width // 2
        self.robot_y = self.window_height - 80
        self.robot_speed = 12

        self.coins = [] 
        self.monsters = []  
        self.score = 0
        self.game_over = False
        self.font = pygame.font.SysFont("Arial", 24)

        self.clock = pygame.time.Clock()
        self.main_loop()

    def spawn_coin(self):
        x = random.randint(0, self.window_width - 30)
        self.coins.append([x, 0])

    def spawn_monster(self):
        x = random.randint(0, self.window_width - 30)
        self.monsters.append([x, 0])

    def main_loop(self):
        while True:
            self.check_events()
            if not self.game_over:
                self.update_game()
            self.draw_window()
            self.clock.tick(45)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_r and self.game_over: 
                    self.restart_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False

    def update_game(self):
        if self.to_left:
            self.robot_x -= self.robot_speed
        if self.to_right:
            self.robot_x += self.robot_speed

        self.robot_x = max(10, min(self.robot_x, self.window_width - 100))

        if random.randint(1, 20) == 1:
            self.spawn_coin()
        if random.randint(1, 40) == 1:
            self.spawn_monster()
        for coin in self.coins:
            coin[1] += 5 
        for monster in self.monsters:
            monster[1] += 7

        self.coins = [coin for coin in self.coins if not self.check_collision(coin, "coin")]
        self.monsters = [monster for monster in self.monsters if not self.check_collision(monster, "monster")]

        self.coins = [coin for coin in self.coins if coin[1] < self.window_height]
        self.monsters = [monster for monster in self.monsters if monster[1] < self.window_height]

    def check_collision(self, obj, obj_type):
        obj_x, obj_y = obj
        robot_rect = pygame.Rect(self.robot_x, self.robot_y,100,100)
        obj_rect = pygame.Rect(obj_x, obj_y, 60, 40)

        if robot_rect.colliderect(obj_rect):
            if obj_type == "coin":
                self.score += 1
            elif obj_type == "monster":
                self.game_over = True
            return True
        return False

    def draw_window(self):
        self.window.fill((0, 0, 0))

        self.window.blit(self.robot, (self.robot_x, self.robot_y))

        for coin in self.coins:
            self.window.blit(self.coin, (coin[0], coin[1]))

        for monster in self.monsters:
            self.window.blit(self.monster, (monster[0], monster[1]))

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.window.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render("Game Over! Press R to Restart", True, (255, 0, 0))
            self.window.blit(game_over_text, (self.window_width // 2 - game_over_text.get_width() // 2,
                                              self.window_height // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()

    def restart_game(self):
        self.coins = []
        self.monsters = []
        self.score = 0
        self.game_over = False
        self.robot_x = self.window_width // 2

if __name__ == "__main__":
    Oyun()