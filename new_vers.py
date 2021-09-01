import cv2 as cv
import numpy as np
from PIL import Image
import math


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


def calculate_boarder(img, delta_min, delta_max) -> []:
    """
    Finds and calculates the contours of the desired objects

    Returns:
         2 data structures of the same content, [np.ndarray, dict]
    """
    hsv_min = np.array(delta_min, np.uint8)
    hsv_max = np.array(delta_max, np.uint8)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # меняем цветовую модель с BGR на HSV
    thresh = cv.inRange(hsv, hsv_min, hsv_max)  # применяем цветовой фильтр
    # ищем контуры и складируем их в переменную contours
    contours = [elem for elem
                in cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]
                if len(elem) >= 15]
    return contours


def create_pics(contours: list, image: np.ndarray, color=None) -> list:
    if not color:
        color = [255, 0, 0]
    pics_arr = []
    image_arr = []
    for i in range(len(contours)):
        image_arr.append(image.copy())
        pics_arr.append(cv.drawContours(image_arr[i], contours, i, color, -1, cv.LINE_AA, maxLevel=1))
    return pics_arr


def check_contour(pixel: list, pics_arr: list, color=None):
    if not color:
        color = [255, 0, 0]
    for image in pics_arr:
        if check_arrays(image[pixel[-1]][pixel[0]], color):
            return image
    return None


def check_arrays(a: np.ndarray, b: list):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        try:
            if type(a[i]) != int and type(b[i]) != int:
                if check_arrays(a[i], b[i]):
                    continue
                else:
                    return False
            elif a[i] == b[i]:
                return True
            else:
                return False
        except:
            return False


def painter(image: np.ndarray, color=None) -> np.ndarray:
    """
    Draws a new image with found areas

    Returns:
        np.ndarray
    """
    if not color:
        color = [255, 0, 0]
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y][x][0] != color[0]:
                image[y][x] = [0, 0, 0]
    return image


def main():
    inputs = {'input': cv.imread('image_data/test_photo.bmp'), 'output': 'output.bmp', 'delta_min': [0, 0, 106],
              'delta_max': [255, 255, 255], 'pixel': [76, 66]}
    #  inputs = input_params()
    contours = calculate_boarder(inputs['input'], inputs['delta_min'], inputs['delta_max'])
    pics_arr = create_pics(contours, inputs['input'])
    image = painter(check_contour(inputs['pixel'], pics_arr))
    Image.fromarray(image).save(inputs['output'])


if __name__ == '__main__':
    main()
