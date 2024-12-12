import pygame
import sys
import random
import time

# Initialisierung von Pygame
pygame.init()

# Sound für das Futtergeräusch laden
# eat = pygame.mixer.Sound('Pfad zur Datei')

# Einstellungen für das Spielfenster
width, height = 840, 600
window_size = (width, height)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Snake Spiel")

# Farben
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Schriftart und Textgröße für die Anzeige der gefressenen Äpfel und "ENDE"
font = pygame.font.Font(None, 50)
end_font = pygame.font.Font(None, 100)
start_font = pygame.font.Font(None, 30)
pause_font = pygame.font.Font(None, 80)

# Snake Einstellungen
snake_size = 15
snake_speed = 15

# Initialisierung der Schlange
snake = [(width // 2, height // 2), (width // 2 - snake_size, height // 2)]
snake_direction = (1, 0)

# Initialisierung des Apfels
apple = None

def place_apple():
    global apple
    while True:
        apple_candidate = (random.randrange(1, (width // snake_size)) * snake_size,
                           random.randrange(1, (height // snake_size)) * snake_size)
        if (apple_candidate not in snake):
            apple_rect = pygame.Rect(apple_candidate[0], apple_candidate[1], snake_size, snake_size)
            text_rect = pygame.Rect(width - 180, 20, 150, 50)  # Rechteck für den Text "Äpfel: "
            if not apple_rect.colliderect(text_rect):
                apple = apple_candidate
                break

# Ersten Apfel platzieren
place_apple()

# Anzahl der gefressenen Äpfel
apples_eaten = 0

# Variable für die Endbedingung
end_condition = False

# Zeitpunkt, an dem ENDE angezeigt wird
end_display_time = None

# Zeitpunkt, an dem der Anfangsbildschirm angezeigt wird
start_display_time = None

# Zeitpunkt, an dem das Spiel pausiert wurde
pause_time = None

# Pause-Flag
paused = False

# Anfangsbildschirm anzeigen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Wenn eine Taste gedrückt wird, starte das Spiel
            start_display_time = time.time()

    # Anfangsbildschirm anzeigen
    window.fill(black)
    start_text = start_font.render("Snake mit beliebiger Taste starten... Steuerung mit den Pfeiltasten. [P] = Pause", True, white)
    window.blit(start_text, ((width - start_text.get_width()) // 2, (height - start_text.get_height()) // 2))

    pygame.display.flip()

    # Überprüfen, ob das Spiel gestartet werden soll
    if start_display_time is not None and time.time() - start_display_time > 0.5:
        break

    pygame.time.Clock().tick(snake_speed)

# Hauptspiel-Schleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not end_condition and event.key == pygame.K_p:
                if paused:
                    pause_time = None
                    paused = False
                else:
                    paused = True
                    pause_time = time.time()
                    pause_text = pause_font.render("Pause", True, white)
                    window.blit(pause_text, ((width - pause_text.get_width()) // 2, (height - pause_text.get_height()) // 2))

            if not paused:
                if not end_condition:
                    if event.key == pygame.K_UP and snake_direction != (0, 1):
                        snake_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                        snake_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                        snake_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                        snake_direction = (1, 0)

    if not paused:
        if end_condition:
            if end_display_time is None:
                end_display_time = time.time()
            current_time = time.time()
            if current_time - end_display_time > 5:
                pygame.quit()
                sys.exit()
        else:
            # Bewegung der Schlange
            snake_head = (snake[0][0] + snake_direction[0] * snake_size,
                          snake[0][1] + snake_direction[1] * snake_size)
                    # Überprüfen, ob die Schlange die Wände trifft
        if not (0 <= snake_head[0] < width and 0 <= snake_head[1] < height):
            end_condition = True
            snake_head = (min(max(snake_head[0], 0), width - snake_size), min(max(snake_head[1], 0), height - snake_size))
        else:
            snake.insert(0, snake_head)

        # Überprüfen, ob die Schlange den Apfel gegessen hat
        if snake_head == apple:
            place_apple()
            apples_eaten += 1
            # Soundeffekt
        #   pygame.mixer.Sound.play(eat)
        else:
            if snake:  # Überprüfe, ob die Schlange nicht leer ist
                snake.pop()

        # Überprüfen, ob die Schlange mit sich selbst kollidiert
        if snake_head in snake[1:]:
            end_condition = True

        # Zeichnen des Spielfensters
        window.fill(black)
        pygame.draw.rect(window, red, (apple[0], apple[1], snake_size, snake_size))

        for segment in snake:
            pygame.draw.rect(window, white, (segment[0], segment[1], snake_size, snake_size))

        # Anzeige der Anzahl der gefressenen Äpfel oben rechts
        text = font.render("Äpfel:  {}".format(apples_eaten), True, white)
        window.blit(text, (width - 180, 20))

        # Überprüfen, ob das ENDE angezeigt werden soll
        if end_condition:
            end_text = end_font.render("ENDE", True, blue)
            window.blit(end_text, ((width - end_text.get_width()) // 2, (height - end_text.get_height()) // 2))

    pygame.display.flip()
    pygame.time.Clock().tick(snake_speed)