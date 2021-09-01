import pygame
import random # 17. enemy를 random하게 움직이도록 하기 위함.
import math # 21. 적 죽는 것 감지하기 위한 모듈
from pygame import mixer # 음악을 사용하기 위함

# pip install pyinstaller

# freepik
# flaticon

# objects 64pixel
# icon 32pixel
# bullet 32pixel
# background 800 * 600

# 1. 파이게임을 시작.
pygame.init()

# 스크린 만들기
# 창의 너비: 800 높이: 600 스크린이나, 아이콘이나 영점은 항상 왼쪽 위다.
screen = pygame.display.set_mode((800, 600))

# 18. Background
background = pygame.image.load('image/background.jpg') # 18. adding background
brighten = 15
background.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)


# Background Sound
mixer.music.load('sound/Wave.mp3')
mixer.music.play(-1) # -1을 넣으면 반복 재생

# Title and Icon
pygame.display.set_caption("Space Invaders") # 5. 제목 정하기
# https://www.flaticon.com 사이트에서 컬렉션에 넣고 32픽셀로 아이콘 만들기
icon = pygame.image.load('image/spaceship.png') # 6. icon 객체에 pygame.image.load()메서드를 이용해 이미지를 넣는다.
pygame.display.set_icon(icon)  # 이미지를 적용시킨다.

# 8. Player
playerImg = pygame.image.load('image/ufo64.png')
playerX = 370  # playerImg가 위치할 x좌표 좌측이 0 오른쪽으로 갈 수록 커진다.
playerY = 480  # playerImg가 위차할 y좌표 위쪽이 0 아래로 갈 수록 커진다.
playerX_change = 0

# 16. Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('image/alien64.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# enemy 하나의 경우
# enemyImg = pygame.image.load('alien64.png')
# enemyX = random.randint(0, 800)  # 17. random함수 적용
# enemyY = random.randint(50, 150)  # 17. random함수 적용
# enemyX_change = 4
# enemyY_change = 40

# 19. Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('image/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"

# Score
# score = 0
score_value = 0
font = pygame.font.Font('font/SEBANG Gothic Bold.ttf', 32)

textX = 10 # top_left에 나오도록
textY = 10

# Game Over
over_font = pygame.font.Font('font/SEBANG Gothic Bold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# 9. player를 그릴 메소드 정의
# x와 y를 인자로 받아서, 해당 위치로 오브젝트를 옮긴다.
def player(x, y):  # 12. 인자 두 개를 받는 형태로 수정
    screen.blit(playerImg, (x, y))  # draw player


def enemy(x, y, i):  # 16
    screen.blit(enemyImg[i], (x, y))  # 16. draw enemy


# 19. bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16, y+10)) # spaceship의 중앙에서 총알이 나가도록 하기 위함


# 21. distance
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance <27:
        return True
    else:
        return False


# 2. 화면이 계속 켜져있도록 한다.
# Game Loop
running = True

while running:
    for event in pygame.event.get():  # 3. 발생하는 이벤트를 모두 확인한다.
        if event.type == pygame.QUIT:  # 4. 화면 닫기를 누르면 게임 창이 종료되도록 한다. pygame.QUIT()는 종료 버튼이 눌렸는지를 체크하는 함수이다.
            running = False
            # 13. if keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            # print("키스트로크가 press됐습니다.") # 14. 키 테스트
            if event.key == pygame.K_LEFT:
                # print("왼쪽 입력") #14. 키 테스트
                playerX_change = -5 #15. 키 적용
            if event.key == pygame.K_RIGHT:
                # print("오른쪽 입력") # 14. 키 테스트
                playerX_change = 5 #15. 키 적용
            if event.key == pygame.K_SPACE:  # 19.
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('sound/laser.wav') # 총알이 나갈 때
                    bullet_Sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("키스트로크가 release됐습니다.") # 14. 키 테스트
                playerX_change = 0  #15. 키 적용
    screen.fill((0, 0, 0)) # 7. RGB 설정
    # 18. Background Image
    screen.blit(background, (0,0))

    # playerX += 0.2
    # 5 = 5 + -0.1 -> 5 = 5- 0.1
    # 5 = 5 + 0.1

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <=0:
        playerX = 0
    elif playerX >= 736: # png 가 64픽셀의 크기를 가지므로
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text ()
            break




        enemyX[i] += enemyX_change[i]

        # 적 하나
        # enemyX += enemyX_change

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # png 가 64픽셀의 크기를 가지므로
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_Sound = mixer.Sound('image/explosion.wav')  # 총알이 나갈 때
            bullet_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # 20. Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change




    # collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    # if collision:
    #     bulletY = 480
    #     bullet_state = "ready"
    #     score += 1
    #     print(score)
    #     enemyX = random.randint(0, 735)
    #     enemyY = random.randint(50, 150)


    player(playerX, playerY)  # 10. screen이 먼저 올라오므로 , 그 위에 플레이어 아이콘이 쌓인다.
    # enemy(enemyX, enemyY)
    show_score(textX, textY)
    pygame.display.update()  # 11. 그 후 디스플레이가 업데이트 되도록 해야한다.
    # 64픽셀로 우주선 아이콘 다운로드
