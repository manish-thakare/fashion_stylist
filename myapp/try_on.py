import cvzone, cv2
from cvzone.PoseModule import PoseDetector
from rembg import remove
from PIL import Image
import os

def removebg(inputpath):
    input = Image.open(inputpath)
    output = remove(input)
    
    return output

# cap = cv2.VideoCapture('media/itemimages/1.mp4')
cap = cv2.VideoCapture(0)
detector = PoseDetector()

itemFolderPath = 'media/itemimages'
listitems = os.listdir(itemFolderPath)
print(listitems)

# wobg = removebg(os.path.join(itemFolderPath,listitems[0]))
# print(wobg)

width_ratio = 270/190
shirt_ratio_width_height = 600/440

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    # img = cv2.flip(img, 1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        lm12 = lmList[12][0:2]
        lm11 = lmList[11][0:2]
        # # center = bboxInfo["center"]
        # # cv2.circle(img, center, 5, (255,0,255), cv2.FILLED)

        imgitem = cv2.imread(os.path.join(itemFolderPath,listitems[1]), cv2.IMREAD_UNCHANGED)
        

        width_shirt = int((lm11[0]-lm12[0])*width_ratio)
        print(width_shirt)
        imgitem = cv2.resize(imgitem,(width_shirt,int(width_shirt*shirt_ratio_width_height)))
        currentScale = (lm11[0]-lm12[0])/190
        offset = int(44*currentScale), int(48*currentScale)
        
        try :
            img = cvzone.overlayPNG(img, imgitem, (lm12[0]-offset[0],lm12[1]-offset[1]))
        except:
            pass
        


    cv2.imshow("Image", img)
    cv2.waitKey(1)