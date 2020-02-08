# Import tinkter for GUI
import tkinter as tk
from tkinter import messagebox

# Import openCV for video
import cv2 as cv2

# Import pillow for reading image and drawing on canvas
import PIL.Image
import PIL.ImageTk

# Import os for file handling
import os as os

# Import datetime for timestamps
from datetime import datetime

# Lets create a class for app

PATH = 'C:\\Users\\op95w\\github\\python_code\\Vlog_app\\'


class AppGUI:
    def __init__(self, window_title, iconFileName, widthXheight="700x540"):

        self.app_window = tk.Tk()

        # set the window name
        self.app_window.title(window_title)

        # Set the icon
        self.app_window.iconbitmap(iconFileName)

        # Set aspect ratio
        self.app_window.geometry(widthXheight)

        # Open a video source
        self.video = captureVideo(video_source=0)

        # Create a canvas that fits the video
        self.frame1 = tk.Frame(self.app_window)
        self.frame1.pack()
        self.canvas = tk.Canvas(self.frame1, width=self.video.width, height=self.video.height)
        self.canvas.pack(padx=10, side=tk.LEFT)

        # Set what happens when closing
        self.app_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create buttons and other UI components
        # First lets create a frame for buttons
        self.frame2 = tk.Frame(self.app_window)
        self.frame2.pack()
        # Creating a photoimage object to use image in button
        rec_photo1 = PIL.ImageTk.PhotoImage(
            file=PATH+"record_icon.ico")
        self.button_rec = tk.Button(self.frame2, text="Record Vlog", image=rec_photo1, compound="left")
        self.button_rec.state = False
        self.button_rec_prev = False
        self.button_rec.bind('<ButtonRelease-1>', self.manage_recording)
        self.button_rec.pack(ipadx=5, padx=10, side=tk.LEFT)

        # Creating a label for displaying current status
        self.label_bottom = tk.Label(self.app_window, text="Press the record button to start vlogging")
        self.label_bottom.place(relx=1.0, rely=1.0, anchor='se')

        # Creating one more button for face detection toggle
        rec_photo2 = PIL.ImageTk.PhotoImage(file=PATH+"face_icon.ico")
        self.button_face_detect = tk.Button(self.frame2, text="Detect Faces", image=rec_photo2, compound="left")
        self.button_face_detect.state = False
        self.button_face_detect.bind('<ButtonRelease-1>', self.toggle_face_detection)
        self.button_face_detect.pack(ipadx=5, padx=10, side=tk.LEFT)

        # Create new folder for recordings
        self.dirName = 'Vlog_Recordings'
        # Create target Directory if don't exist
        if not os.path.exists(self.dirName):
            os.mkdir(self.dirName)
            print("Directory ", self.dirName,  " Created ")
        else:
            print("Directory ", self.dirName,  " already exists")

        # Set delay and call update method
        self.delay = 10
        self.update()

        # Run the GUI
        self.app_window.mainloop()

    def update(self):
        # get frame from video
        ret, frame = self.video.get_frame()

        if ret:
            if self.button_face_detect.state is True:
                # First thing is detect face
                faces = self.video.face_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # text
            text_date = datetime.now().strftime("%d-%b-%Y")
            text_time = datetime.now().strftime("%H:%M:%S")
            # font
            font = cv2.FONT_HERSHEY_PLAIN
            # org
            org_date = (500, 375)
            org_time = (500, 395)
            # fontScale
            fontScale = 1
            # Red color in BGR
            color = (0, 255, 0)
            # Line thickness of 2 px
            thickness = 1

            # Using cv2.putText() method
            frame = cv2.putText(frame, text_date, org_date, font, fontScale, color, thickness, cv2.LINE_AA, False)
            frame = cv2.putText(frame, text_time, org_time, font, fontScale, color, thickness, cv2.LINE_AA, False)

            # Add frame lines to video
            cv2.line(img=frame, pt1=(575, 75), pt2=(625, 75), color=(
                0, 255, 0), thickness=2, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(625, 75), pt2=(625, 105), color=(
                0, 255, 0), thickness=2, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(15, 75), pt2=(65, 75), color=(
                0, 255, 0), thickness=2, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(15, 75), pt2=(15, 105), color=(
                0, 255, 0), thickness=2, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(575, 405), pt2=(625, 405),
                     color=(0, 255, 0), thickness=2, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(625, 405), pt2=(625, 375),
                     color=(0, 255, 0), thickness=2, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(15, 405), pt2=(65, 405), color=(
                0, 255, 0), thickness=2, lineType=8, shift=0)
            cv2.line(img=frame, pt1=(15, 405), pt2=(15, 375), color=(
                0, 255, 0), thickness=2, lineType=8, shift=0)

            # Plot to canvas in app
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        if self.button_rec.state:
            # Converts to HSV color space, RGB frame is converted to hsv
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # output the frame
            self.recording.write(hsv)

        if self.button_rec_prev is True and self.button_rec.state is False:
            # Release the output
            self.recording.release()
            print("recording released")

        # Update prev state
        self.button_rec_prev = self.button_rec.state

        self.app_window.after(self.delay, self.update)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.video.__del__()
            self.app_window.destroy()

    def manage_recording(self, event):
        if self.button_rec.state is False:
            self.button_rec.state = True
            self.button_rec.configure(text="Pause Vlog")

            # Set frame per second for recording
            self.fps = 15
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            # Current recording file
            timestampStr = "\\Vlog_" + datetime.now(
            ).strftime("%d-%b-%Y_%H-%M-%S")+".avi"
            self.current_rec_file = self.dirName + timestampStr
            # Write to recording using video writer
            self.recording = cv2.VideoWriter(
                self.current_rec_file, fourcc, self.fps, (
                    int(self.video.width), int(self.video.height)))
            self.show_status("Recording in progress...")
        else:
            self.button_rec.configure(text="Record Vlog")
            self.button_rec.state = False
            self.show_status("Recording Stopped and saved.")

    def toggle_face_detection(self, event):
        if self.button_face_detect.state is False:
            self.button_face_detect.state = True
            self.button_face_detect.configure(text="Stop Detection")
            self.show_status("Detecting Faces...")
        else:
            self.button_face_detect.configure(text="Detect Faces")
            self.button_face_detect.state = False
            self.show_status("Face detection stopped")

    def show_status(self, msg):
        self.label_bottom.configure(text=msg)

    # Class to capture video


class captureVideo:
    def __init__(self, video_source=0):
        # open video source
        self.capturedVideo = cv2.VideoCapture(video_source)
        # Throw error if not openeing
        if not self.capturedVideo.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source and hieght
        self.width = self.capturedVideo.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.capturedVideo.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Initialize object detection cascades
        self.face_cascade = cv2.CascadeClassifier(
            PATH + 'haarcascade_frontalface_default.xml')

    def __del__(self):
        if self.capturedVideo.isOpened():
            self.capturedVideo.release()

    def get_frame(self):
        if self.capturedVideo.isOpened():
            ret, frame = self.capturedVideo.read()
            if ret:
                # return current frame converted to RGB
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)


# Lets run the app
AppGUI("Vlog Master", PATH+"favicon.ico", "700x540")
