#############################################################
# Module Name: Sugar Pop value Display Module
# Project: Sugar Pop Program
# Date: Nov 17, 2024
# By: Brett W. Huffman
# Description: The value Display implementation of the sugar pop game
#############################################################
import pygame as pg
import time

class Display:
    def __init__(self, color=(255, 255, 255)):
        """
        Initialize the Display class.
        
        :param screen: The Pygame screen to display values on.
        :param font_name: The name of the font (default is None, which uses the default font).
        :param font_size: The size of the font.
        :param color: The color of the text (default is white).
        """
        
        self.color = color
        self.total_count = 0
        self.sugar_in_buckets = {}
        self.sugar_left = 0
        self.level_count = 0

    def show_value(self, text, duration):
        """
        Show a value on the screen for a given duration.
        
        :param text: The text to display.
        :param duration: The number of seconds to display the text.
        """
        self.info = text
        self.display_until = time.time() + duration

    def update_values(self, total_count, sugar_in_bucket, sugar_left, level_count):
        """
        Update the values displayed. 
        """
        self.total_count = total_count
        self.sugar_in_buckets = sugar_in_bucket
        self.sugar_left = sugar_left
        self.level_count = level_count

    def draw_total_count(self, screen, pos, font_name=None, font_size=36):
        """
        Draw the value on the screen, if there is an active value.
        """
        self.font = pg.font.SysFont(font_name, font_size)

        
        text_surface = self.font.render(("Total Sugar: " + str(self.total_count)), True, self.color)
        text_rect = text_surface.get_rect(topright =pos)
        screen.blit(text_surface, text_rect)

    def draw_sugar_left(self, screen, pos, font_name=None, font_size=36):
        """
        Draw the value on the screen, if there is an active value.
        """
        self.font = pg.font.SysFont(font_name, font_size)

        
        text_surface = self.font.render(("Sugar Left: " + str(self.sugar_left)), True, self.color)
        text_rect = text_surface.get_rect(topright=pos)
        screen.blit(text_surface, text_rect)

    def draw_level_count(self, screen, pos, font_name=None, font_size=36):
        """
        Draw the value on the screen, if there is an active value.
        """
        self.font = pg.font.SysFont(font_name, font_size)

        
        text_surface = self.font.render((" Level: " + str(self.level_count)), True, self.color)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

    def draw_sugar_in_bucket(self, screen, font_name=None, font_size=36):
        """
        Draw the value on the screen, if there is an active value.
        """
        self.font = pg.font.SysFont(font_name, font_size)
        if len(self.sugar_in_buckets) > 0:
            for i, bucket  in self.sugar_in_buckets.items():
                if not bucket[2]:
                    text_surface = self.font.render(str(bucket[0]), True, self.color)
                    text_rect = text_surface.get_rect(center=bucket[1])
                    screen.blit(text_surface, text_rect)

    def draw_sugar_in_help_bucket(self, screen, hb, font_name=None, font_size=36):
        """
        Draw the value on the screen, if there is an active value.
        """
        self.font = pg.font.SysFont(font_name, font_size)
        if not hb.exploded:
            text_surface = self.font.render(str(hb.count), True, self.color)
            text_rect = text_surface.get_rect(center=(hb.x, hb.y))
            screen.blit(text_surface, text_rect)

    def draw_gravity_direction(self, screen, grav, start_pos=(270, 30)):
        """
        Draws an arrow showing the direction of gravity on the screen.

        :param screen: The Pygame screen where the arrow will be drawn.
        :param space: The pymunk space object which holds gravity information.
        :param start_pos: The starting point of the arrow on the screen (default is (50, 50)).
        """
        # Get the gravity vector from pymunk space
        self.gravity = grav  # This is a tuple (x, y)
        
        # Convert pymunk gravity coordinates to pygame coordinates (invert Y-axis)
        self.gravity_pygame = (self.gravity[0], -self.gravity[1])  # Invert Y for Pygame's coordinate system
        
        # Set the arrow color
        arrow_color = (255, 0, 0)  # Red color for gravity arrow
        
        # Text
        self.font = pg.font.SysFont(None, 36)
        text_surface = self.font.render("Gravity: ", True, self.color)
        text_rect = text_surface.get_rect(center=(200, 30))
        screen.blit(text_surface, text_rect)

        # Draw a line representing the gravity direction
        self.end_pos = (start_pos[0] + self.gravity_pygame[0], start_pos[1] + self.gravity_pygame[1])
        pg.draw.line(screen, arrow_color, start_pos, self.end_pos, 7)
        
        # Draw an arrowhead to indicate the direction more clearly
        arrowhead_length = 10
        arrowhead_angle = 30  # Angle for the arrowhead
        dx = self.gravity_pygame[0]
        dy = self.gravity_pygame[1]

        # Normalize the gravity vector to get a consistent arrow size
        magnitude = (dx**2 + dy**2)**0.5
        dx /= magnitude
        dy /= magnitude
        
        # Calculate the points for the arrowhead
        arrowhead_left = (self.end_pos[0] - arrowhead_length * (dx * 0.5 + dy * 0.866), 
                        self.end_pos[1] - arrowhead_length * (dy * 0.5 - dx * 0.866))
        arrowhead_right = (self.end_pos[0] - arrowhead_length * (dx * 0.5 - dy * 0.866), 
                        self.end_pos[1] - arrowhead_length * (dy * 0.5 + dx * 0.866))

        # Draw the arrowhead
        pg.draw.polygon(screen, arrow_color, [self.end_pos, arrowhead_left, arrowhead_right])


    
            
            