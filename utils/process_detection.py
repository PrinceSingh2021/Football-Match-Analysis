from utils.draw_bbox import draw_bbox

def get_class_name(class_id):
    class_names = {
        0: "ball",
        1: "goalkeeper",
        2: "player",
        3: "referee"
    }
    return class_names.get(class_id, "Unknown")

def get_class_color(c_id):
    color_map = {
        0: (0, 255, 255),    # Yellow (ball)
        1: (255, 0, 0),      # Blue (goalkeeper)
        2: (0, 255, 0),      # Green (player)
        3: (0, 0, 255)       # Red (referee)
    }
    return color_map.get(c_id, (255, 255, 255))

def process_detection(model, frame):
    detections = []

    results = model.predict(frame, verbose=False)[0]
    for box in results.boxes:
        x1, y1, x2, y2 = (int(x) for x in box.xyxy[0][:4])
        score = float(box.conf[0])
        cls = int(box.cls[0])
        if score > 0.50:
            detections.append([x1, y1, x2, y2, score, cls])

    return detections

def process_tracker(frame, trackers, team_assigner=None, speed_calculator=None):
    for tracker in trackers:
        x1, y1, x2, y2, track_id, class_id = map(int, tracker[:6])
        
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        if speed_calculator:
            speed = speed_calculator.update(track_id, (center_x, center_y))
            slabel = f"{speed:.1f}km/h"
        else:
            speed = 0

        if class_id == 2:
            player_color = team_assigner.get_player_color(frame, (x1, y1, x2, y2))
        else:
            player_color = get_class_color(class_id)
        
        draw_bbox(frame, x1, y1, x2, y2, track_id, slabel, player_color)
