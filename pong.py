import pygame, sys
from pygame.locals import *
from pygame.math import Vector2

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BALL_SIZE = 20
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80
PADDLE_SPEED = 250

INIT_BALL_SPEED = 400 #moves 150 pixels per second across the hypotenuse
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

INTRO_FONT_SIZE = 32
SCORE_FONT_SIZE = 20

INTRO_SCREEN = "INTRO_SCREEN"
GAME_PLAY = "GAME_PLAY"
GAME_OVER = "GAME_OVER"

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def main():
    global speed, left_paddle, right_paddle, ball, intro_font, score_font, score_1, score_2
    pygame.init()
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("Pong")
    background = pygame.image.load("background.png")

    ball_pos = Vector2(WINDOW_WIDTH//4, WINDOW_HEIGHT//2) #using a vector to represent position!
    ball = pygame.Rect(*ball_pos, BALL_SIZE, BALL_SIZE) # Using * UNPACKS a tuple into 2 values

    left_paddle_pos = Vector2(50, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2)#
    left_paddle = pygame.Rect(*left_paddle_pos, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    right_paddle_pos = Vector2(WINDOW_WIDTH - (50 + PADDLE_WIDTH), WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2)#
    right_paddle = pygame.Rect(*right_paddle_pos, PADDLE_WIDTH, PADDLE_HEIGHT)

    movement_vector = Vector2(1, 0)
    movement_vector = movement_vector.normalize()

    intro_font = pygame.font.Font('freesansbold.ttf', INTRO_FONT_SIZE)
    score_font = pygame.font.Font('freesansbold.ttf', INTRO_FONT_SIZE)

    speed = INIT_BALL_SPEED
    score_1 = 0
    score_2 = 0

    #Normal Vectors for all walls of the screen
    right_normal_vector = Vector2(-1, 0)
    top_normal_vector = Vector2(0, 1)
    left_normal_vector = Vector2(1, 0)
    bottom_normal_vector = Vector2(0, -1)
    
    game_state = INTRO_SCREEN
    time = CLOCK.tick() #gives us a fresh start on the time (ignores start set-up time)
    key_pressed = False
    mouse_clicked = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_clicked = True
            elif event.type == KEYDOWN:
                key_pressed = True
                if event.key == K_w:
                    w_pressed = True
                if event.key == K_s:
                    s_pressed = True
                if event.key == K_UP:
                    up_pressed = True
                if event.key == K_DOWN:
                    down_pressed = True
            elif event.type == KEYUP:
                if event.key == K_w:
                    w_pressed = False
                if event.key == K_s:
                    s_pressed = False
                if event.key == K_UP:
                    up_pressed = False
                if event.key == K_DOWN:
                    down_pressed = False
                    
        if game_state == INTRO_SCREEN:
            displayIntroScreen()
            w_pressed = False
            s_pressed = False
            up_pressed = False
            down_pressed = False
            if key_pressed or mouse_clicked:
                game_state = GAME_PLAY

        elif game_state == GAME_PLAY:
            
            SCREEN.blit(background, (0, 0))
            displayScore()
            time = CLOCK.tick()
            time_seconds = time / 1000 #how much time in seconds have elapsed

            distance_moved = time_seconds * speed #calculate desired movement magnitude in that time slice
            ball_pos += movement_vector * distance_moved#add that movement to my current position

            ball.center = tuple(ball_pos)

            r_vector = Vector2(0, 0)
            l_vector = Vector2(0, 0)
            
            if ball.right >= WINDOW_WIDTH and movement_vector.x > 0:#Player1 Scores point
                score_2 += 1
                pygame.event.clear()
                movement_vector = Vector2(-1, 0)
                ball_pos = Vector2(WINDOW_WIDTH//4, WINDOW_HEIGHT//2)
                speed = 250
                
                
                
                # movement_vector.x *= -1

            if ball.left <= 0 and movement_vector.x < 0:#player2 Scores point
                score_1 += 1
                pygame.event.clear()
                movement_vector = Vector2(1, 0)
                ball_pos = Vector2(WINDOW_WIDTH//4, WINDOW_HEIGHT//2)
                speed = 250
                # movement_vector.x *= -1
                
            if ball.bottom >= WINDOW_HEIGHT and movement_vector.y > 0:
                movement_vector = movement_vector.reflect(top_normal_vector)
            if ball.top <= 0 and movement_vector.y < 0:
                movement_vector = movement_vector.reflect(bottom_normal_vector)
            
            if w_pressed and left_paddle.top >= 0:
                l_vector += Vector2(0, -1)
            if s_pressed and left_paddle.bottom <= WINDOW_HEIGHT:
                l_vector += Vector2(0, 1)
            if up_pressed and right_paddle.top >= 0:
                r_vector += Vector2(0, -1)
            if down_pressed and right_paddle.bottom <= WINDOW_HEIGHT:
                r_vector += Vector2(0, 1)

            paddle_distance_moved = time_seconds * PADDLE_SPEED

            right_paddle_pos += r_vector * paddle_distance_moved
            left_paddle_pos += l_vector * paddle_distance_moved
            
            right_paddle.topright = (WINDOW_WIDTH - 50, right_paddle_pos.y)
            left_paddle.topleft = (50, left_paddle_pos.y)

            if right_paddle.colliderect(ball) and movement_vector.x > 0:
                movement_vector.x *= -1
                speed += 25
                movement_vector = (r_vector * PADDLE_SPEED) + (movement_vector * speed)
                movement_vector = movement_vector.normalize()
            elif left_paddle.colliderect(ball) and movement_vector.x < 0:
                movement_vector.x *= -1
                speed += 25
                movement_vector = (l_vector * PADDLE_SPEED) + (movement_vector * speed)
                movement_vector = movement_vector.normalize()
                
            if score_1 == 3:
                game_state = GAME_OVER
            elif score_2 == 3:
                game_state = GAME_OVER
            draw_paddle_and_ball()
            
        elif game_state == GAME_OVER:
            score_1, score_2 = 0, 0
            w_pressed = False
            s_pressed = False
            up_pressed = False
            down_pressed = False
            if key_pressed or mouse_clicked:
                game_state = GAME_PLAY

        
        pygame.display.update()


def draw_paddle_and_ball():
    pygame.draw.rect(SCREEN, WHITE, left_paddle)
    pygame.draw.rect(SCREEN, WHITE, right_paddle)
    pygame.draw.rect(SCREEN, WHITE, ball)


def displayIntroScreen():
    SCREEN.fill(BLACK)
    intro_msg1 = intro_font.render('Pong |  .   |', True, WHITE)
    text_intro = intro_msg1.get_rect()
    text_intro.midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    SCREEN.blit(intro_msg1, text_intro)
    
    intro_msg2 = intro_font.render('Click or press any key to start', True, WHITE)
    text_rect_obj = intro_msg2.get_rect()
    text_rect_obj.midtop = text_intro.midbottom
    SCREEN.blit(intro_msg2, text_rect_obj)


def displayScore():
    score_msg_1 = score_font.render(f'{score_1}', True, WHITE)
    score_msg_2 = score_font.render(f'{score_2}', True, WHITE)
    score_text_1 = score_msg_1.get_rect()
    score_text_2 = score_msg_2.get_rect()
    score_text_1.midtop = (WINDOW_WIDTH // 4, 30)
    score_text_2.midtop = (WINDOW_WIDTH // 4 * 3, 30)
    SCREEN.blit(score_msg_1, score_text_1)
    SCREEN.blit(score_msg_2, score_text_2)
    
if __name__ == '__main__':
    main()
