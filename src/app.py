#
#
#



from src import *
from src.exceptions import GameOverException
from src.utils import *
from src.enums import Direction
from src.snake import Snake, DefaultSnake, PartInfo
from src.color import Color
from src.consumables import *



class App(object):
    
    def main(self) -> None:
        "App entry point, indicates game start by pressing SPACE, quit using ESC oder quit event(pressing x on top right corner)"
        running = True
        animation_speed = 64
        while running:
            mouse_pos = pygame.mouse.get_pos()
            display.fill(Color.BACKGROUND)

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        quit()
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                pygame.quit()
                                quit()

                            case pygame.K_SPACE:
                                self.game()

            write("Press SPACE to start", (0xaa, 0x1b, 0x8c), (0, 0, display_width, display_height), int(120 + math.sin(pygame.time.get_ticks() / animation_speed)*16), centered=True)
            write("Snake alpha1.0", (0xaa, 0x1b, 0x8c), (16, 16), 32)

            clock.tick(144)
            pygame.display.update()



    def game(self) -> None:
        running = True
        snake = DefaultSnake()
        direction: Direction = Direction.EAST
        fruit_types = [Apple, Cherry, Ginger]
        fruits = []
        fruit_spawn_delay = random.random() * 3
        fruit_spawn_time = time.time()

        snake_update_time = time.time()
        input_buffer = []
        try:
            while running:
                display.fill(Color.BACKGROUND)
                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    match event.type:
                        case pygame.QUIT:
                            pygame.quit()
                            quit()
                        case pygame.KEYDOWN:
                            direction = None
                            match event.key:
                                case pygame.K_ESCAPE:
                                    self.main()
                                
                                case pygame.K_SPACE:
                                    self.pause()
                                
                                case pygame.K_UP:
                                    direction = Direction.NORTH
                                case pygame.K_RIGHT:
                                    direction = Direction.EAST
                                case pygame.K_DOWN:
                                    direction = Direction.SOUTH
                                case pygame.K_LEFT:
                                    direction = Direction.WEST
                            
                            if direction and (len(input_buffer) < 1 or input_buffer[-1] != direction) and len(input_buffer) < 4:
                                input_buffer.append(direction)


                write(
                    f"Current score: {len(snake.parts)}", 
                    Color.WHITE, 
                    (GRID_POS[0]+GRID_SIZE[1]*CELL_SIZE[0], GRID_POS[1], display_width-GRID_POS[0]-GRID_SIZE[1]*CELL_SIZE[0], GRID_POS[1]), 
                    32, 
                    centered=True
                )
                self._draw_highscore(len(snake.parts))

                # Drawing grid
                pygame.draw.rect(display, Color.GRID, GRID_RECT, 0)
                for row in range(GRID_SIZE[0]):
                    for column in range(GRID_SIZE[1]):
                        cell_rect = (*translate_idx2pos((row, column), False), *CELL_SIZE)
                        pygame.draw.rect(display, Color.BLACK, cell_rect, 1)


                # Update snake movement based on direction inputs
                if time.time() - snake_update_time >= 1/SNAKE_SPEED:
                    if len(input_buffer) >= 1:
                        snake.direction = input_buffer[0]
                        del input_buffer[0]
                    snake.update()
                    snake_update_time = time.time()

                    # Check if snake hit obstacle
                    for part in snake.parts[:-1]:
                        if part.pos == snake.parts[-1].pos:
                            snake.draw()
                            pos = translate_idx2pos(snake.parts[-1].pos, centered=False)
                            display.blit(pygame.image.load("resources/explosion.png"), pos)
                            raise GameOverException(f"Snake ran into itself at {snake.parts[-1].pos}")
                

                if time.time() - fruit_spawn_time > fruit_spawn_delay and len(fruits) <= FRUITS_MAX:
                    fruit_spawn_time = time.time()
                    fruit_spawn_delay = 1 * random.random() * 3  # 1 <= DELAY <= 4
                    pos = (random.randint(0, GRID_SIZE[0] - 1), random.randint(0, GRID_SIZE[1] - 1))

                    # Make sure new consumable does not spawn inside snake/other consumables
                    while pos in [part.pos for part in snake.parts] or pos in [fruit.pos for fruit in fruits]:
                        pos = (random.randint(0, GRID_SIZE[0] - 1), random.randint(0, GRID_SIZE[1] - 1))
                    fruits.append(random.choice(fruit_types)(pos))
                    print(f"Spawning {str(fruits[-1])} at {pos}, spawn next consumable in {fruit_spawn_delay:.2f} seconds")

                # Check if snake ate fruit
                tmp = []
                for fruit in fruits:
                    fruit.update()
                    if not fruit.is_alive:
                        continue

                    tmp.append(fruit)

                    if fruit.pos == snake.parts[-1].pos:
                        snake.eat(fruit)
                        del tmp[-1]

                    fruit.draw()
                fruits = tmp 

                snake.draw()
                
                clock.tick(144)
                pygame.display.update()

        except GameOverException as gameover_exception:
            print(gameover_exception)
            if len(snake.parts) > self.highscores[-1]:
                self.highscores.append(len(snake.parts))
                self.highscores = sorted(self.highscores)[:0:-1]
            self._safe_highscores()
            self.gameover()
        
        except Exception as e:
            raise e
            self.main()
        
        finally:
            if self._load_highscores() != self.highscores:
                if len(snake.parts) > self.highscores[-1]:
                    self.highscores.append(len(snake.parts))
                    self.highscores = sorted(self.highscores)[:0:-1]
                self._safe_highscores()



    def gameover(self) -> None:
        "Called when game is over, offers restart using SPACE, navigate back to menu using ESC, draws last frame"
        running = True
        animation_speed = 64
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        quit()
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.main()

                            case pygame.K_SPACE:
                                self.game()
            
            pygame.draw.rect(display, Color.BACKGROUND, (0, 0, display_width, GRID_POS[1]), 0)
            write("GAME OVER", (0xaa, 0x1b, 0x8c), (0, 0, display_width, display_height//8), int(120 + math.sin(pygame.time.get_ticks() / animation_speed)*16), centered=True)

            clock.tick(144)
            pygame.display.update()



    def pause(self):
        "Just listen to inputs, draws last frame, continue on ESC, P"
        running = True
        animation_speed = 64
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        quit()
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.main()
                            case pygame.K_SPACE:
                                running = False
            
            pygame.draw.rect(display, Color.BACKGROUND, (0, 0, display_width, GRID_POS[1]), 0)
            write("Game paused, press SPACE to continue", (0xaa, 0x1b, 0x8c), (0, 0, display_width, display_height//8), int(60 + math.sin(pygame.time.get_ticks() / animation_speed)*4), centered=True)

            clock.tick(144)
            pygame.display.update((0, 0, display_width, GRID_POS[1]))



    def _draw_highscore(self, current: int) -> None:
        "Draws the 5 highest scores of all time to the right of the grid, highlighting the current score"
        try:
            drawn_box = False
            scores = [current]
            scores.extend(self.highscores)
            scores = sorted(scores)[:0:-1]
            for rank, score in enumerate(scores):
                if score == current and not drawn_box:
                    pygame.draw.rect(
                        display, 
                        Color.RED, 
                        (GRID_POS[0]+GRID_SIZE[1]*CELL_SIZE[0], display_height//4+rank*((display_height//2)//5), 200, (display_height//2)//5),
                        4
                    )
                    drawn_box = True
                write(
                    f"{rank + 1}:",
                    Color.BLUE,
                    (GRID_POS[0]+GRID_SIZE[1]*CELL_SIZE[0], display_height//4+rank*((display_height//2)//5), 50, (display_height//2)//5),
                    32,
                    centered = True
                )
                write(
                    f"{score}",
                    Color.GREEN,
                    (GRID_POS[0]+GRID_SIZE[1]*CELL_SIZE[0], display_height//4+rank*((display_height//2)//5), 200, (display_height//2)//5),
                    64,
                    centered = True
                )
        except AttributeError as attribute_error:
            self.highscores = self._load_highscores()



    def _load_highscores(self) -> List[int]:
        "Tries to load previously archieved scores, return all 0 on error"
        try: 
            with open("resources/.highscores.txt", "r") as file:
                highscores = list(map(int, file.read().replace("\n", "").split(",")))
                while len(highscores) < 5:
                    highscores.append(0)
                return highscores
        except Exception as e:
            print(f"Exception occured during highscore loading - {e}")
            return [0,0,0,0,0]



    def _safe_highscores(self) -> None:
        "Saves current highscore to persistent storage"
        try: 
            with open("resources/.highscores.txt", "w") as file:
                file.write(",".join(map(str, self.highscores)))
        except Exception as e:
            print(f"Exception occured during highscore saving - {e}")
    
