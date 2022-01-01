import turtle
import math
import random
import pygame
import turtle as turtle

pygame.mixer.init()
laser_shot = pygame.mixer.Sound("laser_shot.wav")
explosion = pygame.mixer.Sound("explosion.wav")
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(-1)

wn = turtle.Screen()
wn.setup(700, 700)
wn.bgcolor("black")
wn.title("Space Invaders - 消灭入侵地球的外星飞船！")
wn.bgpic("background.gif")


turtle.register_shape("enemy.gif")
turtle.register_shape("tank.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.goto(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.forward(600)
    border_pen.lt(90)
border_pen.hideturtle()

score = 0

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.goto(-290, 270)

score_pen.write(f"Score:{score}", font=("Arial", 14))
score_pen.hideturtle()

player = turtle.Turtle()
player.shape("tank.gif")
player.speed(0)
player.penup()
player.goto(0, -250)
player.setheading(90)

player_speed = 15

num_enemies = 5
enemies = []

for i in range(num_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.shape("enemy.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.goto(x,y)

enemy_speed = 2

bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bullet_speed = 20
can_fire = True

def move_left():
    x = player.xcor()
    x -= player_speed
    if x > -280:
        player.setx(x)

def move_right():
    x = player.xcor()
    x += player_speed
    if x < 280:
        player.setx(x)

turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")

def fire_bullet():
    global can_fire
    if can_fire:
        laser_shot.play()
        # os.system("afplay laswr.wav&")
        can_fire = False
        x = player.xcor()
        y = player.ycor() + 10
        bullet.goto(x,y)
        bullet.showturtle()

def is_collided(t1, t2):
    c = math.sqrt((t1.xcor()- t2.xcor())**2 + (t1.ycor()- t2.ycor())**2)
    return c < 35

turtle.onkey(fire_bullet, "space")

playing = True
while True:

    for enemy in enemies:
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        if enemy.xcor() > 280 or enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemy_speed *= -1

        if is_collided(bullet, enemy):
            explosion.play()
            bullet.hideturtle()
            can_fire = True

            x = random.randint(-200, 200)
            y = random.randint(-200, 200)
            enemy.goto(x,y)

            score += 10
            score_pen.clear()
            score_pen.write(f"Score: {score}", font=("Arial", 14))

        if is_collided(player, enemy) or enemy.ycor() < -290:
            explosion.play()
            player.hideturtle()
            enemy.hideturtle()
            pygame.mixer.stop()
            playing = False

            gameover = turtle.Turtle()
            gameover.hideturtle()
            gameover.setx(-260)
            gameover.color("white")
            gameover.write("GAME OVER!!!", font=("Arial", 64))

            break


        if not can_fire:
            bullet.sety(bullet.ycor() + 20)

        if bullet.ycor() > 275:
            bullet.hideturtle()
            can_fire = True


turtle.exitonclick()
