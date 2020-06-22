import face_recognition
import cv2
import numpy as np

video_capture=cv2.VideoCapture(0)

huraken_image=face_recognition.load_image_file("../known/known.jpg")
huraken_face_encoding=face_recognition.face_encodings(huraken_image)[0]

known_face_encodings=[
    huraken_face_encoding
]

known_face_name=[
    "Huraken"
]

face_locations=[]
face_encodings=[]
face_names=[]
current_frame=True

while True :
    ret,frame = video_capture.read()
    small_frame=cv2.resize(frame, (0,0), fx=0.25,fy=0.25)
    
    rgb_frame=small_frame[:,:,::-1]
    
    if current_frame :
        face_locations=face_recognition.face_locations(rgb_frame)
        face_encodings=face_recognition.face_encodings(rgb_frame,face_locations)
        
        face_names=[]
        for current_encoding in face_encodings :
            
            matches=face_recognition.compare_faces(known_face_encodings,current_encoding)
            name="Unknown"
            
            face_distances=face_recognition.face_distance(known_face_encodings,current_encoding)
            best_match_index=np.argmin(face_distances)
            if matches[best_match_index] :
                name=known_face_name[best_match_index]
                
            face_names.append(name)
        current_frame=not current_frame
        
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()