import pygame 
import sys 


WIDH, HEIGH = 1000, 800


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
    
    def main(self):
        while self.running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        sys.exit()
            except Exception as e:
                print(f"Error in main cycle: {e}")


if __name__ == "__main__":
    Game().main()