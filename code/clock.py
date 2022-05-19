import pygame

class Countdown:
    def __init__(self,cooldown):
        self.__start = pygame.time.get_ticks()
        self.__cooldown = cooldown
        self.__stop = False
    @property
    def elapsed_time(self):
        if self.__stop == False:
            time = (self.__cooldown - (pygame.time.get_ticks() - self.__start)/1000)
            self.__stop = time <= 0
            return max(time, 0)
        else:
            return 0

    @property
    def is_done(self) -> bool:
        return self.elapsed_time == 0

    def reset(self):
        self.__start = pygame.time.get_ticks()
        self.__stop = False