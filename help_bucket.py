#############################################################
# Module Name: Sugar Pop Help Bucket Module
# Project: Sugar Pop Program
# Date: Nov 17, 2024
# By: Sana I. Udokeong
# Description: The help bucket implementation of the sugar pop game
#############################################################


import pygame as pg
import pymunk
from pymunk import Vec2d
from settings import SCALE, HEIGHT, WIDTH
from math import sqrt
import sounds
import time

import static_item


class HelpBucket:
    """ 
    A movable bucket that can be used to collect and transport sugar, 
    with a few restrictions to keep it from making the game too easy.
    It should only be used in emergencies or you'll loose sugars that 
    will keep dropping while your're trying to empty it. It cannot go 
    back up once it goes down. I can also pick up trapped sugars on the way. 
    When you click enter, it releases the items into a bucket.
    To use it click "h" and it will appear.
    """
    def __init__(self, screen, space, x, y, width, height, needed_sugar):
        """
        Initialize the bucket with:
        - The ability to move with arrow keys.
        - Removes the bottom wall when the Enter key is pressed.
        (To avoid making the game too easy)
            - Explodes after 30 seconds.
            - It can only hold 30 sugars 
        
        :param space: The Pymunk space.
        :param x: X position of the bucket's center in Pygame coordinates.
        :param y: Y position of the bucket's top in Pygame coordinates.
        :param width: Width of the bucket in pixels.
        :param height: Height of the bucket in pixels.
        """
        self.snd = sounds.Sound()
        self.screen = screen
        self.space = space
        self.width = width / SCALE
        self.height = height / SCALE
        self.count = 0  # Counter for collected sugar grains
        self.needed_sugar = needed_sugar

        self.collected_sugars = []  # List to store collected (inside the bucket) sugar grains
        self.emptied = False

        wall_thickness = 0.2  # Thickness of the walls in physics units

        
        # Convert Pygame coordinates to Pymunk coordinates
        x_pymunk = x / SCALE
        y_pymunk = y / SCALE

        # Left wall
        left_wall_start = (x_pymunk - self.width / 2, y_pymunk - self.height / 2)
        left_wall_end = (x_pymunk - self.width / 2, y_pymunk + self.height / 2)
        self.left_wall = pymunk.Segment(space.static_body, left_wall_start, left_wall_end, wall_thickness)
        self.left_wall.friction = 0.5
        self.left_wall.elasticity = 0.5
        space.add(self.left_wall)

        # Right wall
        right_wall_start = (x_pymunk + self.width / 2, y_pymunk - self.height / 2)
        right_wall_end = (x_pymunk + self.width / 2, y_pymunk + self.height / 2)
        self.right_wall = pymunk.Segment(space.static_body, right_wall_start, right_wall_end, wall_thickness)
        self.right_wall.friction = 0.5
        self.right_wall.elasticity = 0.5
        space.add(self.right_wall)

        # Bottom wall (removable when the Enter key is pressed)
        bottom_wall_start = (x_pymunk - self.width / 2, y_pymunk - self.height / 2)
        bottom_wall_end = (x_pymunk + self.width / 2, y_pymunk - self.height / 2)
        self.bottom_wall = pymunk.Segment(space.static_body, bottom_wall_start, bottom_wall_end, wall_thickness)
        self.bottom_wall.friction = 0.5
        self.bottom_wall.elasticity = 0.5
        space.add(self.bottom_wall)

        # Coordinates for displaying bucket count
        self.x = x
        self.y = HEIGHT - y
        


        # Define bucket boundaries
        self.left_boundary = x - width / 2
        self.right_boundary = x + width / 2
        self.top_boundary = y - height / 2
        self.bottom_boundary = y + height / 2

        

        self.exploded = False  # Track if the bucket has exploded
        self.start_time = time.time()  # Start the timer to explode after 30 seconds
        self.explosion_triggered = False  # Flag to check if explosion is triggered


    def explode(self, grains):
        """Apply a radial force to all grains near the bucket and remove the bucket walls."""
        if self.exploded:
            return  # Prevent multiple explosions

        # Get the bucket's center position
        bucket_center_x = (self.left_wall.a[0] + self.right_wall.a[0]) / 2
        bucket_center_y = (self.left_wall.a[1] + self.left_wall.b[1]) / 2

        self.snd.play('explosion')  # Play a sound when the bucket explodes

        # Apply radial force to each grain
        for grain in grains:
            grain_pos = grain.body.position

            # Calculate the vector from the bucket center to the grain
            dx = grain_pos.x - bucket_center_x
            dy = grain_pos.y - bucket_center_y
            distance = sqrt(dx**2 + dy**2)

            if distance < 2:  # Only affect grains within a certain radius
                # Normalize the vector
                if distance > 0:
                    dx /= distance
                    dy /= distance

                # Apply a radial impulse (adjust magnitude as needed)
                impulse_magnitude = 20 / (distance + 0.1)  # Reduce force with distance
                impulse = (dx * impulse_magnitude, dy * impulse_magnitude)
                grain.body.apply_impulse_at_world_point(impulse, grain.body.position)

        # Remove the bucket walls (left, right, bottom)
        if self.emptied:
            self.space.remove(self.left_wall, self.right_wall)
        else: 
            self.space.remove(self.left_wall, self.right_wall, self.bottom_wall)

        self.exploded = True  # Mark the bucket as exploded

    def move(self, dx, dy):
        """Move the bucket with the arrow keys."""
        self.x += dx
        self.y += dy

        # Update the positions of the walls based on the new bucket position
        x_pymunk = self.x / SCALE
        y_pymunk = (HEIGHT - self.y) / SCALE


        # Update the position of each sugar grain relative to the bucket
        if not self.emptied:
            for grain in self.collected_sugars:
                grain_pos = grain.body.position
                # Create a new Vec2d to set the grain's position
                new_position = grain_pos + (dx, dy)
                grain.body.position = new_position
                # Check if the grain has gone outside the bucket after the move
                left_bound = self.left_wall.a[0]
                right_bound = self.right_wall.a[0]
                top_bound = self.left_wall.b[1]
                bottom_bound = self.bottom_wall.a[1]

                # If the grain is outside the bucket, move it back inside
                if new_position.x < left_bound:
                    new_position = Vec2d(left_bound, new_position.y)
                elif new_position.x > right_bound:
                    new_position = Vec2d(right_bound, new_position.y)

                if new_position.y > top_bound:
                    new_position = Vec2d(new_position.x, top_bound)
                elif new_position.y < bottom_bound:
                    new_position = Vec2d(new_position.x, bottom_bound)

                # Apply the corrected position back to the grain
                grain.body.position = new_position

        # Remove old walls
        if self.emptied:
            self.space.remove(self.left_wall, self.right_wall)
        else:
            self.space.remove(self.left_wall, self.right_wall, self.bottom_wall)

        # Recreate the walls at the new position
        wall_thickness = 0.2  # Wall thickness in Pymunk units

        # Left wall
        left_wall_start = (x_pymunk - self.width / 2, y_pymunk - self.height / 2)
        left_wall_end = (x_pymunk - self.width / 2, y_pymunk + self.height / 2)
        self.left_wall = pymunk.Segment(self.space.static_body, left_wall_start, left_wall_end, wall_thickness)
        self.left_wall.friction = 0.5
        self.left_wall.elasticity = 0.5
        self.space.add(self.left_wall)

        # Right wall
        right_wall_start = (x_pymunk + self.width / 2, y_pymunk - self.height / 2)
        right_wall_end = (x_pymunk + self.width / 2, y_pymunk + self.height / 2)
        self.right_wall = pymunk.Segment(self.space.static_body, right_wall_start, right_wall_end, wall_thickness)
        self.right_wall.friction = 0.5
        self.right_wall.elasticity = 0.5
        self.space.add(self.right_wall)

        # Bottom wall
        bottom_wall_start = (x_pymunk - self.width / 2, y_pymunk - self.height / 2)
        bottom_wall_end = (x_pymunk + self.width / 2, y_pymunk - self.height / 2)
        self.bottom_wall = pymunk.Segment(self.space.static_body, bottom_wall_start, bottom_wall_end, wall_thickness)
        self.bottom_wall.friction = 0.5
        self.bottom_wall.elasticity = 0.5
        if not self.emptied:
            self.space.add(self.bottom_wall)


    def count_reset(self):
        if not self.exploded:
            self.count = 0

    def collect(self, sugar_grain):
        """
        Check if a sugar grain is within the bucket bounds and, if so, increase the bucket's count.
        
        :param sugar_grain: The sugar grain to check.
        """
        if self.exploded:
            return  # Don't count grains if the bucket has exploded

        grain_pos = sugar_grain.body.position

        # Get bucket boundaries
        left = self.left_wall.a[0]
        right = self.right_wall.a[0]
        bottom = self.bottom_wall.a[1]
        top = self.left_wall.b[1]

        # Check if the grain's position is within the bucket's bounding box
        if left <= grain_pos.x <= right and bottom <= grain_pos.y <= top:
            if sugar_grain not in self.collected_sugars:
                self.count += 1  # Increase the sugar count
                self.snd.play('add_sugar')  # Play sound for sugar being added
                self.collected_sugars.append(sugar_grain)  # Store the collected sugar grain
                sugar_grain.body.velocity = (0, 0)  # Stop the grain's movement by setting its velocity to 0
                return True  # Indicate that the grain was collected

        return False  # Grain not collected


    def draw(self, screen):
        """Draw the bucket on the Pygame screen."""
        if self.exploded:
            return  # Don't draw if the bucket has exploded

        color = (144, 238, 144)  # Light green color

        # Helper function to convert Pymunk coordinates to Pygame coordinates
        def to_pygame(p):
            return int(p[0] * SCALE), int(HEIGHT - p[1] * SCALE)

        # Draw the bucket edges
        pg.draw.line(screen, color, to_pygame(self.left_wall.a), to_pygame(self.left_wall.b), 2)
        pg.draw.line(screen, color, to_pygame(self.right_wall.a), to_pygame(self.right_wall.b), 2)
        pg.draw.line(screen, color, to_pygame(self.bottom_wall.a), to_pygame(self.bottom_wall.b), 2)

    def reset(self, screen, space, x, y, width, height, needed_sugar):
        """
        Resets the bucket to its initial state, allowing a new one to be created after explosion.
        """
        # Reset the bucket's state to be like new:
        self.__init__(screen, space, x, y, width, height, needed_sugar)  # Reinitialize the bucket

        # Reset other states like `self.count`, `self.collected_sugars`, etc.
        self.count = 0  # Counter for collected sugar grains

        self.collected_sugars = []  # List to store collected (inside the bucket) sugar grains
        self.emptied = False

