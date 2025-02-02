import cv2
import numpy as np


def main():
    url = 'data/sample1.png'
    im = cv2.imread(url, cv2.IMREAD_GRAYSCALE)
    cells = extract_cells(im, 50)


def show(im, max_size=500, title='Show'):
    def calculate_size(shape):
        x, y, *_ = shape

        if x > max_size or y > max_size:
            if x > y:
                r = y / x
                x = max_size
                y = int(x * r)
            else:
                r = x / y
                y = max_size
                x = int(y * r)
        return x, y

    cv2.namedWindow(title)
    size = calculate_size(im.shape)
    im_s = cv2.resize(im, size)
    cv2.imshow(title, im_s)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def extract_cells(image, cell_size=50):
    blurred = cv2.GaussianBlur(image, (9, 9), 0)
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    peri = cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, 0.02 * peri, True)

    pts = np.float32([approx[0][0], approx[1][0], approx[2][0], approx[3][0]])
    pts = sorted(pts, key=lambda x: (x[1], x[0]))
    if pts[1][0] < pts[0][0]:
        pts[0], pts[1] = pts[1], pts[0]
    if pts[3][0] < pts[2][0]:
        pts[2], pts[3] = pts[3], pts[2]

    s = cell_size * 9

    rect = np.array([pts[0], pts[1], pts[3], pts[2]], dtype='float32')
    dst = np.array([[0, 0], [s, 0], [s, s], [0, s]], dtype='float32')

    matrix = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, matrix, (s, s))

    cells = []
    for i in range(9):
        for j in range(9):
            cell = warped[i * cell_size:(i + 1) * cell_size, j * cell_size:(j + 1) * cell_size]
            cells.append(cell)
    return cells


def show_cells(cells, cell_size, gap):
    size = 9 * cell_size + 10 * gap
    arr = np.zeros((size, size), dtype=np.uint8)

    for i, cell in enumerate(cells):
        ix, iy = i % 9, i // 9
        rx, ry = ix * (cell_size + gap) + gap, iy * (cell_size + gap) + gap

        arr[ry:ry+cell_size, rx:rx+cell_size] = cell
    show(arr)


def detect_empty(cell):
    def is_centered(binary_image, k):
        M = cv2.moments(binary_image)
        if M["m00"] == 0:
            return False
        cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        h, w = binary_image.shape
        center_x, center_y = w // 2, h // 2
        threshold = min(w, h) * k
        return abs(cx - center_x) < threshold and abs(cy - center_y) < threshold

    n = 8
    blurred = cv2.GaussianBlur(cell, (19, 19), 0)
    binarized = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    trimmed = binarized[n:50 - n, n:50 - n]

    if not is_centered(trimmed, 0.225):
        return True

    m = trimmed / 255
    if m.sum() / (50 - 2 * n) ** 2 < 0.15:
        return True

    return False


if __name__ == '__main__':
    main()
