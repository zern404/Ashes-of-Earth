import pygame 
import sys 


WIDH, HEIGH = 1000, 800


class Player:
    def __init__(self, frame, x=WIDH/2, y=HEIGH/2):
        self.x = x
        self.y = y

        self.frame = frame
        
        self.speed = 10
        self.size_player = 30
        self.color = (255, 255, 255)

    def handle_keyboard(self):
        kb = pygame.key.get_pressed()
        if kb[pygame.K_w]:
            self.y -= self.speed
            self.color = (155, 155, 255)
        elif kb[pygame.K_s]:
            self.y += self.speed
            self.color = (155, 155, 255)
        elif kb[pygame.K_d]:
            self.x += self.speed
            self.color = (155, 155, 255)
        elif kb[pygame.K_a]:
            self.x -= self.speed
            self.color = (155, 155, 255)
        else:
            self.color = (255, 255, 255)
    
    def draw_player(self):
        pygame.draw.circle(self.frame, self.color, (int(self.x), int(self.y)), self.size_player)

class Game:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        pygame.display.set_caption("Game")

        self.width = WIDH
        self.height = HEIGH

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.running = True
        self.end_game = False

        self.player = Player(self.screen)

    def handle_player(self, player):
        player.handle_keyboard()
        player.draw_player()

    def main(self):
        while self.running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        sys.exit()
                self.screen.fill((20, 20, 20))

                self.handle_player(self.player)

                pygame.display.flip()
                self.clock.tick(60)
            except Exception as e:
                print(f"Error in main cycle: {e}")


if __name__ == "__main__":
    Game().main()