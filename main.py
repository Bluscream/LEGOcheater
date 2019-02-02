import time, numpy, cv2, mss, pytesseract, re
from itertools import repeat, groupby
from operator import itemgetter
from datetime import datetime

enabled = True

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
mon = {'top': 390, 'left': 540, 'width': 839, 'height': 323}
regex = re.compile(r"^[A-Z0-9]{6}$")

config = ""
# config += "--psm 10 --oem 3"
config += "--psm 7"  # single line mode
config += " -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
config += " -c enable_new_segsearch=1 -c language_model_penalty_non_freq_dict_word=10 -c language_model_penalty_non_dict_word=10"

def most_common(L):
    SL = sorted((x, i) for i, x in enumerate(L))
    groups = groupby(SL, key=itemgetter(0))
    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(L)
        for _, where in iterable:
            count += 1
            min_index = min(min_index, where)
        # print 'item %r, count %r, minind %r' % (item, count, min_index)
        return count, -min_index
    return max(groups, key=_auxfun)[0]

class LEGOCheater(object):
    def __init__(self):
        self.sct = mss.mss()
        self.lasttext = ""

    def codeFromScreen(self):
            img = numpy.asarray(self.sct.grab(mon))
            # cv2.imshow('Original', img)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, None, fx=.5, fy=.5)
            # img = cv2.bitwise_not(img)
            # cv2.imshow('Preview', img)
            text = pytesseract.image_to_string(img, config=config)
            text = text.strip().upper()
            # print(datetime.now(), "\"",text,"\"!=\"",lasttext,"\":",text!=lasttext)
            if text != self.lasttext:
                self.lasttext = text
                if (text):
                    match = regex.match(text)
                    if (match):
                        # text = match.group(1)
                        return text

cheater = LEGOCheater()
while enabled:
    codes = []; code = None
    for _ in repeat(None, 3):
        code = cheater.codeFromScreen()
        if code: codes.append(codes)
        time.sleep(.1)
    if len(codes) > 0:
        code = most_common(codes)[0]
        codes.clear()
    if code:
        print("===", datetime.now(), "===")
        print(code)
        print("==================================")
    if cv2.waitKey(25) & 0xFF == ord('q'): # Press "q" to quit
        enabled = False
        break

cv2.destroyAllWindows()