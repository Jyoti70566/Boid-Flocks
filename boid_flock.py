import pygame
import random
import math

WIDTH, HEIGHT = 800, 600

NUM_ENTITIES = 500
NUM_GROUPS = 8
MAX_SPEED = 8
PERCEPTION_RADIUS = 50

class Entity:
    def __init__(self, x, y, group):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(MAX_SPEED)
        self.group = group

    def update(self, flock):
        self.position += self.velocity
        self.wrap_edges()

        average_velocity = pygame.Vector2(0, 0)
        num_neighbors = 0

        for other in flock:
            if other == self or other.group != self.group:
                continue
            distance = self.distance_to(other)
            if distance < PERCEPTION_RADIUS:
                average_velocity += other.velocity
                num_neighbors += 1

        if num_neighbors > 0:
            average_velocity /= num_neighbors
            self.velocity = average_velocity
            self.velocity.scale_to_length(MAX_SPEED)

    def wrap_edges(self):
        if self.position.x < 0:
            self.position.x = WIDTH
        elif self.position.x > WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT:
            self.position.y = 0

    def distance_to(self, other):
        return math.sqrt((self.position.x - other.position.x)**2 + (self.position.y - other.position.y)**2)

NUM_GROUPS = 3
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

while len(colors) < NUM_GROUPS:
    new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    colors.append(new_color)

flock = []
for _ in range(NUM_ENTITIES):
    group = random.randint(0, NUM_GROUPS - 1)
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    flock.append(Entity(x, y, group))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Simulation - Multiple Groups")

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        for entity in flock:
            entity.update(flock)

            # Change from triangle to circle
            pygame.draw.polygon(screen, colors[entity.group], [
                (entity.position.x, entity.position.y - 5),
                (entity.position.x - 5, entity.position.y + 5),
                (entity.position.x + 5, entity.position.y + 5)
            ])
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

""" What happens if you change the order of 3 rules given above. What is the ”correct order”? Is it
possible to answer this question?
Answer - Changing the order of three rules - Separation, Alignment and Cohesion may affect the behaviour of birds flock in a subtle way 
for example If separation is applied first, boids may avoid collisions and spread out. Alignment and cohesion then act to give the flock a directional movement and group cohesion. 
If alignment is applied first, boids might align their directions, and then separation and cohesion can work to refine the overall flock structure.
Applying cohesion first might result in boids moving towards the center of mass, and then separation and alignment could refine the movement and orientation.
"""
""" What happens if birds can only see in front of them and what if they see all around?
Answer - Limited Field of Vision:Separation- Boids avoid collisions and nearby flockmates within their limited frontal view, leading to dynamic avoidance behaviors.
Alignment- Boids align their heading with neighbors in their frontal view, resulting in localized directional movement within the flock.
Cohesion- Boids move towards the center of mass of neighbors within their frontal view, leading to tighter local clustering.
360-Degree Field of Vision:Separation- Boids avoid collisions and respond to threats from all directions, resulting in smoother avoidance behaviors.
Alignment- Boids align their heading with the average heading of all neighbors, providing a more global sense of directionality for the entire flock.
Cohesion- Boids move towards the center of mass of all neighbors, contributing to a more balanced and cohesive overall flock structure.
"""

