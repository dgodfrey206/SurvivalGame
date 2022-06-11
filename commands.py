import pygame
from settings import *

class Commands:
    def __init__(self) -> None:
        self.x = 0
        self.width = WIDTH
        self.height = 30
        self.y = HEIGHT - self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.t = "/"
        self.text = main_font.render(self.t, 1, BLACK)

    def draw(self, surf: pygame.Surface) -> None:
        # drawing rect into background
        pygame.draw.rect(surf, (150, 150, 150), self.rect)
        # drawing line as cursor
        pygame.draw.line(surf, BLACK, (self.x + self.text.get_width() + 5, HEIGHT - self.height + 2), (self.x + self.text.get_width() + 5, HEIGHT - 2))
        # blitting text onto the rect
        surf.blit(self.text, (5, self.y + self.height / 2 - self.text.get_height() / 2))
    def update(self) -> None:
        """
        updating variables
        """
        self.text = main_font.render(self.t, 1, BLACK)
        
    def append_letter(self, letter: str) -> None:
        """
        append letter to current text
        """
        self.t += letter
    
    def remove_letter(self) -> None:
        """
        remove last latter from current text
        """
        if len(self.t) > 1:
            self.t = self.t[:-1]

    def r_input(self) -> str:
        """
        returning the text
        setting it back to None
            > done after hitting enter to execute command
        """
        t = self.t
        self.t = "/"
        return t
    
    def make_action(self):
        pass