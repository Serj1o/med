import cv2 as cv
import pandas as pd
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
              'delta': int(input("Enter the amount of spread: ")),
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
    return params


def create_circle(arr: np.ndarray, delta: int, xc: int, yc: int) -> {int: [int, int]}:
    """
    Calculates the coordinates of the circle border

    Returns:
         Dictionary, the keys of which is the y coordinate,
         the values are an array with boundaries along the x coordinate
    """
    a = {}  # coord
    for y in range(yc-delta, yc+delta+1):
        if 0 <= y <= arr.shape[0]:
            x = math.sqrt(delta ** 2 - (y - yc) ** 2) + xc
            x_min = math.floor(2*xc-x)
            x_max = math.ceil(x)
            if x_min < 0:
                x_min = 0
            if x_max > arr.shape[1]:
                x_max = arr.shape[1]
            a[y] = [x_min, x_max]
    return a


def cf(img_arr: np.ndarray) -> []:
    """
    Calculates the color border
    The mean is calculated and the standard deviation is added to it,
    or the standard deviation is subtracted from the mean

    Returns:
         List[color, color boarder]
    """
    df = pd.DataFrame(img_arr.T.reshape(-1, 3), columns=['R', 'G', 'B'])
    if df.B.mean() - df.B.min() < df.B.max() - df.B.mean():
        return ['white', math.ceil(df.B.mean() + df.B.std())]
    else:
        return ['black', math.ceil(df.B.mean() - df.B.std())]


def calculate_boarder(img, kf: int) -> []:
    """
    Finds and calculates the contours of the desired objects

    Returns:
         2 data structures of the same content, [np.ndarray, dict]
    """
    hsv_min = np.array((0, 0, kf), np.uint8)
    hsv_max = np.array((255, 255, 255), np.uint8)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # меняем цветовую модель с BGR на HSV
    thresh = cv.inRange(hsv, hsv_min, hsv_max)  # применяем цветовой фильтр
    # ищем контуры и складируем их в переменную contours
    contours, _ = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    _contours = []
    for _arr in contours:
        if len(_arr) >= 15:
            _contours.append(_arr)
    contours = _contours
    contours_list = []
    for _array in _contours:
        coord_dict = {}
        for elements in _array:
            x = elements[0][0]
            y = elements[0][1]
            if coord_dict.get(y, None):
                coord_dict[y].append(x)
            else:
                coord_dict[y] = [x]
        contours_list.append(coord_dict)
    response = []
    for _arr in contours_list: # находит граничные значения контура
        response_elem = {}
        for k, v in _arr.items():
            if len(v) > 2:
                response_elem[k] = [min(v), max(v)]
            else:
                response_elem[k] = v
        response.append(response_elem)
    return [contours, response]


def check_coincidences(circle: dict, contours_dict: list, contours: list) -> list:
    """
    Selection of the desired contours

    Returns:
         Selected contours, np.ndarray
    """
    contours = [contours[contour_index] for contour_index in range(len(contours))
                if check_area_coincidences(contours_dict[contour_index], circle)]
    return contours


def check_area_coincidences(area: dict, circle: dict) -> bool:
    """
    Checking the intersection of the contour with the search area

    Returns:
         bool
    """
    for y, x_list in area.items():
        circle_x_coords = circle.get(y, [])
        for circle_x in circle_x_coords:
            if x_list[0] <= circle_x <= x_list[-1]:
                return True
            elif x_list[0] == circle_x:
                return True
        if len(circle_x_coords) > 1:
            if x_list[0] >= circle_x_coords[0] and x_list[-1] <= circle_x_coords[-1]:
                return True
    return False


def painter(contours: list, img_arr: np.ndarray, area_color: str, color=None) -> np.ndarray:
    """
    Draws a new image with found areas

    Returns:
        np.ndarray
    """
    if color is None:
        color = [255, 0, 0]
        # if area_color == 'white':
        #     color = [255, 255, 255]
        # elif area_color == 'black':
        #     color = [0, 0, 0]
    if area_color == 'white':
        for y in range(img_arr.shape[0]):
            for x in range(img_arr.shape[1]):
                img_arr[y][x] = [0, 0, 0]
    elif area_color == 'black':
        for y in range(img_arr.shape[0]):
            for x in range(img_arr.shape[1]):
                img_arr[y][x] = [255, 255, 255]
    img_arr = cv.drawContours(img_arr, contours, -1, color, cv.FILLED, cv.LINE_AA, maxLevel=1)
    return img_arr


def main():
    inputs = input_params()
    circle = create_circle(inputs['input'], inputs['delta'], inputs['xc'], inputs['yc'])
    ans = calculate_boarder(inputs['input'], cf(inputs['input'])[1])
    new_img = painter(check_coincidences(circle, ans[1], ans[0]),  inputs['input'], cf(inputs['input'])[0],
                      inputs['color'])
    Image.fromarray(new_img).save(inputs['output'])


if __name__ == '__main__':
    main()
