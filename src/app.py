#
#
#


from src import *
from src.exceptions import GameOverException
from src.utils import *
from src.enums import Direction
from src.snake import Snake
from src.consumables import *



class App(object):
    
    def main(self) -> None:
        running = True
        animation_speed = 64
        while running:
            mouse_pos = pygame.mouse.get_pos()
            display.fill((0xe0, 0xbb, 0xe4))

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        quit()
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                running = False

                            case pygame.K_SPACE:
                                self.game()

            write("Press SPACE to start", (0xaa, 0x1b, 0x8c), (0, 0, display_width, display_height), int(120 + math.sin(pygame.time.get_ticks() / animation_speed)*16), centered=True)
            write("Snake alpha1.0", (0xaa, 0x1b, 0x8c), (16, 16), 32)

            color = (0xcc, 0x14, 0x51)
            if pygame.mouse.get_pressed()[0]:
                color = (0x14, 0xcc, 0x51)
            pygame.draw.circle(display, color, mouse_pos, 16, 0)


            clock.tick(144)
            pygame.display.update()

    def game(self) -> None:
        running = True
        snake = Snake([(10, 2), (10, 3)])
        fruit = Apple((random.randint(0, 16), random.randint(0, 32)))
        direction: Direction = Direction.EAST
        fruits = [Apple, Cherry, Ginger]
        snake_update_time = time.time()
        input_buffer = []
        while running:
            display.fill((0xe0, 0xbb, 0xe4))
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        quit()
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                running = False

                            # Capture movement inputs
                            case pygame.K_UP:
                                direction = Direction.NORTH
                            case pygame.K_RIGHT:
                                direction = Direction.EAST
                            case pygame.K_DOWN:
                                direction = Direction.SOUTH
                            case pygame.K_LEFT:
                                direction = Direction.WEST

            # Make sure to capture all inputs in between snake updates using a buffer
            if len(input_buffer) > 0:
                if input_buffer[-1] != direction:
                    input_buffer.append(direction)
            else:
                input_buffer.append(direction)


            # Drawing grid
            for row in range(19):
                for column in range(32):
                    pygame.draw.rect(display, 0x000000, (100 + column*32, 100 + row*32, 32, 32), 1)


            # Chek if fruit is still alive and replace otherwise
            if not fruit.is_alive:
                fruit = random.choice(fruits)((random.randint(0, 18), random.randint(0, 31)))


            # Update snake movement based on direction inputs
            if time.time() - snake_update_time >= .1:
                snake.update(input_buffer[0])
                snake_update_time = time.time()
                del input_buffer[0]

                # Check if snake hit obstacle
                for part in snake.parts[:-1]:
                    if part == snake.parts[-1]:
                        running = False


            # Check if snake ate fruit
            if fruit.pos == snake.parts[-1]:
                snake.eat(fruit)
                fruit = random.choice(fruits)((random.randint(0, 18), random.randint(0, 31)))

            fruit.update()

            snake.draw()
            fruit.draw()


            clock.tick(144)
            pygame.display.update()

