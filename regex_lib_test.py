import sys
sys.dont_write_bytecode = True
import imgFindRegexLib as imreg
import imgFindRegexLib1D as imreg1D
import time


def main():
    workspacePath = r"C:\Users\KPY35\Desktop\PYE\image_finding_with_regex\\"
    sub_cv = imreg.cv2.imread(workspacePath + "data\\sub.png")
    sub2_cv = imreg.cv2.imread(workspacePath + "data\\sub2.png")
    sub3_cv = imreg.cv2.imread(workspacePath + "data\\sub3.png")
    main_cv = imreg.cv2.imread(workspacePath + "data\\main.png")

    sub_pil = imreg.cv2pil(sub_cv)
    sub2_pil = imreg.cv2pil(sub2_cv)
    sub3_pil = imreg.cv2pil(sub3_cv)
    main_pil = imreg.cv2pil(main_cv)
    for i in range(100):
        start_time = time.time()
        position = imreg.subimg_location(main_pil, sub_pil)
        position_time = time.time()
        position1D = imreg1D.subimg_location(main_pil, sub_pil)
        position1D_time = time.time()
        all_time = position1D_time - start_time
        subimg_location_time = (position_time-start_time)/all_time*100
        subimg1D_location_time = (position1D_time-position_time)/all_time*100
        print(subimg_location_time, subimg1D_location_time)
        print(position, position1D)

    imreg.drawRectangle(main_cv, main_pil, sub_pil)
    imreg.drawRectangle(main_cv, main_pil, sub2_pil)
    imreg.drawRectangle(main_cv, main_pil, sub3_pil)
    imreg.cv2.imshow("OpenCV Image Reading", main_cv)
    imreg.cv2.waitKey(0)


if __name__ == '__main__':
    main()
