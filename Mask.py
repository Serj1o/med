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


def create_mask(img: np.ndarray, xc: int, yc: int, delta_min: list, delta_max: list):
    """
    создает и возвращает маску
    """
    mask = np.empty([480, 640, 3], dtype=int)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            mask[yc][xc] = [0, 0, 0]
    for pixel in rec(img, delta_min, delta_max, [xc, yc]):
        mask[pixel[1]][pixel[0]] = [255, 255, 255]
    return mask


def rec(img: np.ndarray, delta_min: list, delta_max: list, pixel: list):
    """
    возвращает координаты области
    """
    response = []
    check_pixels = [pixel]
    checked_pixels = {}
    _checked_pixels = []
    while check_pixels:
        deep_copy_check_pixels = deepcopy(check_pixels)
        for pixel in deep_copy_check_pixels:
            if rec_sup(img, delta_min, delta_max, pixel):
                response.append(pixel)
                for x in range(pixel[0] - 1, pixel[0] + 2):
                    for y in range(pixel[1] - 1, pixel[1] + 2):
                        if x == pixel[0] and y == pixel[1]:
                            continue
                        if [x, y] not in check_pixels and x not in checked_pixels.get(y, []):
                            check_pixels.append([x, y])
            if checked_pixels.get(pixel[1]):
                checked_pixels[pixel[1]].append(pixel[0])
            else:
                checked_pixels[pixel[1]] = [pixel[0]]
            check_pixels.remove(pixel)
    return response


def rec_sup(img_arr: np.ndarray, delta_min: list, delta_max: list, pixel: list):
    """
    проверяет цвет пикселя по диапозону
    """
    if 0 <= pixel[0] < img_arr.shape[1] and 0 <= pixel[1] < img_arr.shape[0]:
        if delta_min[2] <= img_arr[pixel[1]][pixel[0]][2] <= delta_max[2]:
            return True
        else:
            return False
    else:
        return False


def main():
    min_color = [0, 0, 90]
    max_color = [255, 255, 150]
    x = 320
    y = 240
    file_path = 'image_data/test_photo.bmp'
    out_path = 'outputs.bmp'
    Image.fromarray(create_mask(cv.imread(file_path), x, y, min_color, max_color).astype(np.uint8)).save(out_path)


if __name__ == '__main__':
    now = time.time()
    main()
    end = time.time()
    print(f"Время работы: {end - now}")
