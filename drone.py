import os, cv2
import numpy as np

def get_mask(thermal_frame):
    b, g, r = cv2.split(thermal_frame)

    g = g.astype(np.int16)
    b = b.astype(np.int16)
    r = r.astype(np.int16)

    mask1, mask2 = g - r, b - g
    t1_mask1 = mask1 > 20
    t2_mask1 = mask2 > 20
    mask = np.bitwise_or(np.array(t1_mask1), np.array(t2_mask1)).astype(np.uint8) * 255

    kernel = np.ones((31, 31), np.uint8)
    closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return closed_mask

def get_correct_contours(mask):
    (h, w) = mask.shape
    # cv2.imshow('mask', mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    if len(contours) != 0:
        for contour in contours:
            x, y, ww, hh = cv2.boundingRect(contour)
            if x < w // 7 or x > w // 7 * 6: continue
            if y < h // 7 or y > h // 7 * 6: continue
            
            centers.append([w + x + ww // 2, y + hh // 2])
    print(centers)
    return centers

def _main():
    video_path = "2.mp4"
    vid = cv2.VideoCapture(video_path)

    ret, frame = vid.read()
    i = 0
    while ret:
        (h, w, _) = frame.shape
        i += 1
        colored_frame = frame[0: h, 0 :w // 2]
        thermal_frame = frame[0: h, w // 2: w]

        mask = get_mask(thermal_frame)
        centers = get_correct_contours(mask)
        
        for center in centers:
            cv2.circle(img=frame, center=center, radius=3, thickness=6, color=[255, 0, 0])

        # if i > 2000:
        # cv2.imshow('mask', mask)
        # cv2.imshow('b_r', g)
        # cv2.imshow('colored_frame', colored_frame)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

        ret, frame = vid.read()

    return

if __name__ == "__main__":
    _main()