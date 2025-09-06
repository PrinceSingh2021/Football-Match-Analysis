from sklearn.cluster import KMeans
import cv2
import numpy as np 

class TeamAssigner:
    def __init__(self):
        self.team_colors = {}
        self.kmeans = None
    
    def get_clustering_model(self, image):
        image_2d = image.reshape(-1, 3)
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=1)
        kmeans.fit(image_2d)
        return kmeans

    def get_player_color(self, frame, bbox):
        x1, y1, x2, y2 = (int(x) for x in bbox)
        
        if x1 >= x2 or y1 >= y2:
            return (0, 0, 0)
        
        image = frame[y1:y2, x1:x2]
        
        jersey_area = image[0:int(image.shape[0]*0.4), :]
                
        kmeans = self.get_clustering_model(jersey_area)
        
        labels = kmeans.labels_
        clustered_image = labels.reshape(jersey_area.shape[0], jersey_area.shape[1])
        
        corner_clusters = [
            clustered_image[0, 0],
            clustered_image[0, -1],
            clustered_image[-1, 0],
            clustered_image[-1, -1]
        ]
        non_player_cluster = max(set(corner_clusters), key=corner_clusters.count)
        player_cluster = 1 - non_player_cluster
        
        lab_color = kmeans.cluster_centers_[player_cluster]
        return tuple(map(int, lab_color))

    def assign_team_color(self, frame, player_detections):
        if len(player_detections) < 2:
            return False
            
        player_colors = []
        for detection in player_detections:
            color = self.get_player_color(frame, detection[:4])
            if np.mean(color) > 10:
                player_colors.append(color)
        
        if len(player_colors) < 2:
            return False
        
        self.kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10)
        self.kmeans.fit(player_colors)
        
        self.team_colors[1] = tuple(map(int, self.kmeans.cluster_centers_[0]))
        self.team_colors[2] = tuple(map(int, self.kmeans.cluster_centers_[1]))
        return True