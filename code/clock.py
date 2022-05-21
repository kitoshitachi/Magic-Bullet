import pygame

class Countdown:
    def __init__(self,cooldown):
        '''
        this make a clock to check cooldown of status
        parameter cooldown: time to end status
        '''
        self.__start = pygame.time.get_ticks()
        self.__cooldown = cooldown
        self.__stop = False
    @property
    def elapsed_time(self):
        '''return elapse time between start and now'''
        if self.__stop == False:
            time = (self.__cooldown - (pygame.time.get_ticks() - self.__start)/1000)
            self.__stop = time <= 0
            return max(time, 0)
        else:
            return 0

    @property
    def is_done(self):
        '''return True if countdown back 0 else False'''
        return self.elapsed_time == 0

    def reset(self):
        '''reset countdown clock'''
        self.__start = pygame.time.get_ticks()
        self.__stop = False