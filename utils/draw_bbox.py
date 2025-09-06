# import cv2 as cv

# def draw_bbox(frame, x1, y1, x2, y2, label, color):
#     cv.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#     cv.putText(frame, str(label), (x1 + 5, y1 - 10), 
#                cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)


# import cv2 as cv

# def draw_bbox(frame, x1, y1, x2, y2, label, color):
#     # Calculate bottom center point of the bounding box
#     center_x = (x1 + x2) // 2
#     center_y = y2
    
#     # Calculate radius (you can adjust this based on your needs)
#     radius = min((x2 - x1) // 4, (y2 - y1) // 4)
    
#     # Draw circle at the bottom center
#     cv.circle(frame, (center_x, center_y), radius, color, 2)
    
#     # Draw label above the circle
#     cv.putText(frame, str(label), (center_x - 10, center_y - radius - 10), 
#                cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

import cv2 
import numpy as np

# def draw_bbox(frame, x1, y1, x2, y2, label, color):
   
#     center_x = (x1 + x2) // 2
#     center_y = y2
#     radius = min((x2 - x1) // 2, (y2 - y1) // 4)
    
#     cv.ellipse(
#         frame,
#         (center_x, center_y),
#         (radius, radius),
#         0,  
#         0,
#         180,
#         color,
#         2,
#     )
    
#     text_x = center_x - 10
#     text_y = center_y - radius // 2 
    
#     cv.putText(
#         frame,
#         str(label),
#         (text_x, text_y),
#         cv.FONT_HERSHEY_SIMPLEX,
#         0.7,
#         (255, 255, 255),
#         2,
#     )

def draw_bbox(frame, x1, y1, x2, y2, label, speed, color):
    # Calculate center and width
    x_center = (x1 + x2) // 2
    y_bottom = y2
    width = x2 - x1
    
    # Draw the ellipse
    cv2.ellipse(
        frame,
        center=(x_center, y_bottom),
        axes=(int(width), int(0.35 * width)),  # Width and height of ellipse
        angle=0.0,
        startAngle=-45,
        endAngle=235,
        color=color,
        thickness=2,
        lineType=cv2.LINE_4
    )
    
    # Draw the ID rectangle
    rectangle_width = 40
    rectangle_height = 20
    x1_rect = x_center - rectangle_width // 2
    x2_rect = x_center + rectangle_width // 2
    y1_rect = (y_bottom - rectangle_height // 2) + 15  # 15 pixels above bottom
    y2_rect = (y_bottom + rectangle_height // 2) + 15
    
    # Draw filled rectangle
    cv2.rectangle(
        frame,
        (int(x1_rect), int(y1_rect)),
        (int(x2_rect), int(y2_rect)),
        color,
        cv2.FILLED
    )
    
    # Position the text inside the rectangle
    x_text = x1_rect + 12
    if int(label) > 99:  # Adjust for 3-digit IDs
        x_text -= 10
    
    cv2.putText(
        frame,
        str(label),
        (int(x_text), int(y1_rect + 15)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 0),  # Black text
        2
    )

 # Draw full label (with speed) above the rectangle
    cv2.putText(
        frame,
        str(speed),
        (int(x_center - 20), int(y1_rect - 5)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        2
    )