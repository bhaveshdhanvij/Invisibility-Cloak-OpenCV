import cv2
import numpy as np
import time

def capture_background(cap, num_frames=60):
    """Capture the static background for invisibility effect."""
    print("Capturing background... Please stay out of frame.")
    time.sleep(3)
    for i in range(num_frames):
        ret, background = cap.read()
    background = np.flip(background, axis=1)
    return background

def create_red_mask(hsv_frame):
    """Create a mask for red color detection."""
    # Red color ranges in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)

    # Combine masks
    red_mask = mask1 + mask2

    # Morphological operations to remove noise
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8))
    return red_mask

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    background = capture_background(cap)

    # Optional: Define codec and create VideoWriter to save output
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('invisibility_output.avi', fourcc, 20.0, (640,480))

    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = create_red_mask(hsv)

        # Replace red area with background
        frame[np.where(mask == 255)] = background[np.where(mask == 255)]

        cv2.imshow("Invisibility Cloak", frame)
        # out.write(frame)  # Save frame to video if needed

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    # out.release()  # Release video writer if used
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
