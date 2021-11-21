import cv2
import pytesseract
import numpy as np

#função já criada
def adjust_gamma(image, gamma):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")

    return cv2.LUT(image, table)

def findPlate(source, gamma):
    img = cv2.imread(source)
    # cv2.imshow("Original", img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray", gray)

    gray_gamma = adjust_gamma(gray, gamma)
    # cv2.imshow("Gray Gamma", gray_gamma)

    _, bin = cv2.threshold(gray_gamma, 200, 255, cv2.THRESH_BINARY)
    # cv2.imshow("Binary", img)

    blur = cv2.GaussianBlur(bin, (5, 5), 0)
    # cv2.imshow("Blur", bluur)

    cv2.imwrite('temp-files/plate.png', blur)

    # contours, hierarchy = cv2.findContours(bluur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (255, 0, 0), 1)
    # cv2.imshow("contours", img)

def ocrPlate():
    image = cv2.imread("temp-files/plate.png")
    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'
    result = pytesseract.image_to_string(image, lang='eng', config=config)

    return result

if __name__ == "__main__":
    verf = 0
    gamma = 1

    while(verf != 2):

        findPlate("plates/placa-carro.jpg", gamma)
        ocr = ocrPlate()

        # print(ocr) #test
        # print("gama: " + str(gamma)) #test
        # print(len(ocr)) #test

        if len(ocr) != 0:

            ocrSplited = ocr.split()

            for ocrSe in ocrSplited:
                if len(ocrSe) == 7:
                    #verificar aqui se a placa contem 3 letras e 4 numeros (para o modelo de placa antigo)
                    verf = verf + 1
                    gamma = gamma + 1
                    # print(ocrSe)
                    result = ocrSe
                elif verf == 1:
                    verf = 2
            if verf == 0:
                gamma = gamma + 1
        else:
            gamma = gamma + 1
    
    print("Plate: " + result)
                
