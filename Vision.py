import cv2
import numpy as np
from random import randint

class BoundBox:
    def __init__(self,x,y,w,h,is_person):
        self.x1 = x
        self.y1 = y
        self.x2 = self.x1+w
        self.y2 = self.y1+h
        self.w = w
        self.h = h
        self.size = abs(self.w*self.h)
        self.is_person = is_person
    
    # Returns true if the given bound box is within [n] pixels of self
    def compare(self, bbx):
        n = 10
        return abs(self.x1 - bbx.x1) < n and \
                abs(self.y2 - bbx.y2) < n and \
                abs(self.x2 - bbx.x2) < n and \
                abs(self.y1 - bbx.y1) < n
    def draw(self,frame):
        color_dict = {0 : (0,0,255), 1 : (0,255,0), 2 : (255,0,0)}
        color = color_dict[randint(0,len(color_dict)-1)]
        if self.is_person:
            # People are blue
            color = (255,0,0)
        cv2.rectangle(frame,(self.x1,self.y1), 
                     (self.x2, self.y2),color,3)
def congratulate(img, person):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 2
    fontColor              = (0,255,255)
    lineType               = 2
    texts = {0 : 'Yes', 1 : 'Ur so good', 2 : 'Sick'}
    text = texts[randint(0,len(texts)-1)]
    x = int((person.x1 + person.x2) / 2)
    y = int((person.y1 + person.y2) / 2)
    
    cv2.putText(img,text, 
               (x,y), 
               font, 
               fontScale,
               fontColor,
               lineType)
    cv2.imshow("Lowkey waste of time", img)
    cv2.waitKey(3)
    return None
def main():
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    capture = cv2.VideoCapture(0)
    width = int(capture.get(3))
    height = int(capture.get(4))
    stop = False
    t = 0
    correct_count = 0
    new_face = None
    while(not stop):
        ret,frame = capture.read()
		#frame = cv2.resize(frame,800,600)
        
        faces = faceCascade.detectMultiScale(frame, scaleFactor=1.5,minNeighbors=5,minSize=(40,40),flags=cv2.CASCADE_SCALE_IMAGE)
    
        for (x,y,w,h) in faces:
            if new_face is None:
                new_face = BoundBox(0,randint(0,height - 70),w,h,False)

            else:
                # move square
                if new_face.x1 + 1 < width:
                    new_face.x1 += 2
                    new_face.x2 += 2
                else:
                    # update move square back to the edge of frame
                    new_face = BoundBox(0,randint(0,height - 70),w,h,False)
                    
            person = BoundBox(x,y,w,h,True)
            person.draw(frame)
            new_face.draw(frame)
            
            if person.compare(new_face):
                congratulate(frame, person)
                new_face = None
                correct_count += 1
                if correct_count == 4:
                    stop = True
                
        t += 1
                
            
	
        cv2.imshow("Lowkey waste of time", frame)
        cv2.waitKey(1)
main()
        