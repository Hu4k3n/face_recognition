import face_recognition
from os import listdir
from os.path import isfile, join
import cv2

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
        img_name = "../unknown/unknown_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written".format(img_name))
        img_counter += 1

    cam.release()
    cv2.destroyAllWindows()

def check_face(known,unknown):
    check_for_face=face_recognition.load_image_file("../unknown/"+unknown)
    face_exists=face_recognition.face_locations(check_for_face)
    
    if len(face_exists)!=0:
        known_image=face_recognition.load_image_file("../known/"+known)
        known_encoding=face_recognition.face_encodings(known_image)[0]
        
        unknown_image=face_recognition.load_image_file("../unknown/"+unknown)
        unknown_encoding=face_recognition.face_encodings(unknown_image)[0]
        
        print('working on :'+unknown)
        print('checking with : '+known)
        results=face_recognition.compare_faces([known_encoding],unknown_encoding)
        print(results)
        if(results==[True]) :
            return True
    else :
        print('no face')
def main():
    capture_burst()
    unknown_img = [f for f in listdir("../unknown/") if isfile(join("../unknown/", f))]
    j=0
    final = False
    while j<len(unknown_img):
        knownimages = [f for f in listdir("../known/") if isfile(join("../known/", f))]
        i=0
        while i<len(knownimages) :
            final=check_face(knownimages[i],unknown_img[j])
            if(final == True) :
                break
            i=i+1
        if(final == True) :
            break
        j=j+1
    
    if final == True :
        
if __name__ == "__main__":
    main()