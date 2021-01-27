import asyncio as aio
from pygame.constants import QUIT
import simple_term_menu
import threading
import pygame
import sys

i = 0

def main(loop: aio.BaseEventLoop):
    # while True:
    #     cmd = input(">>> ")
    #     print(cmd)
    #     if cmd == 'play':
    #         choices = ['a', 'b']
    #         choice = choices[simple_term_menu.TerminalMenu(choices).show()]
    #         aio.run_coroutine_threadsafe(say_hello(choice), loop).result()
    pygame.init()
    screen = pygame.display.set_mode((500, 500))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Do all the drawings here
        screen.fill((i % 255, 255, 255))

        # Update the actual screen
        pygame.display.update()
            

async def say_hello(name):
    print('hello', name)
    await aio.sleep(1)
    print('how r u')



def worker(loop: aio.BaseEventLoop):
    async def worker_inner():
        global i
        i = 0
        while True:
            i += 1
            # print(i)
            await aio.sleep(0.005)
    
    aio.set_event_loop(loop)
    loop.run_until_complete(worker_inner())
    # aio.run(worker_inner(), debug=True)
    # pass


if __name__ == "__main__":
    loop = aio.new_event_loop()
    worker_thread = threading.Thread(target=worker, daemon=True, args=(loop,))
    worker_thread.start()
    main(loop)
    worker_thread.join()
