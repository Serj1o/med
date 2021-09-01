from copy import deepcopy

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
    Заливка от начального пиксела впаво и влево.
    """
    queue = [pixel]
    while queue:
        pixel = queue.pop(0)
        if not check_in_mask(mask[pixel[1]][pixel[0]], 255):
            if check_color(img[pixel[1]][pixel[0] + 1], delta_min, delta_max):
                right(img, mask, delta_min, delta_max, pixel, queue)
            if check_color(img[pixel[1]][pixel[0] - 1], delta_min, delta_max):
                left(img, mask, delta_min, delta_max, pixel, queue)
    return mask


def left(img_arr: np.ndarray, mask: np.ndarray, delta_min: int, delta_max: int, pixel: list, queue: list):
    """
    Движение влево.
    """
    _pixel = deepcopy(pixel)
    while check_color(img_arr[_pixel[1]][_pixel[0]], delta_min, delta_max):
        if 0 <= _pixel[0] - 1:
            mask[_pixel[1]][_pixel[0]] = 255
            check_up_and_down_pixels(img_arr, delta_min, delta_max, _pixel, queue)
            _pixel[0] -= 1
        else:
            break
    _pixel[0] += 1
    if _pixel[1] + 1 < img_arr.shape[0]:
        if check_color(img_arr[_pixel[1] + 1][_pixel[0]], delta_min, delta_max):
            queue.append([_pixel[0], _pixel[1] + 1])
    if 0 <= _pixel[1] - 1:
        if check_color(img_arr[_pixel[1] - 1][_pixel[0]], delta_min, delta_max):
            queue.append([_pixel[0], _pixel[1] - 1])


def right(img_arr: np.ndarray, mask: np.ndarray, delta_min: int, delta_max: int, pixel: list, queue: list):
    """
    Движение вправо.
    """
    _pixel = deepcopy(pixel)
    while check_color(img_arr[_pixel[1]][_pixel[0]], delta_min, delta_max):
        if _pixel[0] + 1 < img_arr.shape[1]:
            mask[_pixel[1]][_pixel[0]] = 255
            check_up_and_down_pixels(img_arr, delta_min, delta_max, _pixel, queue)
            _pixel[0] += 1
        else:
            break
    _pixel[0] -= 1
    if _pixel[1] + 1 < img_arr.shape[0]:
        if check_color(img_arr[_pixel[1] + 1][_pixel[0]], delta_min, delta_max):
            queue.append([_pixel[0], _pixel[1] + 1])
    if 0 <= _pixel[1] - 1:
        if check_color(img_arr[_pixel[1] - 1][_pixel[0]], delta_min, delta_max):
            queue.append([_pixel[0], _pixel[1] - 1])


def check_up_and_down_pixels(img_arr: np.ndarray, delta_min: int, delta_max: int, pixel: list, queue: list):
    """
    Проверка пикселей над и создание "опорных" точек.
    """
    if pixel[1] + 1 < img_arr.shape[0]:
        if not check_color(img_arr[pixel[1] + 1][pixel[0]], delta_min, delta_max):
            if pixel[0] + 1 < img_arr.shape[1]:
                if check_color(img_arr[pixel[1] + 1][pixel[0] + 1], delta_min, delta_max):
                    queue.append([pixel[0] + 1, pixel[1] + 1])
            if 0 <= pixel[0] - 1:
                if check_color(img_arr[pixel[1] + 1][pixel[0] - 1], delta_min, delta_max):
                    queue.append([pixel[0] - 1, pixel[1] + 1])
    if 0 <= pixel[1] - 1:
        if not check_color(img_arr[pixel[1] - 1][pixel[0]], delta_min, delta_max):
            if pixel[0] + 1 < img_arr.shape[1]:
                if check_color(img_arr[pixel[1] - 1][pixel[0] + 1], delta_min, delta_max):
                    queue.append([pixel[0] + 1, pixel[1] - 1])
            if 0 <= pixel[0] - 1:
                if check_color(img_arr[pixel[1] - 1][pixel[0] - 1], delta_min, delta_max):
                    queue.append([pixel[0] - 1, pixel[1] - 1])


def check_color(a: int, min_delta: int, max_delta: int):
    """
    Проверка цвета пикселя изображения.
    """
    if min_delta <= a <= max_delta:
        return True
    else:
        return False


def check_in_mask(a: int, b: int):
    """
    Проверка закрашен ли пиксель в маске.
    """
    if a == b:
        return True
    else:
        return False


def main():
    min_color = 70
    max_color = 135
    x = 328
    y = 250
    file_path = 'image_data/test_photo.bmp'
    out_path = 'outputs.bmp'
    img = cv.imread(file_path, 0)
    Image.fromarray(rec(img,
                        create_start_mask(img),
                        min_color,
                        max_color, [x, y]).astype(np.uint8)).save(out_path)


"""
Довольно-таки хорошо справляется с большими областями заливки.
"""


if __name__ == '__main__':
    now = time.time()
    main()
    end = time.time()
    print(f"Время работы: {end - now}")
