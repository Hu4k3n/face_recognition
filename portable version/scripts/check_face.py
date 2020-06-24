import face_recognition
from os import listdir
from os.path import isfile, join
import cv2
import os

def capture_burst():
    cam=cv2.VideoCapture(0)
    cv2.namedWindow("LockScreen")
    img_counter=0
    while img_counter<=2 :
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        img_name = "Documents/stuff/face-recog/unknown/unknown_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        # print("{} written".format(img_name))
        # print("Analysing burst shot ...("+str(img_counter+1)+"/3)")
        img_counter += 1

    cam.release()
    cv2.destroyAllWindows()

def check_face(known,unknown,n,d):
    check_for_face=face_recognition.load_image_file("Documents/stuff/face-recog/unknown/"+unknown)
    face_exists=face_recognition.face_locations(check_for_face)
    
    if len(face_exists)!=0:
        known_image=face_recognition.load_image_file("Documents/stuff/face-recog/known/"+known)
        known_encoding=face_recognition.face_encodings(known_image)[0]
        
        unknown_image=face_recognition.load_image_file("Documents/stuff/face-recog/unknown/"+unknown)
        unknown_encoding=face_recognition.face_encodings(unknown_image)[0]
        
        # print("Checking ... ("+str(n+1)+"/"+str(d)+")")
        results=face_recognition.compare_faces([known_encoding],unknown_encoding)
        # print(results)
        if(results==[True]) :
            print(known[:len(known)-4])
            return True
    # else :
        # print('No face detected')
        
        
def main():
    print('Facial Recognition initialising ...')
    capture_burst()
    unknown_img = [f for f in listdir("Documents/stuff/face-recog/unknown/") if isfile(join("Documents/stuff/face-recog/unknown/", f))]
    j=0
    final = False
    while j<len(unknown_img):
        knownimages = [f for f in listdir("Documents/stuff/face-recog/known/") if isfile(join("Documents/stuff/face-recog/known/", f))]
        i=0
        while i<len(knownimages) :
            final=check_face(knownimages[i],unknown_img[j],i,len(knownimages))
            if(final == True) :
                break
            i=i+1
        if(final == True) :
            break
        j=j+1
    
    if final == True :
        # print("Exiting ...")
        print("Verified")
        exit()
    else :
        # print('Unknown user \nTurning on screensaver ...')
        print("Non-verified")
        # os.system('xscreensaver')
        # os.system('pkill gnome-terminal')
        exit()
        
if __name__ == "__main__":
    main()
