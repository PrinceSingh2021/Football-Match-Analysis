import cv2 as cv
from ultralytics import YOLO
import numpy as np
from bytetracker import BYTETracker
from utils.process_detection import process_detection, process_tracker
from utils.team_assign import TeamAssigner
from utils.calculate_speed import SpeedCalculator

def run(video, model, team_assigner, speed_calculator):
    cap = cv.VideoCapture(video)

    while True:
        _, frame = cap.read()

        detections = process_detection(model, frame)

        if detections:
            trackers = byte_tracker.update(np.asarray(detections), frame)
        else:
            trackers = []

        players = [t for t in trackers if t[5] == 2]
        team_assigner.assign_team_color(frame, players)

        process_tracker(frame, trackers, team_assigner, speed_calculator)

        # cv.putText(frame, "goalkeeper", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2,)
        # cv.putText(frame, "player", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,)
        # cv.putText(frame, "referee", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,)

        cv.namedWindow("Video", cv.WINDOW_NORMAL)
        cv.imshow("Video", frame)

        if cv.waitKey(1) & 0xFF == ord("q"):
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    model_path = "models/best.pt"
    video_path = "videos/08fd33_4.mp4"
    model = YOLO(model_path)
    byte_tracker = BYTETracker(track_thresh=0.5, track_buffer=30, match_thresh=0.8, frame_rate=30)
    team_assigner = TeamAssigner()
    speed_calculator = SpeedCalculator()
    run(video_path, model, team_assigner, speed_calculator)
    