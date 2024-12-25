import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Background intro image
background_img = pygame.image.load("Background.jpg")  # Add a background image
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load spaceship image
spaceship_img = pygame.image.load("spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (100, 80))
spaceship_rect = spaceship_img.get_rect()
spaceship_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)

# Load enemy images
alien_img = pygame.image.load("badguy.PNG")
alien_img = pygame.transform.scale(alien_img, (50, 50))
asteroid_img = pygame.image.load("asteroid.PNG")
asteroid_img = pygame.transform.scale(asteroid_img, (75, 75))

# Explosion images (load one or multiple frames for animation)
explosion_img = pygame.image.load("explosion.jpg")
explosion_img = pygame.transform.scale(explosion_img, (50, 50))

# Bullet settings
bullets = []
BULLET_SPEED = -10

# Enemy and enemy bullet settings
enemies = []
enemy_bullets = []
ENEMY_SPEED = 5
ENEMY_BULLET_SPEED = 7
ENEMY_INTERVAL = 1000  # Milliseconds
ALIEN_SCORE = 10
ASTEROID_SCORE = 0

# Explosion settings
explosions = []
EXPLOSION_DURATION = 30  # Frames
EXPLOSION_COLORS = [YELLOW, ORANGE, RED]

# Fonts and score
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
score = 0
top_score = 0

# Sound effects
bullet_sound = pygame.mixer.Sound("bulletsound.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Game state
running = True
game_over = False
intro_screen = True

# Timers for enemies
pygame.time.set_timer(pygame.USEREVENT, ENEMY_INTERVAL)

# Game loop
while running:
    if intro_screen:
        screen.blit(background_img, (0, 0))

        # Display title and options
        title_text = large_font.render("SpaceForce", True, WHITE)
        start_text = font.render("Press S to Start", True, WHITE)
        quit_text = font.render("Press Q to Quit", True, WHITE)

        screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 300))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 250))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    intro_screen = False  # Exit intro screen
                if event.key == pygame.K_q:
                    running = False
        continue

    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                # Shoot bullet
                bullet = pygame.Rect(
                    spaceship_rect.centerx - 5, spaceship_rect.top, 10, 20
                )
                bullets.append(bullet)
                bullet_sound.play() 
        if event.type == pygame.USEREVENT and not game_over:
            # Spawn enemies
            enemy_type = random.choice(["alien", "asteroid"])
            enemy_x = random.randint(0, SCREEN_WIDTH - 50)
            enemy_y = -50
            enemies.append({
                "rect": pygame.Rect(enemy_x, enemy_y, 50, 50),
                "type": enemy_type,
            })
            # Aliens randomly shoot bullets
            if enemy_type == "alien" and random.random() < 0.5:  # 50% chance
                enemy_bullet = pygame.Rect(enemy_x + 25, enemy_y + 50, 10, 20)
                enemy_bullets.append(enemy_bullet)
                bullet_sound.play() 

    if not game_over:
        # Move spaceship
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_rect.left > 0:
            spaceship_rect.move_ip(-8, 0)
        if keys[pygame.K_RIGHT] and spaceship_rect.right < SCREEN_WIDTH:
            spaceship_rect.move_ip(8, 0)

        # Move bullets
        for bullet in bullets[:]:
            bullet.move_ip(0, BULLET_SPEED)
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Move enemies
        for enemy in enemies[:]:
            enemy["rect"].move_ip(0, ENEMY_SPEED)
            if enemy["rect"].top > SCREEN_HEIGHT:
                enemies.remove(enemy)

        # Move enemy bullets
        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.move_ip(0, ENEMY_BULLET_SPEED)
            if enemy_bullet.top > SCREEN_HEIGHT:
                enemy_bullets.remove(enemy_bullet)

        # Check collisions with bullets
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy["rect"]):
                    bullets.remove(bullet)
                    explosions.append({"rect": enemy["rect"].copy(), "timer": EXPLOSION_DURATION})
                    enemies.remove(enemy)
                    explosion_sound.play()
                    if enemy["type"] == "alien":
                        score += ALIEN_SCORE

        # Check collisions with player
        for enemy in enemies[:]:
            if spaceship_rect.colliderect(enemy["rect"]):
                explosions.append({"rect": spaceship_rect.copy(), "timer": EXPLOSION_DURATION})
                explosion_sound.play()
                game_over = True
        for enemy_bullet in enemy_bullets[:]:
            if spaceship_rect.colliderect(enemy_bullet):
                explosions.append({"rect": spaceship_rect.copy(), "timer": EXPLOSION_DURATION})
                explosion_sound.play()
                game_over = True

        # Draw spaceship
        screen.blit(spaceship_img, spaceship_rect)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, GREEN, bullet)

        # Draw enemy bullets
        for enemy_bullet in enemy_bullets:
            pygame.draw.rect(screen, RED, enemy_bullet)

        # Draw enemies
        for enemy in enemies:
            if enemy["type"] == "alien":
                screen.blit(alien_img, enemy["rect"])
            else:
                screen.blit(asteroid_img, enemy["rect"])

        # Draw explosions
        for explosion in explosions[:]:
            color = EXPLOSION_COLORS[explosion["timer"] % len(EXPLOSION_COLORS)]
            pygame.draw.rect(screen, color, explosion["rect"].inflate(20, 20))
            explosion["timer"] -= 1
            if explosion["timer"] <= 0:
                explosions.remove(explosion)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        # Update top score
        if score > top_score:
            top_score = score

        # Display Game Over with score and top score
        game_over_text = large_font.render("GAME OVER!", True, WHITE)
        restart_text = font.render("Press R to Restart", True, WHITE)
        final_score_text = font.render(f"Your Score: {score}", True, YELLOW)
        top_score_text = font.render(f"Top Score: {top_score}", True, ORANGE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 300))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 300))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25))
        screen.blit(top_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 25))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game state
            enemies.clear()
            enemy_bullets.clear()
            bullets.clear()
            explosions.clear()
            score = 0
            spaceship_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
            game_over = False

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

pygame.quit()