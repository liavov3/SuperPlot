from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from mpl_toolkits.mplot3d import Axes3D
from data_collector import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull


class MyApp(Tk):
    def __init__(self):
        super().__init__()

        self.title("Super Plot")
        self.df: pd.DataFrame = pd.DataFrame()
        self.convex_df: pd.DataFrame = pd.DataFrame()
        self.x = []
        self.y = []
        self.z = []
        self.convex_x = []
        self.convex_y = []
        self.columns_name: list = []
        self.pathes: list = []
        plt.ioff()
        self.fig, self.ax = plt.subplots()
        self.popup = ''

        # Style
        style_btn = Style()
        style_btn.configure("Rounded.TButton", borderwidth=5, relief="ridge", padding=10)
        style_check_btn = Style()
        style_check_btn.configure("Custom.TCheckbutton", font=('Ariel, 14'))

        # Create the frames for inputs
        self.top_frame = Frame(self)
        self.top_frame.pack(side=TOP, padx=10, pady=10)

        self.bottom_frame = Frame(self)
        self.bottom_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)

        self.left_frame = Frame(self.bottom_frame)
        self.left_frame.pack(side=LEFT, fill=Y, padx=5)

        self.right_frame = Frame(self.bottom_frame)
        self.right_frame.pack(side=RIGHT, fill=Y, padx=5)

        ### IntVars for checkbuttons ###
        self.check_3d = BooleanVar()
        self.check_scatter = BooleanVar()
        self.check_locations = BooleanVar()
        self.check_poly = BooleanVar()
        self.check_axis_equal = BooleanVar()

        ### Buttons in top frame ###
        self.check_3d_btn = Checkbutton(self.top_frame, variable=self.check_3d, text="3D", style="Custom.TCheckbutton", command=self.btn_3d_validity)
        self.check_scatter_btn = Checkbutton(self.top_frame, variable=self.check_scatter, text='Scatter', style="Custom.TCheckbutton")
        self.check_locations_btn = Checkbutton(self.top_frame, variable=self.check_locations, text="Locations", style="Custom.TCheckbutton")
        self.check_poly_btn = Checkbutton(self.top_frame, variable=self.check_poly, text="Add convex hull", style="Custom.TCheckbutton", command=self.btn_poly_validity)
        self.check_axis_equal_btn = Checkbutton(self.top_frame, variable=self.check_axis_equal, text="Axis equal",style="Custom.TCheckbutton", command=self.btn_axis_eq_validity)

        # Griding
        self.check_3d_btn.grid(row=0, column=0, padx=20)
        self.check_scatter_btn.grid(row=0, column=1, padx=20)
        self.check_locations_btn.grid(row=0, column=2, padx=20)
        self.check_poly_btn.grid(row=0, column=3, padx=20)
        self.check_axis_equal_btn.grid(row=0, column=4, padx=20)

        self.button_file = Button(self.top_frame, text='Choose files', style="Rounded.TButton", command=self.path_to_csv)
        self.button_add_files = Button(self.top_frame, text='Add files', style="Rounded.TButton", command=self.path_to_csv)
        self.button_g = Button(self.top_frame, text="Generate",  style="Rounded.TButton", command=self.generate_plot)
        self.button_show = Button(self.top_frame, text="Show plot", style="Rounded.TButton", command=self.show_plot)

        self.button_file.grid(row=1, columnspan=5, pady=10)
        self.button_add_files.grid(row=2, columnspan=5, pady=0)
        self.button_g.grid(row=3, columnspan=5, pady=10)
        self.button_show.grid(row=4, columnspan=5, pady=10)

        self.button_add_files.configure(state="disabled")
        self.button_g.configure(state="disabled")
        self.button_show.configure(state="disabled")

        # Buttons in left frame #
        self.x_axis_var = StringVar()
        self.y_axis_var = StringVar()
        self.z_axis_var = StringVar()

        # Axes setter
        self.list_box_x = OptionMenu(self.left_frame, self.x_axis_var, *self.columns_name)
        self.list_box_y = OptionMenu(self.left_frame, self.y_axis_var, *self.columns_name)
        self.list_box_z = OptionMenu(self.left_frame, self.z_axis_var, *self.columns_name)

        # Scaling setter
        self.entry_scaleX = Entry(self.left_frame)
        self.entry_scaleY = Entry(self.left_frame)
        self.entry_scaleZ = Entry(self.left_frame)

        self.entry_scaleX.insert(0, '1')
        self.entry_scaleY.insert(0, '1')
        self.entry_scaleZ.insert(0, '1')

        # Adding setter
        self.entry_addX = Entry(self.left_frame)
        self.entry_addY = Entry(self.left_frame)
        self.entry_addZ = Entry(self.left_frame)

        self.entry_addX.insert(0, '0')
        self.entry_addY.insert(0, '0')
        self.entry_addZ.insert(0, '0')

        # Azimuth setter (right frame)
        self.entry_azimuth = Entry(self.right_frame)
        self.entry_azimuth.insert(0, '0')

        # New Graph and convex to csv btns #
        self.button_new = Button(self.right_frame, text="New graph", style="Rounded.TButton", command=self.new_app)
        self.convex_hull_to_csv = Button(self.right_frame, text="Convex hull to csv",
                                         style="Rounded.TButton", command=self.convex_to_csv)

        # Grid labels in left frame #
        Label(self.left_frame, text="X axis:").grid(row=0, column=0, padx=5, pady=5)
        Label(self.left_frame, text="Y axis:").grid(row=1, column=0, padx=5, pady=5)
        Label(self.left_frame, text="Z axis:").grid(row=2, column=0, padx=5, pady=5)

        Label(self.left_frame, text="").grid(row=3, column=0, padx=5, pady=20)

        Label(self.left_frame, text="Scale x:").grid(row=4, column=0, padx=5, pady=5)
        Label(self.left_frame, text="Scale y:").grid(row=5, column=0, padx=5, pady=5)
        Label(self.left_frame, text="Scale z:").grid(row=6, column=0, padx=5, pady=5)

        Label(self.left_frame, text="").grid(row=7, column=0, padx=5, pady=20)

        Label(self.left_frame, text="Add x:").grid(row=8, column=0, padx=5, pady=5)
        Label(self.left_frame, text="Add y:").grid(row=9, column=0, padx=5, pady=5)
        Label(self.left_frame, text="Add z:").grid(row=10, column=0, padx=5, pady=5)

        # Grid btns in left frame #
        self.list_box_x.grid(row=0, column=1, padx=5, pady=5)
        self.list_box_y.grid(row=1, column=1, padx=5, pady=5)
        self.list_box_z.grid(row=2, column=1, padx=5, pady=5)

        self.entry_scaleX.grid(row=4, column=1, padx=5, pady=5)
        self.entry_scaleY.grid(row=5, column=1, padx=5, pady=5)
        self.entry_scaleZ.grid(row=6, column=1, padx=5, pady=5)

        self.entry_addX.grid(row=8, column=1, padx=5, pady=5)
        self.entry_addY.grid(row=9, column=1, padx=5, pady=5)
        self.entry_addZ.grid(row=10, column=1, padx=5, pady=5)

        # Grid labels in right frame #
        Label(self.right_frame, text="Azimuth:").grid(row=0, column=0, padx=5, pady=5)


        # Grid btns in right frame #
        self.entry_azimuth.grid(row=0, column=1, padx=5, pady=5)
        self.convex_hull_to_csv.grid(row=1, column=1, padx=0, pady=(300, 10))
        self.button_new.grid(row=2, column=1, padx=0, pady=(10, 10))

        # Disable all the z axis buttons #
        self.list_box_z.configure(state="disabled")
        self.entry_scaleZ.configure(state="disabled")
        self.entry_addZ.configure(state="disabled")

        # Disable the convex_to_csv btn #
        self.convex_hull_to_csv.configure(state="disabled")

    def popup_window(self):
        # Error for the user - abnormal csv
        self.popup = Toplevel()
        self.popup.title("string in csv")
        self.popup.geometry("300x200")
        Label(self.popup, text="Can get only numbers in the csv, check it please.").pack(pady=20)
        Button(self.popup, text="Got it!", comand=self.popup.destroy).pack()

    def path_to_csv(self):
        '''
        read the first csv columns and let the user the option to choose the axes
        '''
        self.pathes = filedialog.askopenfilenames()
        if len(self.pathes) > 0:
            try:
                df = pd.read_csv(self.pathes[0])
                self.columns_name = df.columns.tolist()

                self.list_box_x['menu'].delete(0, 'end')
                self.list_box_y['menu'].delete(0, 'end')
                self.list_box_z['menu'].delete(0, 'end')

                for column in self.columns_name:
                    self.list_box_x['menu'].add_command(label=column, command=lambda value=column: self.x_axis_var.set(value))
                    self.list_box_y['menu'].add_command(label=column, command=lambda value=column: self.y_axis_var.set(value))
                    self.list_box_z['menu'].add_command(label=column, command=lambda value=column: self.z_axis_var.set(value))

                self.x_axis_var.set(self.columns_name[0])
                self.y_axis_var.set(self.columns_name[1])
                self.z_axis_var.set(self.columns_name[2])

                self.button_add_files.configure(state="normal")
                self.button_g.configure(state="normal")
                self.button_show.configure(state="normal")

            except Exception as e:
                print('doesnt chose csv files', e)

    def btn_3d_validity(self):
        if self.check_3d.get() == 1:
            self.able_3d()
        else:
            self.disable_3d()

    def btn_poly_validity(self):
        if self.check_poly.get() == 1:
            self.check_3d.set(0)
            self.disable_3d()

    def btn_axis_eq_validity(self):
        if self.check_axis_equal.get() == 1:
            self.check_3d.set(0)
            self.disable_3d()

    def able_3d(self):
        self.list_box_z.configure(state="normal")
        self.entry_scaleZ.configure(state="normal")
        self.entry_addZ.configure(state="normal")
        self.check_axis_equal.set(0)
        self.check_poly.set(0)
        self.fig = plt.figure(num=1)
        self.ax = self.fig.add_subplot(111, projection='3d')

    def disable_3d(self):
        self.list_box_z.configure(state="disabled")
        self.entry_scaleZ.configure(state="disabled")
        self.entry_addZ.configure(state="disabled")

    def relevant_axes_setter(self):
        '''
        set the axes per csv path
        '''
        self.x = self.df[self.x_axis_var.get()].to_numpy()
        self.y = self.df[self.y_axis_var.get()].to_numpy()
        if not (np.issubdtype(self.x.dtype, np.number) or np.issubdtype(self.y.dtype, np.number)):
            self.popup_window()
        if self.check_3d.get() == 1:
            self.z = self.df[self.z_axis_var.get()].to_numpy()

    def set_ax(self):
        if self.check_3d.get() == 1:
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            pass

    def scaling(self):
        self.x *= float(self.entry_scaleX.get())
        self.y *= float(self.entry_scaleY.get())
        if self.check_3d.get() == 1:
            self.z *= float(self.entry_scaleZ.get())

    def adding(self):
        self.x += int(self.entry_addX.get())
        self.y += float(self.entry_addY.get())
        if self.check_3d.get() == 1:
            self.z += float(self.entry_addZ.get())

    def azimuthing(self):
        angle = np.radians(float(self.entry_azimuth.get()))
        matrix = np.array([[np.cos(angle), np.sin(angle)],
                  [-np.sin(angle), np.cos(angle)]])
        for count in range(len(self.x)):
            xy = np.dot(matrix, np.array([[self.x[count]],
                                          [self.y[count]]]))
            self.x[count] = xy[0][0]
            self.y[count] = xy[1][0]

    def plot_3D(self, path):
        if self.check_scatter.get() == 1:
            self.ax.scatter(self.x, self.y, self.z, s=0.8, label=extract_last_part(path, '/'))
        else:
            self.ax.plot(self.x, self.y, self.z, label=extract_last_part(path, '/'))

    def plot_2D(self, path):
        if self.check_scatter.get() == 1:
            self.ax.scatter(self.x, self.y, s=0.8, label=extract_last_part(path, '/'))
        else:
            self.ax.plot(self.x, self.y, label=extract_last_part(path, '/'))

    def convex_hull_plotter(self):
        hull_list = np.vstack([self.convex_df[self.x_axis_var.get()], self.convex_df[self.y_axis_var.get()]]).T
        hull_list_convexed = ConvexHull(hull_list)
        index_list = np.append(hull_list_convexed.vertices, hull_list_convexed.vertices[0])  # contain the indexes of all the vertices to create a convexed shape
        final_polygon = np.vstack([hull_list[index_list, 0], hull_list[index_list, 1]])
        self.convex_x, self.convex_y = final_polygon[0], final_polygon[1]
        self.ax.plot(self.convex_x, self.convex_y)
        self.convex_hull_to_csv.configure(state="normal")

    def convex_to_csv(self):
        csv_polygon = pd.DataFrame({'X': self.convex_x,
                                    'Y': self.convex_y})
        path = filedialog.asksaveasfile(defaultextension='.csv')
        csv_polygon.to_csv(path.name)
        

    def plot_generative(self, path):
        if self.check_3d.get() == 1:
            self.plot_3D(path)
        else:
            self.plot_2D(path)

    def show_plot(self):
        if self.check_poly.get() == 1:
            self.convex_hull_plotter()
        if self.check_locations.get() == 1:
            self.plot_locations()
        if self.check_axis_equal.get() == 1:
            plt.axis('equal')
        plt.xlabel(self.x_axis_var.get())
        plt.ylabel(self.y_axis_var.get())
        plt.legend()
        plt.title('Super plot')
        plt.grid()
        plt.ion()
        plt.show()

    def generate_plot(self):
        for path in self.pathes:
            self.df = pd.read_csv(path)
            self.relevant_axes_setter()

            if int(self.entry_scaleX.get()) + int(self.entry_scaleY.get()) + int(self.entry_scaleZ.get()) != 3:
                self.scaling()
            if int(self.entry_addX.get()) + int(self.entry_addY.get()) + int(self.entry_addZ.get()) != 0:
                self.adding()
            if int(self.entry_azimuth.get()) != 0:
                self.azimuthing()
            if self.check_poly.get():
                self.convex_df = self.convex_df.append(self.df)

            self.plot_generative(path)

    def new_app(self):
        self.destroy()
        main()


def main():
    gui = MyApp()
    gui.mainloop()


if __name__ == '__main__':
    main()