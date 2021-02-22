import cv2
import math
from PIL import Image
import re


def cv2pil(frame):
    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


def drawRectangle(haystack, needle):
    cv2.rectangle(img, subimg_location(haystack, needle),
                  (subimg_location(haystack, needle)[0] + needle.size[0],
                  subimg_location(haystack, needle)[1] + needle.size[1]),
                  (0, 0, 255), 2)


workspacePath = r"C:\Users\KPY35\Desktop\PYE\image_finding_with_regex\\"
main = Image.open(workspacePath + "data\\main.png")
sub = Image.open(workspacePath + "data\\sub.png")
sub2 = Image.open(workspacePath + "data\\sub2.png")
sub3 = Image.open(workspacePath + "data\\sub3.png")
img = cv2.imread(workspacePath + "data\\main.png")
main = cv2pil(img)

im = Image.new('RGB', (2, 2), 'white')
im2 = Image.new('RGB', (1, 1), (0, 255, 0))
im3 = Image.new('RGB', (3, 3), 'white')
im.putpixel((0, 1), (0, 0, 255))  # x, y
im.putpixel((1, 0), (0, 255, 0))
im.putpixel((1, 1), (255, 0, 0))
im3.putpixel((2, 1), (0, 255, 0))

im_multi = Image.new('RGB', (3, 3), 'white')
im_multi2 = Image.new('RGB', (2, 2), (0, 0, 0))
im_multi.putpixel((1, 1), (0, 0, 0))
im_multi.putpixel((2, 1), (0, 0, 0))
im_multi.putpixel((1, 2), (0, 0, 0))
im_multi.putpixel((2, 2), (0, 0, 0))

# im.show()
im_str = (str(im.convert('RGB').tobytes())[2:])[:-1].replace('\\x', "")
split = [im_str[i:i+im.size[0]*3]
         for i in range(0, len(im_str), im.size[0] * 3)]
# print(im_str,split)


def subimg_location(haystack, needle):
    haystack = haystack.convert('RGB')
    needle = needle.convert('RGB')
    haystack_str = (str(haystack.tobytes("hex", "rgb"))[2:])[:-1]\
        .replace('\\n', "")
    needle_str = (str(needle.tobytes("hex", "rgb"))[2:])[:-1]\
        .replace('\\n', "")
    # print("haystack_str:", haystack_str)
    # print("len(haystack_str):", len(haystack_str))
    # print("needle_str:", needle_str)

    gap_size = (haystack.size[0]-needle.size[0])*3*2
    # print("gap_size:", gap_size)
    gap_regex = '.{' + str(gap_size) + '}'
    # print("needle.size[0]:", needle.size[0])
    # Split b into needle.size[0] chunks
    chunk_size = needle.size[0]*3*2
    split = [needle_str[i:i+chunk_size]
             for i in range(0, len(needle_str), chunk_size)]

    # for i in range(0, len(needle_str), chunk_size):
    #   split2[i] = needle_str[i:i+chunk_size]

    # Build regex
    regex = re.escape(split[0])
    # print("split", split)
    for i in range(1, len(split)):
        # print(gap_regex,re.escape(split[i]))
        regex += gap_regex + re.escape(split[i])

    # print(regex)
    p = re.compile(regex)  # ''
    # print(p)
    m = p.search(haystack_str)
    # print(m)
    if not m:
        return None
    x, _ = m.span()
    # left = int(round(x % (haystack.size[0] * 3) / 3))
    # top  = int(round(x / haystack.size[0] / 3))
    left = round(haystack.size[0]-1) \
        if round(((x+6)/6) % haystack.size[0])-1 == -1 \
        else round(((x+6)/6) % haystack.size[0])-1
    top = math.ceil((x+6)/6/haystack.size[0])-1
    return (left, top)


# print(subimg_location(main, sub))
# print(subimg_location(im3,im2))
# print(subimg_location(im_multi,im_multi2))
drawRectangle(main, sub)
drawRectangle(main, sub2)
drawRectangle(main, sub3)
image = cv2.circle(img, subimg_location(main, sub3),
                   radius=10, color=(0, 0, 255), thickness=-1)
cv2.imshow("OpenCV Image Reading", img)
cv2.waitKey(0)
