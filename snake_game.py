import turtle
import random
import time

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20
DELAY = 0.1

def setup_screen():
    screen = turtle.Screen()
    screen.title("Snake Game")
    screen.bgcolor("black")
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.tracer(0)
    return screen

def create_pen():
    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, SCREEN_HEIGHT / 2 - 40)
    return pen

def create_food():
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("red")
    food.penup()
    food.goto(0, 0)
    return food

def create_segment(x=0, y=0):
    seg = turtle.Turtle()
    seg.speed(0)
    seg.shape("square")
    seg.color("lime green")
    seg.penup()
    seg.goto(x, y)
    return seg

def place_food(food, segments):
    while True:
        x = random.randint(-(SCREEN_WIDTH // 2 - CELL_SIZE) // CELL_SIZE,
                            (SCREEN_WIDTH // 2 - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(-(SCREEN_HEIGHT // 2 - CELL_SIZE) // CELL_SIZE,
                            (SCREEN_HEIGHT // 2 - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        pos = (x, y)
        if not any(int(s.xcor()) == x and int(s.ycor()) == y for s in segments):
            food.goto(x, y)
            return

def main():
    screen = setup_screen()
    pen = create_pen()
    food = create_food()

    segments = []
    head = create_segment(0, 0)
    head.color("white")
    segments.append(head)

    score = 0
    high_score = 0
    direction = "stop"

    def go_up():
        nonlocal direction
        if direction != "down":
            direction = "up"

    def go_down():
        nonlocal direction
        if direction != "up":
            direction = "down"

    def go_left():
        nonlocal direction
        if direction != "right":
            direction = "left"

    def go_right():
        nonlocal direction
        if direction != "left":
            direction = "right"

    screen.listen()
    screen.onkeypress(go_up, "Up")
    screen.onkeypress(go_down, "Down")
    screen.onkeypress(go_left, "Left")
    screen.onkeypress(go_right, "Right")
    screen.onkeypress(go_up, "w")
    screen.onkeypress(go_down, "s")
    screen.onkeypress(go_left, "a")
    screen.onkeypress(go_right, "d")

    def reset():
        nonlocal score, direction
        time.sleep(0.5)
        direction = "stop"
        for seg in segments[1:]:
            seg.hideturtle()
        segments.clear()
        head.goto(0, 0)
        head.color("white")
        segments.append(head)
        score = 0
        place_food(food, segments)
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}",
                  align="center", font=("Courier", 18, "bold"))

    place_food(food, segments)
    pen.write(f"Score: {score}  High Score: {high_score}",
              align="center", font=("Courier", 18, "bold"))

    while True:
        screen.update()
        time.sleep(DELAY)

        if direction == "stop":
            continue

        # Move the body segments
        for i in range(len(segments) - 1, 0, -1):
            x = segments[i - 1].xcor()
            y = segments[i - 1].ycor()
            segments[i].goto(x, y)

        # Move head
        if direction == "up":
            head.sety(head.ycor() + CELL_SIZE)
        elif direction == "down":
            head.sety(head.ycor() - CELL_SIZE)
        elif direction == "left":
            head.setx(head.xcor() - CELL_SIZE)
        elif direction == "right":
            head.setx(head.xcor() + CELL_SIZE)

        # Wall collision
        if (head.xcor() > SCREEN_WIDTH / 2 - CELL_SIZE / 2 or
                head.xcor() < -SCREEN_WIDTH / 2 + CELL_SIZE / 2 or
                head.ycor() > SCREEN_HEIGHT / 2 - CELL_SIZE / 2 or
                head.ycor() < -SCREEN_HEIGHT / 2 + CELL_SIZE / 2):
            reset()
            continue

        # Self collision
        for seg in segments[1:]:
            if head.distance(seg) < CELL_SIZE / 2:
                reset()
                break
        else:
            # Food collision
            if head.distance(food) < CELL_SIZE:
                score += 10
                if score > high_score:
                    high_score = score
                pen.clear()
                pen.write(f"Score: {score}  High Score: {high_score}",
                          align="center", font=("Courier", 18, "bold"))

                new_seg = create_segment()
                new_seg.goto(segments[-1].xcor(), segments[-1].ycor())
                segments.append(new_seg)

                place_food(food, segments)

if __name__ == "__main__":
    main()
    turtle.mainloop()
