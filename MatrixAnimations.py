from LinearAlgebra import Matrix

import math
import pygame
import sys


class Transformation:
    def __init__(self, numbers):
        self.numbers = [float(x) for x in numbers]

    def set_start_coordinates(self, start_i_coordinates, start_j_coordinates):
        self.start_i_coordinates = start_i_coordinates
        self.start_i_angle = math.atan2(start_i_coordinates[1], start_i_coordinates[0])
        self.start_i_magnitude = math.sqrt(start_i_coordinates[0] ** 2 + start_i_coordinates[1] ** 2)

        self.start_j_coordinates = start_j_coordinates
        self.start_j_angle = math.atan2(start_j_coordinates[1], start_j_coordinates[0])
        self.start_j_magnitude = math.sqrt(start_j_coordinates[0] ** 2 + start_j_coordinates[1] ** 2)


        self.target_i_coordinates = self.numbers[0] * start_i_coordinates[0] + self.numbers[2] * start_i_coordinates[1], \
                                    self.numbers[1] * start_i_coordinates[0] + self.numbers[3] * start_i_coordinates[1]
        self.target_i_angle = math.atan2(self.target_i_coordinates[1], self.target_i_coordinates[0])
        self.target_i_magnitude = math.sqrt(self.target_i_coordinates[0] ** 2 + self.target_i_coordinates[1] ** 2)

        self.target_j_coordinates = self.numbers[0] * start_j_coordinates[0] + self.numbers[2] * start_j_coordinates[1], \
                                    self.numbers[1] * start_j_coordinates[0] + self.numbers[3] * start_j_coordinates[1]
        self.target_j_angle = math.atan2(self.target_j_coordinates[1], self.target_j_coordinates[0])
        self.target_j_magnitude = math.sqrt(self.target_j_coordinates[0] ** 2 + self.target_j_coordinates[1] ** 2)

    def get_basis_positions(self, duration_fraction, as_line):
        if as_line:
            return (
                self.start_i_coordinates[0] + duration_fraction * (self.target_i_coordinates[0] - self.start_i_coordinates[0]),
                self.start_i_coordinates[1] + duration_fraction * (self.target_i_coordinates[1] - self.start_i_coordinates[1])
                   ), (
                self.start_j_coordinates[0] + duration_fraction * (self.target_j_coordinates[0] - self.start_j_coordinates[0]),
                self.start_j_coordinates[1] + duration_fraction * (self.target_j_coordinates[1] - self.start_j_coordinates[1])
            )
        delta = (self.target_i_angle - self.start_i_angle + 2 * math.pi) % (2 * math.pi)
        if delta > math.pi:
            delta -= 2 * math.pi
        current_i_angle = self.start_i_angle + delta * duration_fraction
        current_i_magnitude = self.start_i_magnitude + (self.target_i_magnitude - self.start_i_magnitude) * duration_fraction

        delta = (self.target_j_angle - self.start_j_angle + 2 * math.pi) % (2 * math.pi)
        if delta > math.pi:
            delta -= 2 * math.pi
        current_j_angle = self.start_j_angle + delta * duration_fraction
        current_j_magnitude = self.start_j_magnitude + (self.target_j_magnitude - self.start_j_magnitude) * duration_fraction
        return (current_i_magnitude * math.cos(current_i_angle), current_i_magnitude * math.sin(current_i_angle)),\
            (current_j_magnitude * math.cos(current_j_angle), current_j_magnitude * math.sin(current_j_angle))


pygame.init()
window_width = 800
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Matrix Animations")
clock = pygame.time.Clock()
frame_rate = 30

origin = (window_width / 2, window_height / 2)
shown_x = 12
shown_y = 12
pixels_per_unit = window_height / shown_y

#       R   G   B
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (52, 131, 235)
LIGHT_GREEN = (52, 235, 97)
LIGHT_RED = (212, 65, 49)
LIGHT_GRAY = (100, 100, 100)
PINK = (255, 192, 203)

background_color = BLACK
og_axes_color = (0, 0, 255)
og_grid_color = LIGHT_GRAY
transformed_axes_color = WHITE
tranformed_grid_color = LIGHT_BLUE
i_hat_color = LIGHT_GREEN
j_hat_color = LIGHT_RED
determinant_color = PINK
vector_color = YELLOW

current_i_hat_location = (1, 0)
current_j_hat_location = (0, 1)

with open("MatrixAnimationsParameters.txt", "r") as file:
    lines = file.readlines()
    arrow_width = float(lines[0].split(":")[1].strip()) # length of hypotenuse of an arrow
    delay = float(lines[1].split(":")[1].strip())
    duration = float(lines[2].split(":")[1].strip())
    display_as_vectors = lines[3].split(":")[1].strip() == "v"
    line_interpolation = lines[4].split(":")[1].strip() == "xy"
    show_determinant = "y" in lines[5].split(":")[1].strip()
    show_eigenvectors = "y" in lines[6].split(":")[1]
    matrices = lines[8].split(":")[1].strip().split(" ")
    vectors = lines[9].split(":")[1].strip().split(" ")

if vectors == ['']:
    vectors = []

ticks_per_matrix = int(duration * frame_rate)
total_ticks = len(matrices) * ticks_per_matrix
ticks_passed = 0

transformations = []
start = ((1, 0), (0, 1))
for i, matrix in enumerate(matrices):
    transform = Transformation(matrix.split(","))
    transformations.append(transform)
    transform.set_start_coordinates(start[0], start[1])
    start = [(transform.target_i_coordinates[0], transform.target_i_coordinates[1]),
             (transform.target_j_coordinates[0], transform.target_j_coordinates[1])]
    if show_eigenvectors:
        try:
            (a, b, c, d) = transform.numbers
            vectors.append("1," + str(
                ((d - a) - math.sqrt(((a - d) ** 2) + 4 * b * c)) / 2 / c
            ))
            vectors.append("1," + str(
                ((d - a) + math.sqrt(((a - d) ** 2) + 4 * b * c)) / 2 / c
            ))
        except ZeroDivisionError as error:
            print("No eigenvectors!")

'''target_i_hat_location = float(matrix_coordinates[0]), float(matrix_coordinates[1])
target_i_hat_angle = math.atan2(target_i_hat_location[1], target_i_hat_location[0])
target_i_hat_magnitude = math.sqrt(target_i_hat_location[0] ** 2 + target_i_hat_location[1] ** 2)

target_j_hat_location = float(matrix_coordinates[2]), float(matrix_coordinates[3])
target_j_hat_angle = math.atan2(target_j_hat_location[1], target_j_hat_location[0])
target_j_hat_magnitude = math.sqrt(target_j_hat_location[0] ** 2 + target_j_hat_location[1] ** 2)'''


def get_arrow_coordinates(end_coordinates, angle): # takes angle in radians
    offset = math.pi * 5 / 6
    return (end_coordinates[0] + arrow_width * math.cos(angle - offset), end_coordinates[1] - arrow_width * math.sin(angle - offset)), \
           (end_coordinates[0] + arrow_width * math.cos(angle + offset), end_coordinates[1] - arrow_width * math.sin(angle + offset)), end_coordinates


def normalize(x_coordinate, y_coordinate): # ensure these coordinates are within the screen and fill the whole screen
    if x_coordinate == 0:
        return 0, -shown_y / 2
    x_coordinate, y_coordinate = -shown_x / 2, -y_coordinate * shown_x / 2 / x_coordinate
    '''if y_coordinate < -shown_y / 2:
        x_coordinate, y_coordinate = x_coordinate * shown_y / 2 / y_coordinate, -shown_y / 2
    elif y_coordinate > shown_y / 2:
        x_coordinate, y_coordinate = x_coordinate * shown_y / 2 / y_coordinate, shown_y / 2'''
    return x_coordinate, y_coordinate


def put_og_space(window):
    for i in range(shown_x): # vertical lines
        pygame.draw.line(window, og_axes_color if i == shown_x / 2 else og_grid_color, (int(origin[0] + (i - shown_x / 2) * pixels_per_unit), 0),
                         (int(origin[0] + (i - shown_x / 2) * pixels_per_unit), window_height))

    for i in range(shown_y): # horizontal lines
        pygame.draw.line(window, og_axes_color if i == shown_x / 2 else og_grid_color, (0, int(origin[1]  + (i - shown_y / 2) * pixels_per_unit)),
                         (window_width, int(origin[1] + (i - shown_y / 2) * pixels_per_unit)))


def put_new_space(window, i_hat_coordinates, j_hat_coordinates):

    transformation = Matrix([i_hat_coordinates, j_hat_coordinates])

    for i in range(shown_x): # vertical lines
        image1, image2 = Matrix([[i - shown_x / 2, -shown_y * 3]]) * transformation, Matrix([[i - shown_x / 2, shown_y * 3]]) * transformation
        x_start, y_start = origin[0] + image1.numbers[0][0] * pixels_per_unit, origin[1] - image1.numbers[0][1] * pixels_per_unit

        x_end, y_end = origin[0] + image2.numbers[0][0] * pixels_per_unit, origin[1] - image2.numbers[0][1] * pixels_per_unit
        pygame.draw.line(window, tranformed_grid_color, (x_start, y_start), (x_end, y_end))

    for i in range(shown_y): # horizontal lines
        image1, image2 = Matrix([[-shown_x * 3, i - shown_y / 2]]) * transformation, Matrix([[shown_x * 3, i - shown_y / 2]]) * transformation
        x_start, y_start = origin[0] + image1.numbers[0][0] * pixels_per_unit, origin[1] - image1.numbers[0][1] * pixels_per_unit

        x_end, y_end = origin[0] + image2.numbers[0][0] * pixels_per_unit, origin[1] - image2.numbers[0][1] * pixels_per_unit
        pygame.draw.line(window, tranformed_grid_color, (x_start, y_start), (x_end, y_end))

    x_start, y_start = normalize(i_hat_coordinates[0], i_hat_coordinates[1])
    x_start = origin[0] + x_start * pixels_per_unit
    y_start = origin[1] - y_start * pixels_per_unit
    pygame.draw.line(window, transformed_axes_color, (x_start, y_start),
                     (window_width - x_start, window_height - y_start))  # new x-axis

    x_start, y_start = normalize(j_hat_coordinates[0], j_hat_coordinates[1])
    x_start = origin[0] + x_start * pixels_per_unit
    y_start = origin[1] - y_start * pixels_per_unit

    pygame.draw.line(window, transformed_axes_color, (x_start, y_start),
                     (window_width - x_start, window_height - y_start))  # new y-axis

    # i-hat
    i_hat_grid_coordinates = origin[0] + i_hat_coordinates[0] * pixels_per_unit, origin[1] - i_hat_coordinates[1] * pixels_per_unit

    # j-hat
    j_hat_grid_coordinates = origin[0] + j_hat_coordinates[0] * pixels_per_unit, origin[1] - j_hat_coordinates[1] * pixels_per_unit

    if show_determinant:
        pygame.draw.polygon(window, determinant_color, (origin, i_hat_grid_coordinates, (origin[0] + pixels_per_unit *
                                        (i_hat_coordinates[0] + j_hat_coordinates[0]), origin[1] - pixels_per_unit *
                                                (i_hat_coordinates[1] + j_hat_coordinates[1])), j_hat_grid_coordinates))
    if display_as_vectors:
        pygame.draw.line(window, i_hat_color, origin, i_hat_grid_coordinates)
        pygame.draw.polygon(window, i_hat_color, get_arrow_coordinates(i_hat_grid_coordinates, math.atan2(i_hat_coordinates[1], i_hat_coordinates[0])))
        pygame.draw.line(window, j_hat_color, origin, j_hat_grid_coordinates)
        pygame.draw.polygon(window, j_hat_color, get_arrow_coordinates(j_hat_grid_coordinates, math.atan2(j_hat_coordinates[1], j_hat_coordinates[0])))
    else:
        pygame.draw.circle(window, i_hat_color, i_hat_grid_coordinates, arrow_width)
        pygame.draw.circle(window, j_hat_color, j_hat_grid_coordinates, arrow_width)
    for vector in vectors:
        vector = [float(x) for x in vector.split(",")]
        coordinates = (
            origin[0] + (i_hat_coordinates[0] * vector[0] + j_hat_coordinates[0] * vector[1]) * pixels_per_unit,
            origin[1] - (i_hat_coordinates[1] * vector[0] + j_hat_coordinates[1] * vector[1]) * pixels_per_unit
        )
        if display_as_vectors:
            pygame.draw.line(window, vector_color, origin, coordinates)
            pygame.draw.polygon(window, vector_color, get_arrow_coordinates(coordinates, math.atan2(
                (i_hat_coordinates[1] * vector[0] + j_hat_coordinates[1] * vector[1]),
                i_hat_coordinates[0] * vector[0] + j_hat_coordinates[0] * vector[1])))
        else:
            pygame.draw.circle(window, vector_color, coordinates, arrow_width)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill(background_color)
    put_og_space(window)
    if ticks_passed < total_ticks:
        '''i_angle = target_i_hat_angle * ticks_passed / ticks
        i_magnitude = (target_i_hat_magnitude - 1) * ticks_passed / ticks + 1
        j_angle = math.pi / 2 + (target_j_hat_angle - math.pi / 2) * ticks_passed / ticks
        j_magnitude = (target_j_hat_magnitude - 1) * ticks_passed / ticks + 1

        current_i_hat_location = i_magnitude * math.cos(i_angle), i_magnitude * math.sin(i_angle)
        current_j_hat_location = j_magnitude * math.cos(j_angle), j_magnitude * math.sin(j_angle)'''
        current_i_hat_location, current_j_hat_location = transformations[ticks_passed // ticks_per_matrix].get_basis_positions(float(ticks_passed % ticks_per_matrix) / ticks_per_matrix, line_interpolation)
        ticks_passed += 1
    else:
        current_i_hat_location, current_j_hat_location = transformations[-1].target_i_coordinates, transformations[-1].target_j_coordinates

    put_new_space(window, current_i_hat_location, current_j_hat_location)

    pygame.display.update()

    clock.tick(frame_rate)