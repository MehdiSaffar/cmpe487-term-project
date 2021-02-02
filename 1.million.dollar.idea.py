
import pygame
import asyncio as aio
import package
import time
import functools as ft
import threading
import queue


class App:
    def __init__(self):
        self.init_pygame()
        # pass

    def init_pygame(self):
        pygame.init()
        pygame.mixer.init()  # For sound

        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Connect4")
        # self.is_running = True
    
    def render_loop(self):
        while True:
            time.sleep(1/60)
            self.screen.fill(self.color)
            pygame.display.update()
    
    def event_loop(self, loop: aio.AbstractEventLoop):
        i = 0
        while True:
            event = pygame.event.wait()
            i += 1
            i %= 255
            self.color = (i,) * 3
            aio.run_coroutine_threadsafe(self.handle_event(event), loop)
    
    async def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            print(event)

    
    def main(self):
        async def _main():
            # await aio.sleep(100)
            loop = aio.get_running_loop()
            self.event_thread = threading.Thread(target=self.event_loop, args=(loop,), daemon=True)
            self.event_thread.start()

            self.render_thread = threading.Thread(target=self.render_loop, daemon=True)
            self.render_thread.start()

        # aio.run(_main())
        l = aio.get_event_loop()
        l.create_task(_main())
        l.run_forever()


App().main()

