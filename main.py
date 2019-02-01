import time, numpy, cv2, mss, pytesseract, re
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
# mon = {'top': 546, 'left': 367, 'width': 839, 'height': 323}
mon = {'top': 390, 'left': 540, 'width': 839, 'height': 323}
regex = re.compile(r"^[A-Z0-9]{6}$")

lasttext = ""

config = ""
# config += "--psm 7"  # single line mode
# config += " tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# config += " -c enable_new_segsearch=1 -c language_model_penalty_non_freq_dict_word=10 -c language_model_penalty_non_dict_word=10"

with mss.mss() as sct:
    while True:
        img = numpy.asarray(sct.grab(mon))
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, None, fx=.25, fy=.25)
        cv2.imshow('Preview', img)
        text = pytesseract.image_to_string(img,config=config)
        text = text.strip()
        if (text != lasttext):
            if (text):
                match = regex.match(text)
                if (match):
                    # text = match.group(1)
                    print("===", datetime.now(), "===")
                    print(text)
                    print("==================================")
        lasttext = text

        if cv2.waitKey(25) & 0xFF == ord('q'): # Press "q" to quit
            cv2.destroyAllWindows()
            break

        time.sleep(1) # One screenshot per second