import tkinter as tk
import socket
from datetime import datetime
from tkinter import *
import tkcalendar


class WeatherPredictor:
    def __init__(self, master):
        self.master = master
        master.title("Oracle - The Weather Predictor")
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

        self.label_intro = tk.Label(master, text=self.message)
        self.label_intro.pack()

        self.button_continue = tk.Button(master, text="Continue", command=self.handle_continue)
        self.button_continue.pack(pady=10)

        self.label_name = tk.Label(master, text="Firstly, what is your name?")
        self.entry_name = tk.Entry(master)
        self.button_name = tk.Button(master, text="Submit", command=self.handle_name_submit)

    def handle_continue(self):
        self.s.send("continue".encode('ascii'))
        self.show_name()

    def show_name(self):
        self.label_intro.pack_forget()
        self.button_continue.pack_forget()
        self.label_name.pack()
        self.entry_name.pack()
        self.button_name.pack()

    def handle_name_submit(self):
        self.name = self.entry_name.get().strip()
        self.label_name.pack_forget()
        self.entry_name.pack_forget()
        self.button_name.pack_forget()
        self.label_greeting = tk.Label(self.master, text=f"Nice to meet you, {self.name}.")
        self.label_greeting.pack()
        self.name_received = True
        self.s.send("name_received".encode('ascii'))
        self.show_area_list()

    def show_area_list(self):
        self.label_greeting.pack_forget()
        self.label_area = tk.Label(self.master, text='Here is the list of available areas: ')
        self.label_area.pack()
        self.s.send("area_received".encode('ascii'))
        self.area_list = self.s.recv(1024)
        self.area_list = str(self.area_list.decode('ascii'))
        self.area_list_received = True
        self.listbox_area = tk.Listbox(self.master, selectmode='SINGLE', exportselection=0)
        for area in self.area_list.split(','):
            self.listbox_area.insert('end', area)
        self.listbox_area.pack()
        self.button_area = tk.Button(self.master, text="Submit", command=self.handle_area_submit)
        self.button_area.pack()

    def handle_area_submit(self):
        selected_areas = self.listbox_area.curselection()
        if not selected_areas:
            return
        self.area_user = self.listbox_area.get(selected_areas[0])
        self.listbox_area.pack_forget()
        self.button_area.pack_forget()
        self.label_area.pack_forget()
        self.s.send(self.area_user.encode('ascii'))
        self.area_valid = self.s.recv(1024).decode('ascii') == "valid_area"
        if not self.area_valid:
            self.incorrect_area = True
        self.show_parameter_list()

    def show_parameter_list(self):
        if self.incorrect_area:
            self.label_area.pack()
            self.s.send("area_received".encode('ascii'))
            self.area_list = self.s.recv(1024)
            self.area_list = str(self.area_list.decode('ascii'))
            self.listbox_area = tk.Listbox(self.master, selectmode='SINGLE', exportselection=0)
            for area in self.area_list.split(','):
                self.listbox_area.insert('end', area)
            self.listbox_area.pack()
            self.button_area = tk.Button(self.master, text="Submit", command=self.handle_area_submit)
            self.button_area.pack()
            return

        self.label_parameter = tk.Label(self.master, text='Select a parameter: ')
        self.label_parameter.pack()
        self.s.send("parameter_received".encode('ascii'))
        self.parameter_list = self.s.recv(1024)
        self.parameter_list = str(self.parameter_list.decode('ascii'))
        self.listbox_parameter = tk.Listbox(self.master, selectmode='SINGLE', exportselection=0)
        for parameter in self.parameter_list.split(','):
            self.listbox_parameter.insert('end', parameter)
        self.listbox_parameter.pack()
        self.button_parameter = tk.Button(self.master, text="Submit", command=self.handle_parameter_submit)
        self.button_parameter.pack()
        self.parameter_list_received = True
    def handle_parameter_submit(self):
        selected_parameters = self.listbox_parameter.curselection()
        if not selected_parameters:
            return
        self.parameter_user = self.listbox_parameter.get(selected_parameters[0])
        self.listbox_parameter.pack_forget()
        self.button_parameter.pack_forget()
        self.label_parameter.pack_forget()
        self.s.send(self.parameter_user.encode('ascii'))
        self.parameter_valid = self.s.recv(1024).decode('ascii') == "valid_parameter"
        if not self.parameter_valid:
            self.incorrect_parameter = True
        self.show_date_selector()

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
        self.label_date = tk.Label(self.master, text='Please enter a date in (dd/mm/yyyy) format: ')
        self.entry_date = tk.Entry(self.master)
        self.button_date = tk.Button(self.master, text="Submit", command=self.handle_date_submit)
        self.label_date.pack()
        self.entry_date.pack()
        self.button_date.pack()

    def handle_date_submit(self):
        self.date_user = self.entry_date.get().strip()
        self.label_date.pack_forget()
        self.entry_date.pack_forget()
        self.button_date.pack_forget()
        self.s.send(self.date_user.encode('ascii'))
        info = self.s.recv(1024)
        if info == "invalid_date":
            self.incorrect_date is True
        self.show_weather_report()

    def show_weather_report(self):
        if self.incorrect_date:
            self.label_date.pack()
            self.entry_date.pack()
            self.button_date.pack()
            return
        self.s.send("requested_info".encode('ascii'))
        self.report = self.s.recv(1024)
        self.report = str(self.report.decode('ascii'))
        self.label_report = tk.Label(self.master, text=self.report)
        self.label_report.pack()

    def handle_exit(self):
        self.master.destroy()

           

if __name__ == '__main__':
    root = Tk()
    app = WeatherPredictor(root)
    root.mainloop()