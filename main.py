import pygame, math

pygame.init()

WIDTH = 600
HEIGHT = 600
FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe 3D")

def main():
    clock = pygame.time.Clock()

    points = [
        [-1,-1,1],
        [1,-1,1],
        [1,-1,-1],
        [-1,-1,-1],
        [-1,1,1],
        [1,1,1],
        [1,1,-1],
        [-1,1,-1],
    ]
    lines = [
        [0,1],
        [1,2],
        [2,3],
        [3,0],

        [4,5],
        [5,6],
        [6,7],
        [7,4],

        [0,4],
        [1,5],
        [2,6],
        [3,7],
    ]
    faces = [
        [1,0,2],
        [1,5,0],
        [1,2,5],
        [2,0,5]
    ]
    offset = [0,0,5]
    rotation : list[float]= [0.0,0.0,0.0]

    running = True

    while running:
        delta_time = clock.tick(FPS) / 1000.0

        # Handle Pygame Events
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False

        # Apply rotation to base points, preventing compoinding floaing point errors
        rotation[2] = set_angle(rotation[2] + math.pi * 0.5 * delta_time) # 90 degree / second

        new_pts = [rotate_y(point, rotation[2]) for point in points]

        draw(new_pts, lines, faces, offset)

    pygame.quit()

def draw(points, lines, faces, offset):
    SCREEN.fill((0,0,0))

    screen_points = []
    for point in points:
        screen_points.append(plane_to_screen(point_to_plane(point, offset)))

    for p_screen in screen_points:
        pygame.draw.circle(SCREEN, (200, 200, 200), p_screen, 3)

    for line in lines:
        pygame.draw.line(SCREEN, (255, 255, 255), screen_points[line[0]], screen_points[line[1]], 1)

    face_depths = []
    for face in faces:

        # Calculate position of each vertes
        x0 = points[face[0]][0] + offset[0]
        x1 = points[face[1]][0] + offset[0]
        x2 = points[face[2]][0] + offset[0]

        y0 = points[face[0]][1] + offset[1]
        y1 = points[face[1]][1] + offset[1]
        y2 = points[face[2]][1] + offset[1]

        z0 = points[face[0]][2] + offset[2]
        z1 = points[face[1]][2] + offset[2]
        z2 = points[face[2]][2] + offset[2]

        # Average to find coordinate of center
        avg_x = (x0 + x1 + x2) / 3.0
        avg_y = (y0 + y1 + y2) / 3.0
        avg_z = (z0 + z1 + z2) / 3.0

        # Find distance from camera to prevent clipping issues caused by z depth
        m = length((avg_x, avg_y, avg_z))
        
        face_depths.append((m, face))

    # Sort faces from FARTHEST to CLOSEST (Descending order of Z depth)
    # reverse=True ensures large Z values (far away) are drawn first
    face_depths.sort(key=lambda item: item[0], reverse=True)

    # Draw Faces in sorted order
    for depth, face in face_depths:
        p0 = screen_points[face[0]]
        p1 = screen_points[face[1]]
        p2 = screen_points[face[2]]
        
        # Winding orientation color check
        winding = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])
        if winding > 0:
            color = (50, 120, 255)  # Blue = Front
        else:
            color = (255, 70, 70)   # Red = Back

        pygame.draw.polygon(SCREEN, color, (p0, p1, p2))

        # Optional: Draw wireframe edges around each face so they pop
        pygame.draw.polygon(SCREEN, (255, 255, 255), (p0, p1, p2), 1)

    pygame.display.update()

def point_to_plane(point, offset):
    """tysm Tsoding, not i see why y is up in godot..., i guess it cood be flipped easily"""
    x = point[0]+offset[0]
    y = point[1]+offset[1]
    z = point[2]+offset[2]

    # prevent divide by 0
    if z == 0:
        z += 0.001

    return (x / z, y / z)

def plane_to_screen(point):
    """Projects a plane coord (-1...1, -1...1) to a screen coordinate"""
    return ((point[0] + 1)/2*WIDTH,(1-(point[1] + 1)/2)*HEIGHT)


def rotate_x(point, angle_rad):
    """
    Rotates a 3D point counterclockwise around the Y-axis by a given angle in radians.
    """
    x, y, z = point
    
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Calculate the new Y and Z coordinates
    new_y = y * cos_a + z * sin_a
    new_z = -y * sin_a + z * cos_a
    
    # X remains unchanged during a X-axis rotation
    return (x, new_y, new_z)

def rotate_y(point, angle_rad):
    """
    Rotates a 3D point counterclockwise around the Y-axis by a given angle in radians.
    """
    x, y, z = point
    
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Calculate the new X and Z coordinates
    new_x = x * cos_a + z * sin_a
    new_z = -x * sin_a + z * cos_a
    
    # Y remains unchanged during a Y-axis rotation
    return (new_x, y, new_z)

def rotate_z(point, angle_rad):
    """
    Rotates a 3D point counterclockwise around the Z-axis by a given angle in radians.
    """
    x, y, z = point
    
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Calculate the new X and Y coordinates
    new_x = x * cos_a - y * sin_a
    new_y = x * sin_a + y * cos_a
    
    # Z remains unchanged during a Z-axis rotation
    return (new_x, new_y, z)

def length(vect):
    return math.sqrt(vect[0]**2 + vect[1]**2 + vect[2]**2)

def set_angle(angle: float) -> float:
    return angle % (2 * math.pi)

if __name__ == "__main__":
    main()