#Initialization -------------------------------------------------------------------------------
import pygame, sys
import random
from pygame.locals import QUIT

pygame.init()
screen_size = [800, 1000]
screen_w = screen_size[0]
screen_h = screen_size[1]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Minesweeper')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)

NAVY = (133, 33, 255)
BROWN = (97, 34, 2)
TEAL = (74, 217, 193)
PINK = (255, 33, 222)
MAROON = (128, 0, 0)
LIGHT_GRAY = (200, 200, 200)
GRAY = (100, 100, 100)
DARK_GRAY = (20, 20, 20)

# Helps for checking adjacent cells
dx = [-1, 0, 1, -1, 1, -1, 0, 1]
dy = [-1, -1, -1, 0, 0, 1, 1, 1]

# Minesweeper Grid ---------------------------------------------------------------------------

# Function to get whether x y coords are in a grid
def in_bounds(x, y, grid_dims):
    if (x >= 0) and (y >= 0) and (x < grid_dims[0]) and (y < grid_dims[1]):
        return True
    else:
        return False

# Specify Constants
grid_dims = [20, 20]
grid_w = grid_dims[0]
grid_h = grid_dims[1]
minesweeper_colours = [WHITE, BLUE, GREEN, RED, NAVY, BROWN, TEAL, PINK, GRAY]
num_mines = 50

# Gets a random assortment of cells in grid
coords = [x for x in range(grid_w*grid_h)]
mine_coords = sorted(random.sample(coords, num_mines))
mine_coords.append(-1)

# Prepopulates Grid
minesweeper_grid = [ [0 for x in range(grid_w)] for y in range(grid_h) ]

# Uses pointer to set mines according to predetermined positions
L = 0
for row in range(grid_h):
    for col in range(grid_w):
        if (row*grid_w +col == mine_coords[L]):
            L += 1
            minesweeper_grid[row][col] = 'F'

# Determines the surrounding adjacent 8 mines for each cell
for row in range(grid_h):
    for col in range(grid_w):
        if (minesweeper_grid[row][col] != 'F'):     
            surroundings = 0
            for i in range(8):
                check_x = col + dx[i]
                check_y = row + dy[i]
                if (in_bounds(check_x, check_y, grid_dims)):
                    if (minesweeper_grid[check_y][check_x] == 'F'):
                        surroundings += 1
            minesweeper_grid[row][col] = surroundings

# Prepopulates boolean arrays for visited + flagged cells
revealed = [ [False for x in range(grid_w)] for y in range(grid_h) ]
flagged = [ [False for x in range(grid_w)] for y in range(grid_h) ]

cell_width = screen_w / grid_w

screen.fill((0, 100, 0))

# Number Font
font = pygame.font.SysFont('callisto', 50)
bigger_font = pygame.font.SysFont('callisto', 80)

# Functions ----------------------------------------------------------------------------------



def draw_game():
    # Draws the numbers and colours underneath
    for row in range(grid_h):
        for col in range(grid_w):
            if (minesweeper_grid[row][col] == 'F'):
                pygame.draw.rect(screen, BLACK, (cell_width*row, cell_width*col, cell_width, cell_width))
            else:
                pygame.draw.rect(screen, minesweeper_colours[minesweeper_grid[row][col]], (cell_width*row, cell_width*col, cell_width, cell_width))
                num_text = font.render(f'{minesweeper_grid[row][col]}', True, WHITE)
                num_text_rect = num_text.get_rect(center=(cell_width*row + cell_width/2, cell_width*col + cell_width/2))

                screen.blit(num_text, num_text_rect)

    # Draws the black checkerboard overtop all non-revealed tiles
    for row in range(grid_h):
        for col in range(grid_w):
            if (revealed[row][col] == False):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, BLACK, (cell_width*row, cell_width*col, cell_width, cell_width))
                else:
                    pygame.draw.rect(screen, DARK_GRAY, (cell_width*row, cell_width*col, cell_width, cell_width))
    
    # Draws all flags over flagged spaces
    flag = pygame.transform.scale((pygame.image.load("Images/flag.png")), [cell_width, cell_width])
    for row in range(grid_h):
        for col in range(grid_w):
            if (flagged[row][col] == True):
                screen.blit(flag, (cell_width*row, cell_width*col))

# Draws container at the bottom of the screen
def bottom_container():
    pygame.draw.rect(screen, BLACK, [0, 800, screen_w, 200])
    pygame.draw.rect(screen, (34, 23, 45), [10, 810, screen_w-20, 200-20])

# On bomb detonate
loss_coords = (0, 0)
def lose():
    global loss_coords, time_init, time_end
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kill Game XDDD
            pygame.quit()
            sys.exit()

    draw_game()
    # Mine that was set off
    pygame.draw.rect(screen, MAROON, (cell_width*loss_coords[0], cell_width*loss_coords[1], cell_width, cell_width))

    # Shows user all mines
    mine = pygame.transform.scale((pygame.image.load("Images/mine.png")), [cell_width, cell_width])
    for row in range(grid_h):
        for col in range(grid_w):
            if (revealed[row][col] == False) and (minesweeper_grid[row][col] == 'F') and (flagged[row][col] == False):
                screen.blit(mine, (cell_width*row, cell_width*col))

    # Time Text
    bottom_container()
    time_text = bigger_font.render(f'You lost in: {(round(time_end - time_init) // 1000)} Seconds', True, RED)
    time_text_rect = time_text.get_rect(center=(screen_w/2, 200/2 + 800))
    screen.blit(time_text, time_text_rect)

    pygame.display.update()

# Classes for preset assets
class Flag(pygame.sprite.Sprite):
    def __init__(self, cell_width):
        self.image = pygame.transform.scale((pygame.image.load("Images/flag.png")), [cell_width, cell_width])
        self.x_pos = (random.randint(0, screen_size[0]-self.size))
        self.y_pos = (random.randint(0, screen_size[1]-self.size))

    def draw(self):
        screen.blit(self.image, [self.x_pos, self.y_pos])

class Mine(pygame.sprite.Sprite):
    def __init__(self, cell_width):
        self.image = pygame.transform.scale((pygame.image.load("Images/mine.png")), [cell_width, cell_width])
        self.x_pos = (random.randint(0, screen_size[0]-self.size))
        self.y_pos = (random.randint(0, screen_size[1]-self.size))

    def draw(self):
        screen.blit(self.image, [self.x_pos, self.y_pos])

# Game Loop ------------------------------------------------------------------------------------
clock = pygame.time.Clock()
FPS = 1000
currentFPS = 0
screen = pygame.display.set_mode([800, 800])
game_state = 0

time_init = 0
time_end = 0

# Loading Screen
def pregame():
    global screen
    global game_state, time_init
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            screen = pygame.display.set_mode([800, 1000])
            game_state = 1
            

    # Center Text
    screen.fill(GRAY)
    pregame_text = font.render(f'Click to Begin', True, WHITE)
    pregame_textrect = pregame_text.get_rect(center=(800/2, 800/2))
    pygame.draw.rect(screen, BLACK, [150, 350, 500, 100])
    screen.blit(pregame_text, pregame_textrect)


    pygame.display.update()

# Main Game Loop
def game():
    global game_state, loss_coords, time_init, time_end
    screen.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # If Left Click
                select_x = round(mouse_pos[0] // cell_width)
                select_y = round(mouse_pos[1] // cell_width)
                if (select_y >= grid_dims[1]):
                    print('e')
                # Check if cell has been flagged
                elif not flagged[select_x][select_y]:

                    if revealed[select_x][select_y] == False:
                        revealed[select_x][select_y] = True
                        print(minesweeper_grid[select_x][select_y])


                        # HUGE BFS CHECK for clearing big sweep areas if player clicks a 0
                        if (minesweeper_grid[select_x][select_y] == 0):
                            stack = [(select_x, select_y)]
                            while (stack != []):
                                curr = stack.pop(0)
                                for i in range(8):
                                    if (in_bounds(curr[0]+dx[i], curr[1]+dy[i], grid_dims)):
                                        if (revealed[curr[0]+dx[i]][curr[1]+dy[i]] == False):

                                            revealed[curr[0]+dx[i]][curr[1]+dy[i]] = True
                                            if (minesweeper_grid[curr[0]+dx[i]][curr[1]+dy[i]] == 0):
                                                stack.append((curr[0]+dx[i], curr[1]+dy[i]))

                    else: # CHORD CHECKING!!!
                        
                        # Counts surrounding flags
                        surroundings = 0
                        for i in range(8):
                            check_x = select_x + dx[i]
                            check_y = select_y + dy[i]
                            if (in_bounds(check_x, check_y, grid_dims)):
                                if (flagged[check_x][check_y]):
                                    surroundings += 1
                        
                        # Does a chord click if flags match the number
                        if surroundings == minesweeper_grid[select_x][select_y]:
                            stack = []
                            for i in range(8):
                                check_x = select_x + dx[i]
                                check_y = select_y + dy[i]
                                if (in_bounds(check_x, check_y, grid_dims)):
                                    if flagged[check_x][check_y] == False:

                                        if minesweeper_grid[check_x][check_y] == 'F':
                                            loss_coords = (check_x, check_y)
                                            time_end = pygame.time.get_ticks()
                                            game_state = 3

                                        elif minesweeper_grid[check_x][check_y] == 0:
                                            stack.append((check_x, check_y))

                                        revealed[check_x][check_y] = True
                            
                            # MORE BFS :D (if we found a zero)
                            while (stack != []):
                                curr = stack.pop(0)
                                for i in range(8):
                                    if (in_bounds(curr[0]+dx[i], curr[1]+dy[i], grid_dims)):
                                        if (revealed[curr[0]+dx[i]][curr[1]+dy[i]] == False):

                                            revealed[curr[0]+dx[i]][curr[1]+dy[i]] = True
                                            if (minesweeper_grid[curr[0]+dx[i]][curr[1]+dy[i]] == 0):
                                                stack.append((curr[0]+dx[i], curr[1]+dy[i]))
                            # ---------------------------------------------------------------


                    # If mine is hit
                    if (minesweeper_grid[select_x][select_y] == 'F'):
                        loss_coords = (select_x, select_y)
                        time_end = pygame.time.get_ticks()
                        game_state = 3

            if event.button == 3: # If right click
                select_x = round(mouse_pos[0] // cell_width)
                select_y = round(mouse_pos[1] // cell_width)
                # Flags or Unflags
                if flagged[select_x][select_y]:
                    flagged[select_x][select_y] = False
                elif revealed[select_x][select_y] == False:
                    flagged[select_x][select_y] = True

    mouse_pos = pygame.mouse.get_pos()

    # Calculates Time and Mines left
    curr_time = (round(pygame.time.get_ticks() - time_init) // 1000)
    curr_mines = num_mines - sum([x.count(True) for x in flagged])
    time_text = bigger_font.render(f"{curr_time} Second{'s' if curr_time != 1 else ''} | {curr_mines} Mine{'s' if curr_mines != 1 else ''}", True, WHITE)
    time_text_rect = time_text.get_rect(center=(screen_w/2, 200/2 + 800))
    

    # Checks if every safe cell is revealed (win condition)
    if (sum([x.count(True) for x in revealed]) == grid_w*grid_h-num_mines):
        time_end = pygame.time.get_ticks()
        game_state = 2

    
    # DRAW FUNCTIONS -------------------------------------------------------------------------------------------------------------------------------------

    draw_game()

    bottom_container()
    screen.blit(time_text, time_text_rect)
    # Updates the screen
    pygame.display.update()


# After Game End
def postgame():
    global time_init, time_end
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    # Draw old game and container presets
    draw_game()
    bottom_container()
    # Final Messages
    time_text = bigger_font.render(f'You won in: {(round(time_end - time_init) // 1000)} Seconds', True, GREEN)
    time_text_rect = time_text.get_rect(center=(screen_w/2, 200/2 + 800))
    screen.blit(time_text, time_text_rect)
    pygame.display.update()
    

while True:
    clock.tick(FPS)
    
    if round(clock.get_fps()) != currentFPS:
        print(f'FPS: {round(clock.get_fps())}')
        currentFPS = round(clock.get_fps())

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Handles what state the game is in
    while game_state == 0:
        pregame()
    while game_state == 1:
        game()
    while game_state == 2:
        postgame()
    while game_state == 3:
        lose()