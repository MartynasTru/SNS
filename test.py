import tkinter as tk
import socket
from tkinter import *
import threading
from PIL import Image, ImageTk
import tkcalendar
import datetime
import time
import tkinter.simpledialog


class WeatherPredictor:
    def __init__(self, master):
        self.master = master
        master.title("Oracle - The Weather Predictor")

        # Load background image
        image = Image.open("white-cloud-blue-sky.jpg")
        photo = ImageTk.PhotoImage(image)
        self.background_label = tk.Label(master, image=photo)
        self.background_label.image = photo  # To prevent image from being garbage collected
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Set window size and center it
        window_width = 700
        window_height = 500
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = int((screen_width/2) - (window_width/2))
        y_coordinate = int((screen_height/2) - (window_height/2))
        master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.host = '127.0.0.1'
        self.port = 54321
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        self.message = "\n\nHi, I am Oracle the weather predictor."
        self.name_received = False
        self.area_list_received = False
        self.area_selected = False
        self.area_valid = False
        self.incorrect_area = False
        self.parameter_selected = False
        self.parameter_list_received = False
        self.incorrect_parameter = False
        self.date_selected = False
        self.incorrect_date = False

        self.label_intro = tk.Label(master, text=self.message, font=("Helvetica", 18), bg="#F2F2F2")
        self.label_intro.pack(pady=20)

        self.button_continue = tk.Button(master, text="Continue", command=self.handle_continue, font=("Helvetica", 14), bg="#337AB7", fg="#F2F2F2")
        self.button_continue.pack(pady=10)

        self.label_name = tk.Label(master, text="Firstly, what is your name?", font=("Helvetica", 16), bg="#F2F2F2")
        self.entry_name = tk.Entry(master, font=("Helvetica", 14))
        self.button_name = tk.Button(master, text="Submit", command=self.handle_name_submit, font=("Helvetica", 14), bg="#337AB7", fg="#F2F2F2")

    def handle_continue(self):
        self.s.send("continue".encode('ascii'))
        self.show_name()

    def show_name(self):
        self.label_intro.pack_forget()
        self.button_continue.pack_forget()
        self.label_name.pack()
        self.entry_name.pack(pady=10)
        self.button_name.pack(pady=10)

    def handle_name_submit(self):
        self.name = self.entry_name.get().strip()
        self.label_name.pack_forget()
        self.entry_name.pack_forget()
        self.button_name.pack_forget()
        self.label_greeting = tk.Label(self.master, text=f"Nice to meet you, {self.name}.", font=("Helvetica", 16), bg="#F2F2F2")
        self.label_greeting.pack(pady=20)
        self.name_received = True
        self.s.send("name_received".encode('ascii'))
        self.show_area_list()

    def show_area_list(self):
        self.label_greeting.pack_forget()
        self.label_area = tk.Label(self.master, text='Here is the list of available areas: ', font=("Helvetica", 16), bg="#F2F2F2")
        self.label_area.pack(pady=20)
        self.s.send("area_received".encode('ascii'))
        self.area_list = self.s.recv(1024)
        self.area_list = str(self.area_list.decode('ascii'))
        self.area_list_received = True
        self.listbox_area = tk.Listbox(self.master, selectmode='SINGLE', exportselection=0,bg="#F2F2F2",font=("Helvetica", 16))
        for area in self.area_list.split(','):
            self.listbox_area.insert('end', area)
        self.listbox_area.pack(pady=20)
        self.button_area = tk.Button(self.master, text="Select Area", command=self.handle_area_select, font=("Helvetica", 14), bg="#337AB7", fg="#F2F2F2")
        self.button_area.pack(pady=10)

    def handle_area_select(self):
        selected_index = self.listbox_area.curselection()
        if selected_index:
            self.selected_area = self.listbox_area.get(selected_index)
            self.area_selected = True
            self.incorrect_area = False
            self.s.send(self.selected_area.encode('ascii'))
            self.area_valid = self.s.recv(1024).decode('ascii') == "valid_area"
            self.show_parameter_list()
        else:
            self.incorrect_area = True
            self.label_error = tk.Label(self.master, text='Please select an area from the list.', font=("Helvetica", 14), fg="red", bg="#F2F2F2")
            self.label_error.pack(pady=10)

    def show_parameter_list(self):
        self.label_area.pack_forget()
        self.listbox_area.pack_forget()
        self.button_area.pack_forget()
        self.label_parameter = tk.Label(self.master, text='Please select the parameter you want to know:', font=("Helvetica", 16), bg="#F2F2F2")
        self.label_parameter.pack(pady=20)
        self.s.send("parameter_received".encode('ascii'))
        self.parameter_list = self.s.recv(1024)
        self.parameter_list = str(self.parameter_list.decode('ascii'))
        self.parameter_list_received = True
        self.listbox_parameter = tk.Listbox(self.master, selectmode='SINGLE', exportselection=0, font=("Helvetica", 14), width=30, height=10)
        for parameter in self.parameter_list.split(','):
            self.listbox_parameter.insert(END, parameter)
        self.listbox_parameter.pack(pady=10)
        self.button_parameter = tk.Button(self.master, text="Select Parameter", command=self.handle_parameter_select, font=("Helvetica", 14), bg="#337AB7", fg="#F2F2F2")
        self.button_parameter.pack(pady=10)

    def handle_parameter_select(self):
        selected_index = self.listbox_parameter.curselection()
        if selected_index:
            self.selected_parameter = self.listbox_parameter.get(selected_index)
            self.parameter_selected = True
            self.incorrect_parameter = False
            self.s.send(self.selected_parameter.encode('ascii'))
            self.parameter_valid = self.s.recv(1024).decode('ascii') == "valid_parameter"
            self.show_date_selector()
        else:
            self.incorrect_parameter = True
            self.label_error = tk.Label(self.master, text='Please select a parameter from the list.', font=("Helvetica", 14), fg="red", bg="#F2F2F2")
            self.label_error.pack(pady=10)




    def show_date_selector(self):
        if self.incorrect_parameter:
            self.label_parameter.pack()
            self.s.send("parameter_received".encode('ascii'))
            self.parameter_list = self.s.recv(1024)
            self.listbox_parameter = tk.Listbox(self.master, selectmode='SINGLE', exportselection=0)
            for parameter in self.parameter_list.split(','):
                self.listbox_parameter.insert('end', parameter)
            self.listbox_parameter.pack()
            self.button_parameter = tk.Button(self.master, text="Submit", command=self.handle_parameter_submit)
            self.button_parameter.pack()
            return

        self.s.send("date_received".encode('ascii'))
        self.label_date = tk.Label(self.master, text='Please select a date: ')
        self.cal = tkcalendar.Calendar(self.master, selectmode='day', year=2023, month=4, day=17) # Replace year, month, day with your desired default date
        self.button_date = tk.Button(self.master, text="Submit", command=self.handle_date_submit)
        self.label_date.place(x=100, y=50) # Adjust the position as needed
        self.cal.place(x=100, y=80) # Adjust the position as needed
        self.button_date.place(x=100, y=250) # Adjust the position as needed

    def handle_date_submit(self):
        self.date_user = self.cal.get_date().strip()
        self.date_user = datetime.datetime.strptime(self.date_user, "%m/%d/%y")
        self.date_user = self.date_user.strftime('%d/%m/%Y')
        self.label_date.destroy()
        self.cal.destroy()
        self.button_date.destroy()

        self.s.send(self.date_user.encode('ascii'))
        info = self.s.recv(1024).decode('ascii')
        print(info)
        if info == "valid_date":
            self.incorrect_date = False
            self.show_weather_report()
        elif info == "wrong_date":
            self.incorrect_date = True
            self.show_error_message("Please Select a Valid date")
            self.show_date_selector()
    def show_error_message(self, message):
        top = tk.Toplevel(self.master)
        top.geometry("200x100")
        top.title("Error")

        label = tk.Label(top, text=message)
        label.pack(pady=10)

        ok_button = tk.Button(top, text="OK", command=top.destroy)
        ok_button.pack(pady=10)
    def show_weather_report(self):
        if self.incorrect_date:
            print("yes1")
            self.label_date = tk.Label(self.master, text='Please select a date: ')
            self.cal = tkcalendar.Calendar(self.master, selectmode='day', year=2022, month=4, day=17) # Replace year, month, day with your desired default date
            self.button_date = tk.Button(self.master, text="Submit", command=self.handle_date_submit)
            self.label_date.place(x=100, y=50) # Adjust the position as needed
            self.cal.place(x=100, y=80) # Adjust the position as needed
            self.button_date.place(x=100, y=250) # Adjust the position as needed
            return
        self.label_wait = tk.Label(self.master, text="Calculating...", font=('Helvetica', 14))
        self.label_wait.pack(pady=10)
        self.master.update()
        
        # Schedule the next label to be shown after 1 second
        self.master.after(1000, self.show_predicting_label)

    def show_predicting_label(self):
        self.label_wait2 = tk.Label(self.master, text="\nPredicting...", font=('Helvetica', 14))
        self.label_wait2.pack(pady=10)
        self.master.update()
        
        # Schedule the next label to be shown after 1 second
        self.master.after(1000, self.show_counting_label)

    def show_counting_label(self):
        self.label_wait3 = tk.Label(self.master, text="\nCounting Stars...", font=('Helvetica', 14))
        self.label_wait3.pack(pady=10)
        self.master.update()
        
        # start a new thread to run the function
        t = threading.Thread(target=self.get_weather_data)
        t.start()

    def get_weather_data(self):
        self.s.send("requested_info".encode('ascii'))
        self.s.send(self.date_user.encode('ascii'))
        weather_data = self.s.recv(1024).decode('ascii')

        self.label_wait.pack_forget()
        self.label_wait2.pack_forget()
        self.label_wait3.pack_forget()

        # format weather_data to 2 decimal places
        weather_data_formatted = "{:.2f}".format(float(weather_data))

        self.label_report = tk.Label(self.master, text=f"Here is the weather report for London on {self.date_user}: \n There will be {weather_data_formatted} mm of rain",font=('Helvetica', 14))
        self.label_report.pack(pady=20)

    def handle_exit(self):
        self.master.destroy()

if __name__ == '__main__':
    root = Tk()
    app = WeatherPredictor(root)
    root.mainloop()
       

