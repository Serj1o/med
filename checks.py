import sys
import numpy as np
import cv2 as cv

# параметры цветового фильтра
hsv_min = np.array((0, 0, 106), np.uint8)
hsv_max = np.array((255, 255, 255), np.uint8)

if __name__ == '__main__':
    fn = 'image_data/test_photo.bmp' # путь к файлу с картинкой
    img = cv.imread(fn)

    hsv = cv.cvtColor( img, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV
    thresh = cv.inRange( hsv, hsv_min, hsv_max ) # применяем цветовой фильтр
    # ищем контуры и складируем их в переменную contours
    contours, hierarchy = cv.findContours( thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    print(contours)

    # отображаем контуры поверх изображения
    cv.drawContours( img, contours, -1, (255,255,255), cv.FILLED, cv.LINE_AA, hierarchy, 1)
    cv.imshow('contours', img) # выводим итоговое изображение в окно

    cv.waitKey()
    cv.destroyAllWindows()

# import cv2
# import numpy as np
#
# if __name__ == '__main__':
#     def nothing(*arg):
#         pass
#
# cv2.namedWindow("result")  # создаем главное окно
# cv2.namedWindow("settings")  # создаем окно настроек
#
# img = cv2.imread("image_data/test_photo.bmp")
# # создаем 6 бегунков для настройки начального и конечного цвета фильтра
# cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
# cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
# cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
# cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
# cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
# cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
# crange = [0, 0, 0, 0, 0, 0]
#
# while True:
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#
#     # считываем значения бегунков
#     h1 = cv2.getTrackbarPos('h1', 'settings')
#     s1 = cv2.getTrackbarPos('s1', 'settings')
#     v1 = cv2.getTrackbarPos('v1', 'settings')
#     h2 = cv2.getTrackbarPos('h2', 'settings')
#     s2 = cv2.getTrackbarPos('s2', 'settings')
#     v2 = cv2.getTrackbarPos('v2', 'settings')
#
#     # формируем начальный и конечный цвет фильтра
#     h_min = np.array((h1, s1, v1), np.uint8)
#     h_max = np.array((h2, s2, v2), np.uint8)
#
#     # накладываем фильтр на кадр в модели HSV
#     thresh = cv2.inRange(hsv, h_min, h_max)
#
#     cv2.imshow('result', thresh)
#
#     ch = cv2.waitKey(5)
#     if ch == 27:
#         break
#
#
# cv2.destroyAllWindows()



