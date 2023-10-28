import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
ROAD_WIDTH = 100
DASH_LENGTH = 20
DASH_SPACE = 20
CAR_WIDTH, CAR_HEIGHT = 70, 50

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define the colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)

def draw_road(start_pos, end_pos):
    pygame.draw.line(screen, GRAY, start_pos, end_pos, ROAD_WIDTH)

def draw_dashed_line(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    num_dashes = int((dx**2 + dy**2)**0.5 // (DASH_LENGTH + DASH_SPACE))
    for i in range(num_dashes):
        start = x1 + i*(DASH_LENGTH + DASH_SPACE) * dx // (num_dashes * (DASH_LENGTH + DASH_SPACE)),\
                y1 + i*(DASH_LENGTH + DASH_SPACE) * dy // (num_dashes * (DASH_LENGTH + DASH_SPACE))
        end = start[0] + dx * DASH_LENGTH // (num_dashes * (DASH_LENGTH + DASH_SPACE)),\
              start[1] + dy * DASH_LENGTH // (num_dashes * (DASH_LENGTH + DASH_SPACE))
        pygame.draw.line(screen, WHITE, start, end, 2)

def draw_car(pos):
    pygame.draw.rect(screen, RED, (*pos, CAR_WIDTH, CAR_HEIGHT))

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # Draw two intersecting roads
        draw_road((0, HEIGHT//2), (WIDTH, HEIGHT//2))  # Horizontal road
        draw_road((WIDTH//2, 0), (WIDTH//2, HEIGHT))  # Vertical road

        # Draw road markings
        draw_dashed_line((0, HEIGHT//2), (WIDTH, HEIGHT//2))  # Horizontal road marking
        draw_dashed_line((WIDTH//2, 0), (WIDTH//2, HEIGHT))  # Vertical road marking

        # Draw a car
        draw_car((WIDTH // 2 - CAR_WIDTH // 2, HEIGHT // 2 + ROAD_WIDTH // 4))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
