import cv2
import math
from PIL import Image, ImageOps
import re


def cv2pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def subimg_location(haystack, needle):
    haystack = ImageOps.grayscale(haystack)
    needle = ImageOps.grayscale(needle)
    haystack_str = (str(haystack.tobytes("hex"))[2:])[:-1]\
        .replace('\\n', "")
    needle_str = (str(needle.tobytes("hex"))[2:])[:-1]\
        .replace('\\n', "")
    gap_size = (haystack.size[0]-needle.size[0])*2
    gap_regex = '.{' + str(gap_size) + '}'
    chunk_size = needle.size[0]*2
    split = [needle_str[i:i+chunk_size]
             for i in range(0, len(needle_str), chunk_size)]
    regex = re.escape(split[0])
    for i in range(1, len(split)):
        regex += gap_regex + re.escape(split[i])
    p = re.compile(regex)
    match_list = []
    for match in re.finditer(regex, haystack_str):
        match_list.append(match.start())
    if match_list == []:
        return None
    position = []
    for x in match_list:
        left = round(haystack.size[0]-1) \
            if round(((x+2)/2) % haystack.size[0])-1 == -1 \
            else round(((x+2)/2) % haystack.size[0])-1
        top = math.ceil((x+2)/2/haystack.size[0])-1
        position.append((left, top))
    return position


def drawRectangle(img, haystack, needle):
    position1D_multi = subimg_location(haystack, needle)
    if position1D_multi is not None:
        for x, y in position1D_multi:
            cv2.rectangle(img, (x, y),
                          ((x, y)[0] + needle.size[0],
                          (x, y)[1] + needle.size[1]),
                          (0, 0, 255), 2)
