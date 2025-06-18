import pygame 
import sys 


WIDTH, HEIGHT = 1000, 800
WORLD_W = 3000
WORLD_H = 2000

class Player:
    def __init__(self, frame, world, x=WIDTH/2, y=HEIGHT/2):
        self.x = x
        self.y = y

        self.frame = frame
        self.world = world
        
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
    
    def camera_offset(self):
        camera_x = self.x - WIDTH // 2
        camera_y = self.y - HEIGHT // 2

        camera_x = max(0, min(camera_x, WORLD_W - WIDTH))
        camera_y = max(0, min(camera_y, WORLD_H - HEIGHT))

        return camera_x, camera_y


    def draw_player(self, offset):
        screen_pos = (int(self.x - offset[0]), int(self.y - offset[1]))
        pygame.draw.circle(self.world, self.color, screen_pos, self.size_player)

class Game:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        pygame.display.set_caption("Game")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
        self.end_game = False

        self.world = pygame.Surface((WORLD_W, WORLD_H))
        self.player = Player(self.screen, self.world)

    def handle_world(self):
        offset = self.player.camera_offset()
        self.screen.blit(self.world, (0, 0), area=pygame.Rect(offset[0], offset[1], WIDTH, HEIGHT))
        
        return offset

    def handle_player(self, offset):
        self.player.handle_keyboard()
        self.player.draw_player(offset)

    def main(self):
        while self.running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        sys.exit()

                self.world.fill((20, 20, 20))
                offset = self.player.camera_offset()

                self.handle_player(offset)  
            except Exception as e:
                print(f"Error in main cycle: {e}")
            finally:
                self.screen.blit(self.world, (0, 0), area=pygame.Rect(offset[0], offset[1], WIDTH, HEIGHT))
                pygame.display.flip()
                self.clock.tick(60)

if __name__ == "__main__":
    Game().main()