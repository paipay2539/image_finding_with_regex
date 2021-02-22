import cv2
import math
from PIL import Image
import re


def cv2pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def subimg_location(haystack, needle):
    haystack = haystack.convert('RGB')
    needle = needle.convert('RGB')
    haystack_str = (str(haystack.tobytes("hex", "rgb"))[2:])[:-1]\
        .replace('\\n', "")
    needle_str = (str(needle.tobytes("hex", "rgb"))[2:])[:-1]\
        .replace('\\n', "")
    gap_size = (haystack.size[0]-needle.size[0])*3*2
    gap_regex = '.{' + str(gap_size) + '}'
    chunk_size = needle.size[0]*3*2
    split = [needle_str[i:i+chunk_size]
             for i in range(0, len(needle_str), chunk_size)]
    regex = re.escape(split[0])
    for i in range(1, len(split)):
        regex += gap_regex + re.escape(split[i])
    p = re.compile(regex)
    m = p.search(haystack_str)
    if not m:
        return None
    x, _ = m.span()
    left = round(haystack.size[0]-1) \
        if round(((x+6)/6) % haystack.size[0])-1 == -1 \
        else round(((x+6)/6) % haystack.size[0])-1
    top = math.ceil((x+6)/6/haystack.size[0])-1
    return (left, top)


def drawRectangle(img, haystack, needle):
    cv2.rectangle(img, subimg_location(haystack, needle),
                  (subimg_location(haystack, needle)[0] + needle.size[0],
                  subimg_location(haystack, needle)[1] + needle.size[1]),
                  (0, 0, 255), 2)
