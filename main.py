import pygame 
import sys 
import random
import time


WIDTH, HEIGHT = 1980, 1200
WORLD_W = 3000
WORLD_H = 2000

player_sprite_stay = pygame.image.load("assets/player/stay.png")
player_sprite_go = pygame.image.load("assets/player/go.png")

military_case_close = pygame.image.load("assets/chests/Chest_close.png")
military_case_open = pygame.image.load("assets/chests/militarycase2.png")

military_case_anim1 = pygame.image.load("assets/chests/militarycase3.png")
military_case_anim2 = pygame.image.load("assets/chests/militarycase4.png")
military_case_anim3 = pygame.image.load("assets/chests/militarycase5.png")

ak74 = pygame.image.load("assets/player/gun/ak74/ak74_1.png")

ak74_anim_1 = pygame.image.load("assets/player/gun/ak74/ak74_2.png")
ak74_anim_2 = pygame.image.load("assets/player/gun/ak74/ak74_3.png")
ak74_anim_3 = pygame.image.load("assets/player/gun/ak74/ak74_4.png")


class MilitaryCase(pygame.sprite.Sprite):
    def __init__(self, spawn_pos):
        super().__init__()
        self.spawn_pos = spawn_pos
        self.size = (175, 175)

        self.case_open = pygame.transform.scale(military_case_open, (self.size))
        self.case_close = pygame.transform.scale(military_case_close, (self.size))

        self.case_frames = [pygame.transform.scale(military_case_anim1, (self.size)), pygame.transform.scale(military_case_anim2, (self.size)), pygame.transform.scale(military_case_anim3, (self.size)), pygame.transform.scale(military_case_anim1, (self.size))]
        self.image = self.case_close
        self.rect = self.case_close.get_rect(center=self.spawn_pos)

        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 10

        self.is_open = False
        self.loot = Ak74()

    def handle_click(self, player_pos) -> bool:
        if self.rect.collidepoint(player_pos) and not self.is_open:
            self.is_open = True
            self.anim_index = 0 
            self.anim_timer = 0
            return True
        return False

    def handle_open(self):
        if self.is_open:
            self.animate_case()

    def drop_loot(self):
        if self.loot:
            self.loot.rect = self.rect.copy()  
            Game.instance().dropped_items.append(self.loot)
            self.loot = None

    def animate_case(self):
        self.anim_timer += 1
        if self.anim_index < len(self.case_frames):
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.image = self.case_frames[self.anim_index]
                self.anim_index += 1
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = self.case_open  
            self.drop_loot()


class DefaultAkBullet:
    def __init__(self):
        self.__speed = 80
        self.damage = 30
        self.veight = 10,2


class Ak74(pygame.sprite.Sprite):
    def __init__(self):
        self.hp = 100
        self.veight = 180
        self.magazine = False
        self.fire_mode = True

        self.model_size = (500, 500)

        self.ak_frames = [pygame.transform.scale(ak74, self.model_size), pygame.transform.scale(ak74_anim_1, self.model_size), pygame.transform.scale(ak74_anim_2, self.model_size), pygame.transform.scale(ak74_anim_3, self.model_size)]
        self.image = self.ak_frames[0]
        self.rect = self.image.get_rect()
    
    def change_fire_mode(self, auto=False):
        if auto == False:
            self.fire_mode = False
        else:
            self.fire_mode = True

    def reload(self, magazine):
        pass

    def fire(self):
        pass


class Inventory:
    def __init__(self, player):
        self.player = player
        self.slots = 6
        self.items = []

        self.slot_size = 80  
        self.padding = 10    

    def get_items(self):
        if self.items != None:
            return self.items
        return False

    def add_item(self, item) -> bool:
        if len(self.items) != 6:
            self.items.append(item)
            return True

    def remove_item(self, item):
        if self.items != None:
            self.items.remove(item)


class Player(pygame.sprite.Sprite):
    def __init__(self, frame, world, x=WIDTH/2, y=HEIGHT/2):
        super().__init__()
        self.frame = frame
        self.world = world

        self.speed = 5
        self.veight = 80
        self.size_player = (125, 125)

        self.inventory = Inventory(self)

        self.moved = False
        self.run_audio_status = False
        self.run_audio = pygame.mixer.Sound("assets/audio/run.mp3")

        self.players_frames = [pygame.transform.scale(player_sprite_stay, self.size_player), pygame.transform.scale(player_sprite_go, self.size_player)]
        self.image = self.players_frames[0]

        self.rect = self.image.get_rect(center=(x, y))

        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 10

    def handle_mouse_controller(self):
        pass

    def handle_hud(self):
        pass
    
    def handle_kb_controller(self):
        kb = pygame.key.get_pressed()
        self.moved = False

        if kb[pygame.K_w]:
            self.rect.y -= self.speed
            self.moved = True
        elif kb[pygame.K_s]:
            self.rect.y += self.speed
            self.moved = True
        elif kb[pygame.K_d]:
            self.rect.x += self.speed
            self.moved = True
        elif kb[pygame.K_a]:
            self.rect.x -= self.speed
            self.moved = True

    def move_animate_player(self):
        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(self.players_frames)
        self.image = self.players_frames[self.anim_index]
        
    def handle_moving(self, sound=False):
        if self.moved:
            if sound:
                if not getattr(self, 'run_audio_status', False):
                    self.run_audio.play(-1)  
                    self.run_audio_status = True
            self.move_animate_player()
        else:
            if sound:
                if getattr(self, 'run_audio_status', False):
                    self.run_audio.stop()
                    self.run_audio_status = False
            self.image = self.players_frames[0]


class Game:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        pygame.display.set_caption("Game")

        Game._instance = self

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
        self.end_game = False

        self.world = pygame.Surface((WORLD_W, WORLD_H))

        self.player = Player(self.screen, self.world)
        self.player_sprites = pygame.sprite.Group(self.player)

        self.dropped_items = []

        self.case_sprites = None
        self.items = []
        
        self.generate_case()
    
    @staticmethod
    def instance():
        return Game._instance
    
    def handle_pickups(self):
        for item in self.dropped_items:
            if hasattr(item, 'rect') and hasattr(item, 'image'):
                self.screen.blit(item.image, item.rect)

    def handle_case(self):
        for case in self.items:
            case.handle_open()
        self.case_sprites.draw(self.screen)

    def generate_case(self):
        for i in range(10):
            self.items.append(MilitaryCase((random.randint(100, WIDTH), random.randint(100, HEIGHT))))
        self.case_sprites = pygame.sprite.Group(self.items)

    def handle_player(self, debug=False):
        self.player.handle_kb_controller()
        self.player.handle_moving(True)
        self.player_sprites.draw(self.screen)
        self.player.handle_hud()
        if debug:
            pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect, 2)

    def main(self):
        while self.running:
            try:
                self.screen.fill((20, 20, 20))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                        for case in self.items:
                            click = case.handle_click((self.player.rect.x, self.player.rect.y))
                            if click:
                                break
                        for item in self.dropped_items[:]:
                            if self.player.rect.colliderect(item.rect):
                                if self.player.inventory.add_item(item):
                                    self.dropped_items.remove(item)

                self.handle_case()
                self.handle_pickups()
                self.handle_player()  
            except Exception as e:
                print(f"Error in main cycle: {e}")
            finally:
                pygame.display.flip()
                self.clock.tick(60)


if __name__ == "__main__":
    Game().main()