import cv2
import pytesseract
import numpy as np

#função retirada da internet
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

def verfPlate(plate):
    contAlpha = 0
    contNum = 0
    verf = False
    for carac in plate:
        if carac.isalpha() == True:
            contAlpha = contAlpha + 1
        if carac.isdigit():
            contNum = contNum + 1
    if contAlpha == 3 and contNum == 4:
        verf = True
    
    return verf

if __name__ == "__main__":
    verf = 0
    gamma = 1
    verfPlaca = False

    while(verf != 2):

        findPlate("plates/placa-modelo3.png", gamma)
        ocr = ocrPlate()

        # print(ocr) #test
        # print("gama: " + str(gamma)) #test
        # print(len(ocr)) #test

        if len(ocr) != 0:

            ocrSplited = ocr.split()

            for ocrSe in ocrSplited:
                if len(ocrSe) == 7:
                    if verfPlate(ocrSe) == True:
                        verf = verf + 1
                        gamma = gamma + 1
                        # print(ocrSe)
                        result = ocrSe
                    elif verf > 0:
                        verf = 2
            if verf == 0:
                gamma = gamma + 1
        else:
            gamma = gamma + 1
        
        if gamma == 50:
            verf = 2
            result = "Não foi possivel achar uma placa ou a placa não é do modelo anterior ao Mercosul!"
    
    print("Plate: " + result)
                
