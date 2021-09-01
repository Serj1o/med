import cv2 as cv
import numpy as np
from PIL import Image
import math
import time


def input_params() -> dict:
    """
    Function for data entry

    Returns:
         Parameter's dictionary
    """
    params = {'input': cv.imread(input("Enter input file's path: ")),
              'output': input("Enter output path: "),
              'xc': input("x = "),
              'yc': input("y = "),
              'delta_min': [int(elem) if elem.isdigit() else 0 for elem in
                            input("Enter color's delta_min like '[0-255] [0-255] [0-255]': ").split(" ")],
              'delta_max': [int(elem) if elem.isdigit() else 255 for elem in
                            input("Enter color's delta_max like '[0-255] [0-255] [0-255]': ").split(" ")],
              'color': [int(elem) if elem.isdigit() else 255 for elem in
                        input("Enter color like '[0-255] [0-255] [0-255]': ").split(" ")]
              }
    if params['xc'].isdigit():
        params['xc'] = int(params['xc'])
    else:
        params['xc'] = math.ceil(params['input'].shape[1] / 2)
    if params['yc'].isdigit():
        params['yc'] = int(params['yc'])
    else:
        params['yc'] = math.ceil(params['input'].shape[0] / 2)
    params['pixel'] = [params['xc'], [params['yc']]]
    return params


def create_start_mask(img: np.ndarray):
    mask = np.zeros(img.shape, dtype=int)
    return mask


def rec(img: np.ndarray, mask: np.ndarray, delta_min: int, delta_max: int, pixel: list):
    """
    Заполнение контура от начального пикселя в 4 стороны.
    """
    queue = [pixel]
    while queue:
        pixel = queue.pop()
        if sup_check(img, mask, delta_min, delta_max, [pixel[0] + 1, pixel[1]]):
            mask[pixel[1]][pixel[0] + 1] = 255
            queue.append([pixel[0] + 1, pixel[1]])
        if sup_check(img, mask, delta_min, delta_max, [pixel[0] - 1, pixel[1]]):
            mask[pixel[1]][pixel[0] - 1] = 255
            queue.append([pixel[0] - 1, pixel[1]])
        if sup_check(img, mask, delta_min, delta_max, [pixel[0], pixel[1] + 1]):
            mask[pixel[1] + 1][pixel[0]] = 255
            queue.append([pixel[0], pixel[1] + 1])
        if sup_check(img, mask, delta_min, delta_max, [pixel[0], pixel[1] - 1]):
            mask[pixel[1] - 1][pixel[0]] = 255
            queue.append([pixel[0], pixel[1] - 1])
    return np.uint8(mask)


def sup_check(img: np.ndarray, mask: np.ndarray, min_delta: int, max_delta: int, pixel: list):
    """
    Проверка пикселей.
    """
    if pixel[0] < 0 or pixel[0] >= img.shape[1]:
        return False
    if pixel[1] < 0 or pixel[1] >= img.shape[0]:
        return False
    if not min_delta <= img[pixel[1]][pixel[0]] <= max_delta:
        return False
    if mask[pixel[1]][pixel[0]] == 255:
        return False
    else:
        return True


def main():
    min_color = 110
    max_color = 135
    x = 328
    y = 250
    file_path = 'image_data/test_photo.bmp'
    out_path = 'outputs.bmp'
    img = cv.imread(file_path, 0)
    m = rec(img, create_start_mask(img), min_color, max_color, [x, y])
    Image.fromarray(m).save(out_path)


"""
Плохо справляется с большими областями заливки.
"""


if __name__ == '__main__':
    now = time.time()
    main()
    end = time.time()
    print(f"Время работы: {end - now}")
