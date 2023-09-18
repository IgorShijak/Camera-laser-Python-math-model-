import tkinter as tk
import tkinter.messagebox
import os
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import _homogeneus
import _frames
import _utils
import _matrices
import _principal_axis
import _image
import _points
import _laser

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class MyLabelEntryFrame(ctk.CTkFrame):
    def __init__(self, master, title, label_values, entry_values):
        super().__init__(master)
        self.title = title
        self.label_values = label_values
        self.entry_values = entry_values
        self.entries = []

        self.grid_columnconfigure((0, 1), weight=1)

        self.title = ctk.CTkLabel(self, text=self.title, corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew", columnspan=2)

        for i, value in enumerate(self.label_values):
            label = ctk.CTkLabel(self, text=value)
            label.grid(row=i + 1, column=0, padx=(10, 0), pady=5, sticky="e")

        for i, value in enumerate(self.entry_values):
            value_string_var = ctk.StringVar(value=value)
            entry = ctk.CTkEntry(self, textvariable=value_string_var)
            entry.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")
            self.entries.append(entry)


class MyLabelEntryButtonFrame(ctk.CTkFrame):
    def __init__(self, master, title, label_values, entry_values, button_text, button_command):
        super().__init__(master)
        self.title = title
        self.label_values = label_values
        self.entry_values = entry_values
        self.button_text = button_text
        self.button_command = button_command
        self.entries = []
        self.modified = []
        self.last_row = 0

        self.grid_columnconfigure((0, 1), weight=1)

        self.title = ctk.CTkLabel(self, text=self.title, corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew", columnspan=2)

        for i, value in enumerate(self.label_values):
            label = ctk.CTkLabel(self, text=value)
            label.grid(row=i + 1, column=0, padx=(10, 0), pady=5, sticky="e")

        for i, value in enumerate(self.entry_values):
            value_string_var = ctk.StringVar(value=value)
            entry = ctk.CTkEntry(self, textvariable=value_string_var)
            entry.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")
            self.entries.append(entry)
            self.last_row = i + 1

        self.button = ctk.CTkButton(self, text=self.button_text, command=self.button_command, corner_radius=0)
        self.button.grid(row=self.last_row + 1, column=0, padx=10, pady=(15, 5), columnspan=2)


class MyTabView(ctk.CTkTabview):
    def __init__(self, master, width, height, tab_title_1, tab_title_2, label_values, entry_values, button_text, button_command):
        super().__init__(master)
        self.width = width
        self.height = height
        self.tab_title_1 = tab_title_1
        self.tab_title_2 = tab_title_2
        self.label_values = label_values
        self.entry_values = entry_values
        self.button_text = button_text
        self.button_command = button_command
        self.entries = []

        self.add(tab_title_1)
        self.add(tab_title_2)
        self.tab(self.tab_title_1).grid_columnconfigure((0, 1), weight=1)
        self.tab(self.tab_title_2).grid_rowconfigure(0, weight=1)
        self.tab(self.tab_title_2).grid_columnconfigure(0, weight=1)
        self.configure(width=width)
        self.configure(height=height)

        for i, value in enumerate(self.label_values):
            label = ctk.CTkLabel(self.tab(self.tab_title_1), text=value)
            label.grid(row=i, column=0, padx=(10, 0), pady=5, sticky="e")

        for i, value in enumerate(self.entry_values):
            value_string_var = ctk.StringVar(value=value)
            entry = ctk.CTkEntry(self.tab(self.tab_title_1), textvariable=value_string_var)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries.append(entry)

        self.button = ctk.CTkButton(self.tab(self.tab_title_2), text=self.button_text, command=self.button_command,
                                    corner_radius=0)
        self.button.grid(row=0, column=0)


class MyButtonFrame(ctk.CTkFrame):
    def __init__(self, master, title, button_text, button_command):
        super().__init__(master)
        self.title = title
        self.button_text = button_text
        self.button_command = button_command
        self.entries = []
        self.modified = []
        self.last_row = 0

        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(self, text=self.title, corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.button = ctk.CTkButton(self, text=self.button_text, command=self.button_command, corner_radius=0)
        self.button.grid(row=1, column=0, padx=10, pady=(15, 5))


class CanvasFrame(ctk.CTkFrame, ctk.CTk):
    def __init__(self, master, fig1, fig2, fig3):
        super().__init__(master)
        self.fig1 = fig1
        self.fig2 = fig2
        self.fig3 = fig3

        canvas_1 = FigureCanvasTkAgg(self.fig1, self)
        canvas_1.draw()
        canvas_1.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="w")

        canvas_2 = FigureCanvasTkAgg(self.fig2, self)
        canvas_2.draw()
        canvas_2.get_tk_widget().grid(row=1, column=0, padx=5, sticky="sew", columnspan=2)
        toolbar_2 = NavigationToolbar2Tk(canvas_2, self, pack_toolbar=False)
        toolbar_2.update()
        toolbar_2.grid(row=1, column=0, padx=5, pady=5, sticky="s", columnspan=2)

        canvas_3 = FigureCanvasTkAgg(self.fig3, self)
        canvas_3.draw()
        canvas_3.get_tk_widget().grid(row=0, column=1, padx=(0, 5), pady=5, sticky="e")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Camera-laser math model")
        self.geometry("1920x1080")

        # parameters
        self.matrix = 0

        # current tab
        self.tab = "home"

        # set grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                       size=(20, 20))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                       dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                       size=(18, 18))
        self.instructions_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "instructions.png")),
                                               dark_image=Image.open(os.path.join(image_path, "instructions.png")),
                                               size=(18, 18))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(3, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame,
                                                   text="  Camera-laser\n  math model",
                                                   image=self.logo_image,
                                                   compound="left")
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                         text="Home",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"),
                                         image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.instructions_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                 border_spacing=10, text="Instructions",
                                                 fg_color="transparent", text_color=("gray10", "gray90"),
                                                 hover_color=("gray70", "gray30"),
                                                 image=self.instructions_image, anchor="w",
                                                 command=self.instructions_button_event)
        self.instructions_button.grid(row=2, column=0, sticky="ew")

        # create first frame
        self.frame_1 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_1.grid_rowconfigure(2, weight=1)
        self.frame_1.grid_columnconfigure(2, weight=1)

        self.laser_parameters_frame = MyLabelEntryFrame(self.frame_1,
                                                        title="Laser parameters",
                                                        label_values=["Laser distance (mm):", "Laser angle (°):"],
                                                        entry_values=["421.6", "45"])
        self.laser_parameters_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 5), ipady=5, sticky="nsew")

        self.camera_parameters_frame = MyLabelEntryFrame(self.frame_1,
                                                         title="Camera parameters",
                                                         label_values=["Focal length (mm):",
                                                                       "Camera displacement x (mm):",
                                                                       "Camera displacement y (mm):",
                                                                       "Camera displacement z (mm):",
                                                                       "Camera Euler angle x (°):",
                                                                       "Camera Euler angle y (°):",
                                                                       "Camera Euler angle z (°):"],
                                                         entry_values=["8", "0", "0", "152.1", "-70.16", "180", "0"])
        self.camera_parameters_frame.grid(row=1, column=0, padx=(0, 10), pady=5, ipadx=10, ipady=5, sticky="nsew")

        self.sensor_parameters_frame = MyTabView(self.frame_1,
                                                 width=314,
                                                 height=276,
                                                 tab_title_1="Sensor parameters",
                                                 tab_title_2="Camera matrix",
                                                 label_values=["Sensor width (mm):",
                                                               "Sensor height (mm):",
                                                               "Pixel width (mm):",
                                                               "Pixel height (mm):",
                                                               "Principal point x (mm):",
                                                               "Principal point y (mm):"],
                                                 entry_values=["5.76", "3.6", "3e-03", "3e-03", "2.88", "1.8"],
                                                 button_text="Load from txt file",
                                                 button_command=self.load_from_txt_matrix)
        self.sensor_parameters_frame.grid(row=0, column=1, pady=(0, 5), sticky="nsew")

        self.distortion_parameters_frame = MyLabelEntryButtonFrame(self.frame_1,
                                                                   title="Distortion parameters",
                                                                   label_values=["k1:", "k2:", "k3:", "p1:", "p2:"],
                                                                   entry_values=["0", "0", "0", "0", "0"],
                                                                   button_text="Load from txt file",
                                                                   button_command=self.load_from_txt)
        self.distortion_parameters_frame.grid(row=1, column=1, pady=5, ipadx=10, ipady=5, sticky="nsew")

        self.image_resolution_frame = MyLabelEntryButtonFrame(self.frame_1,
                                                              title="Image resolution",
                                                              label_values=["Image width (px):", "Image height (px):"],
                                                              entry_values=["1920", "1200"],
                                                              button_text="Graph",
                                                              button_command=self.button_pressed)
        self.image_resolution_frame.grid(row=2, column=0, pady=(5, 0), ipadx=10, ipady=5, sticky="nsew", columnspan=2)

        # create second frame
        self.frame_2 = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_2.grid_rowconfigure(0, weight=1)
        self.frame_2.grid_columnconfigure(0, weight=1)

        self.text = ctk.CTkTextbox(self.frame_2)
        self.text.insert("1.0", "Camera-laser math model instructions:"
                                "\n\n\nLaser:"
                                "\n\n- laser distance - the distance between laser dots and the "
                                "origin of the reference coordinate system"
                                "\n- laser angle - the angle of propagation of the laser beam of light"
                                "\n\n\nCamera parameters:"
                                "\n\n- focal length - the focal length of the camera"
                                "\n- camera displacement x, y, z - camera displacement relative to the lase in the "
                                "direction of the laser x, y and z axis"
                                "\n- camera Euler angles (Tait-Bryan angles) - camera Euler angles around the x, y and"
                                " z axis that follow the right hand rule. They are used for getting roll Rx, pitch Ry "
                                "and yaw Rz matrices that are used for getting the rotation matrix Rz*Ry*Rx"
                                "\n\n\nSensor parameters/Camera matrix"
                                "\n\n- an option to use sensor parameters to calculate the ideal camera matrix or to"
                                " load a camera matrix from a txt file that has been calculated after calibration"
                                "\n- principal point - the x and y coordinates of the principal point in the image"
                                " coordinate system"
                                "\n\n\nDistortion parameters"
                                "\n\n- there is an option to insert the distortion coefficients manually or to load"
                                " them from a txt file"
                                "\n - k1, k2, k3 - radial distortion coefficients of the lens"
                                "\n - p1, p2 - tangential distortion coefficients of the lens"
                                "\n\n\nImage resolution"
                                "\n\n- image width and image height in pixels")
        self.text.configure(state="disabled")
        self.text.configure(spacing1=2.5)
        self.text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # select default frame
        self.select_frame_by_name("home")

        self.button_pressed()

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.instructions_button.configure(fg_color=("gray75", "gray25") if name == "instructions" else "transparent")

        # show selected frame
        if name == "home":
            self.frame_1.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        else:
            self.frame_1.grid_forget()
        if name == "instructions":
            self.frame_2.grid(row=0, column=1, sticky="nsew")
        else:
            self.frame_2.grid_forget()

    def home_button_event(self):
        self.tab = "home"
        self.select_frame_by_name(self.tab)

    def instructions_button_event(self):
        self.tab = "instructions"
        self.select_frame_by_name(self.tab)

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def load_from_txt(self):
        text_file = filedialog.askopenfilename(initialdir="Ovaj PC", title="Open Text File",
                                               filetypes=(("Text Files", "*.txt"),))
        text_file = open(text_file, 'r')
        stuff = text_file.readlines()

        for line in stuff:
            self.distortion_parameters_frame.modified.append(line.strip())

        for i, value in enumerate(self.distortion_parameters_frame.entries):
            value.delete(0, ctk.END)
            value.insert(0, self.distortion_parameters_frame.modified[i])

    def load_from_txt_matrix(self):
        text_file = filedialog.askopenfilename(initialdir="Ovaj PC", title="Open Text File",
                                               filetypes=(("Text Files", "*.txt"),))
        self.matrix = np.loadtxt(text_file)

    def button_pressed(self):
        LASER_DISTANCE = float(self.laser_parameters_frame.entries[0].get())  # length of laser plane
        LASER_ANGLE = (float(self.laser_parameters_frame.entries[1].get()) / 180) * np.pi  # laser angle
        NUM_OF_POINTS = 40  # number of points at the end of laser
        L = np.array([0, 0, 0])  # laser centre
        FOCAL_LENGTH = int(self.camera_parameters_frame.entries[0].get())  # focal length
        x = float(self.camera_parameters_frame.entries[1].get())
        y = float(self.camera_parameters_frame.entries[2].get())
        z = float(self.camera_parameters_frame.entries[3].get())
        C = np.array([x, y, z])  # camera centre
        THETA_X = (float(self.camera_parameters_frame.entries[4].get()) / 180) * np.pi  # roll angle
        THETA_Y = (float(self.camera_parameters_frame.entries[5].get()) / 180) * np.pi
        THETA_Z = (float(self.camera_parameters_frame.entries[6].get()) / 180) * np.pi
        CAMERA_FOV_LENGTH = LASER_DISTANCE + 200  # camera_fov length
        SENSOR_WIDTH = float(self.sensor_parameters_frame.entries[0].get())
        SENSOR_HEIGHT = float(self.sensor_parameters_frame.entries[1].get())
        PW = float(self.sensor_parameters_frame.entries[2].get())  # pixel width
        PH = float(self.sensor_parameters_frame.entries[3].get())  # pixel height
        PX = float(self.sensor_parameters_frame.entries[4].get())  # principal point x-coordinate
        PY = float(self.sensor_parameters_frame.entries[5].get())  # principal point y-coordinate
        IMAGE_WIDTH = int(self.image_resolution_frame.entries[0].get())
        IMAGE_HEIGHT = int(self.image_resolution_frame.entries[1].get())
        k1 = float(self.distortion_parameters_frame.entries[0].get())
        k2 = float(self.distortion_parameters_frame.entries[1].get())
        k3 = float(self.distortion_parameters_frame.entries[2].get())
        p1 = float(self.distortion_parameters_frame.entries[3].get())
        p2 = float(self.distortion_parameters_frame.entries[4].get())
        px = IMAGE_WIDTH * (PX / SENSOR_WIDTH)
        py = IMAGE_HEIGHT * (PY / SENSOR_HEIGHT)

        if self.sensor_parameters_frame.get() == "Sensor parameters":
            calibration_kwargs = {"f": FOCAL_LENGTH, "px": PX, "py": PY, "pw": PW, "ph": PH}
            rotation_kwargs = {"theta_x": THETA_X, "theta_y": THETA_Y, "theta_z": THETA_Z}
            projection_kwargs = {**calibration_kwargs, **rotation_kwargs, "C": C}

            R = _matrices.get_rotation_matrix(**rotation_kwargs)

            dx, dy, dz = np.eye(3)

            camera_frame = _frames.ReferenceFrame(
                origin=C,
                dx=R @ dx,
                dy=R @ dy,
                dz=R @ dz,
                name="Camera",
            )

            Z = _principal_axis.PrincipalAxis(
                camera_center=C,
                camera_dz=camera_frame.dz,
                f=FOCAL_LENGTH,
            )

            image_frame = _frames.ReferenceFrame(
                origin=Z.p - camera_frame.dx * PX - camera_frame.dy * PY,
                dx=R @ dx,
                dy=R @ dy,
                dz=R @ dz,
                name="Image",
            )

            image_plane = _image.ImagePlane(
                origin=image_frame.origin,
                dx=image_frame.dx,
                dy=image_frame.dy,
                dz=image_frame.dz,
                height=SENSOR_HEIGHT,
                width=SENSOR_WIDTH,
                C=C,
                camera_fov_length=CAMERA_FOV_LENGTH
            )

            laser_frame = _frames.ReferenceFrame(
                origin=L,
                dx=dx,
                dy=dy,
                dz=dz,
                name="Laser",
            )

            laser_plane = _laser.LaserPlane(
                origin=L,
                dy=dy,
                fi=LASER_ANGLE,
                length=LASER_DISTANCE
            )

            image = _image.Image(height=IMAGE_HEIGHT, width=IMAGE_WIDTH)

            points_3D = laser_plane.get_points(NUM_OF_POINTS)
            points_2D = []
            points_2D_with_distortion = []

            fig1 = plt.figure(figsize=(4.19, 4))
            ax = plt.axes(projection='3d')
            ax.clear()
            camera_frame.draw3D(scale_factor=100)
            # image_frame.draw3D(show_name=False)
            # Z.draw3D(scale_factor=100, show_principal_point=False)
            image_plane.draw3D()
            laser_frame.draw3D(scale_factor=100)
            laser_plane.draw3D_plane()
            ax.set_title("Camera-laser 3D")
            ax.set_xlabel('x(mm)')
            ax.set_ylabel('y(mm)')
            ax.set_zlabel('z(mm)')

            for i in range(0, points_3D.shape[0]):
                _points.draw3D(points_3D[i], image_plane.pi, C=C)

            fig2 = plt.figure(figsize=(4.19, 5.6))
            ax = fig2.gca()
            ax.clear()
            image.draw()
            ax.set_title("Image")

            for i in range(0, points_3D.shape[0]):
                points_2D.append(_points.calculate_2D(points_3D[i], **projection_kwargs))
                _points.draw(points_2D[i])
                dist_point = _points.calculate_2D_with_distortion(np.asarray(points_2D[i]), k1, k2, k3, p1, p2, px, py,
                                                                  FOCAL_LENGTH, PW, PH)
                points_2D_with_distortion.append(dist_point)
                _points.draw(points_2D_with_distortion[i], color='red')

            ax.legend(["no distortion", "distortion"])

            fig3 = plt.figure(figsize=(4.19, 4))
            ax = plt.axes(projection='3d')
            ax.clear()
            camera_frame.draw3D()
            image_frame.draw3D()
            Z.draw3D()
            image_plane.draw3D_without_fov()
            ax.set_title("Camera sensor 3D")
            ax.set_xlabel('x(mm)')
            ax.set_ylabel('y(mm)')
            ax.set_zlabel('z(mm)')

            for i in range(0, points_3D.shape[0]):
                _points.draw3D_projected(points_3D[i], image_plane.pi, C=C)

            canvas_frame = CanvasFrame(self.frame_1, fig1, fig2, fig3)
            canvas_frame.grid(row=0, column=2, padx=10, sticky="nsew", rowspan=3)

        if self.sensor_parameters_frame.get() == "Camera matrix":
            rotation_kwargs = {"theta_x": THETA_X, "theta_y": THETA_Y, "theta_z": THETA_Z}
            projection_kwargs = {**rotation_kwargs, "C": C, "K": self.matrix}

            dx, dy, dz = np.eye(3)

            laser_plane = _laser.LaserPlane(
                origin=L,
                dy=dy,
                fi=LASER_ANGLE,
                length=LASER_DISTANCE
            )

            points_3D = laser_plane.get_points(NUM_OF_POINTS)
            points_2D = []
            points_2D_with_distortion = []

            image = _image.Image(height=IMAGE_HEIGHT, width=IMAGE_WIDTH)

            fig4 = plt.figure()
            ax = fig4.gca()
            image.draw()
            ax.set_title("Image")

            for i in range(0, points_3D.shape[0]):
                points_2D.append(_points.calculate_2D_w_camera_matrix(points_3D[i], **projection_kwargs))
                _points.draw(points_2D[i])
                dist_point = _points.calculate_2D_with_distortion(np.asarray(points_2D[i]), k1, k2, k3, p1, p2, px, py,
                                                                  FOCAL_LENGTH, PW, PH)
                points_2D_with_distortion.append(dist_point)
                _points.draw(points_2D_with_distortion[i], color='red')

            ax.legend(["no distortion", "distortion"])
            fig4.show()


if __name__ == "__main__":
    app = App()
    app.mainloop()


