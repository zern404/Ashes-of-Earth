import pygame 
import sys 


WIDTH, HEIGHT = 1980, 1200
WORLD_W = 3000
WORLD_H = 2000

player_sprite_stay = pygame.image.load("assets/player/stay.png")
player_sprite_go = pygame.image.load("assets/player/go.png")

class Player:
    def __init__(self, frame, world, x=WIDTH/2, y=HEIGHT/2):
        self.x = x
        self.y = y
        self.frame = frame
        self.world = world

        self.speed = 5
        self.size_player = (125, 125)

        self.player_sprite_stay = pygame.transform.scale(player_sprite_stay, self.size_player)
        self.player_sprite_go = pygame.transform.scale(player_sprite_go, self.size_player)

        self.players_sprite = [self.player_sprite_stay, self.player_sprite_go]
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 10  

    def handle_controller(self):
        kb = pygame.key.get_pressed()
        moved = False

        if kb[pygame.K_w]:
            self.y -= self.speed
            moved = True
        elif kb[pygame.K_s]:
            self.y += self.speed
            moved = True
        elif kb[pygame.K_d]:
            self.x += self.speed
            moved = True
        elif kb[pygame.K_a]:
            self.x -= self.speed
            moved = True

        if moved:
            self.move_animate_player()
        else:
            self.frame.blit(self.player_sprite_stay, (int(self.x), int(self.y)))

    def move_animate_player(self):
        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(self.players_sprite)

        self.frame.blit(self.players_sprite[self.anim_index], (int(self.x), int(self.y)))

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

    def handle_player(self):
        self.player.handle_controller()

    def main(self):
        while self.running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        sys.exit()
                self.screen.fill((20, 20, 20))
                self.handle_player()  
            except Exception as e:
                print(f"Error in main cycle: {e}")
            finally:
                pygame.display.flip()
                self.clock.tick(60)

if __name__ == "__main__":
    Game().main()