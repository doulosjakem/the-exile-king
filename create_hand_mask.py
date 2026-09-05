import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os
import shutil

def create_hand_mask(image_path, output_mask_path, model_path="D:/the-exile-king/models/hand_landmarker.task"):
    """Detect hands in image and create a mask covering the hand area."""
    
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image at {image_path}")
        return False
    
    h, w, _ = image.shape
    
    # Initialize MediaPipe HandLandmarker
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    detector = vision.HandLandmarker.create_from_options(options)
    
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    
    # Detect hands
    results = detector.detect(mp_image)
    
    # Create blank mask
    mask = np.zeros((h, w), dtype=np.uint8)
    
    if results.hand_world_landmarks or results.hand_landmarks:
        num_hands = len(results.hand_landmarks) if results.hand_landmarks else 0
        print(f"Found {num_hands} hand(s)")
        
        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                points = []
                for landmark in hand_landmarks:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    points.append((x, y))
                
                points = np.array(points, dtype=np.int32)
                
                # Create convex hull for the hand
                hull = cv2.convexHull(points)
                
                # Draw filled convex hull on mask
                cv2.fillConvexPoly(mask, hull, 255)
                
                # Draw connections between landmarks
                connections = vision.HandLandmarksConnections.HAND_CONNECTIONS
                for conn in connections:
                    pt1 = points[conn[0]]
                    pt2 = points[conn[1]]
                    cv2.line(mask, pt1, pt2, 255, thickness=2)
                
                # Fill small gaps
                for pt in points:
                    cv2.circle(mask, pt, 8, 255, -1)
        
        # Dilate mask slightly
        kernel = np.ones((15, 15), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        
    else:
        print("No hands detected")
        # Fallback: create a rough mask in the center-bottom area where hands typically are
        mask_lower = int(h * 0.5)
        mask_upper = int(h * 0.9)
        mask_left = int(w * 0.2)
        mask_right = int(w * 0.8)
        mask[mask_lower:mask_upper, mask_left:mask_right] = 255
    
    detector.close()
    
    # Save mask
    os.makedirs(os.path.dirname(output_mask_path), exist_ok=True)
    cv2.imwrite(output_mask_path, mask)
    print(f"Mask saved to: {output_mask_path}")
    
    # Return stats
    nonzero_pixels = np.count_nonzero(mask)
    total_pixels = h * w
    pct = nonzero_pixels / total_pixels * 100
    print(f"Mask stats: {nonzero_pixels} pixels = {pct:.1f}% coverage")
    
    return True

if __name__ == "__main__":
    image_path = "D:/the-exile-king/art/test/test_hand_image.png"
    mask_path = "D:/the-exile-king/art/test/test_hand_mask.png"
    
    if os.path.exists(image_path):
        print(f"Input image: {image_path}")
        success = create_hand_mask(image_path, mask_path)
        if success:
            print("Mask creation successful!")
        else:
            print("Mask creation failed!")
    else:
        print(f"Image not found: {image_path}")
