# import socket programming library
import socket
# import thread module
from _thread import *
import threading
import datetime
import re
from predict import predict_weather
print_lock = threading.Lock()
# thread fuction
def threaded(c):
    date_obj = 0
    while True:
        # data received from client
        data = c.recv(1024)
        if not data or data == 'EXIT':
            print('Bye')
            # lock released on exit
            print_lock.release()
            break
        
        data = str(data.decode('ascii'))
        if data == "name_received":
            #print("name received")
            #print("Sending area list")
            areas_list = "ALL_AREAS"
            c.send(areas_list.encode('ascii'))
        if data == "area_received":
            #Listening for the chosen area
            chosen_area = c.recv(1024)
            chosen_area = str(chosen_area.decode('ascii'))
            print("Area inputted: ", chosen_area)
            #RE WRITE WITH DATAFRAMES
            #check if chosen_area is within a list and return either a yes or no
            if chosen_area == "London":
                c.send("valid_area".encode('ascii'))
            else:
                c.send("wrong_area".encode('ascii'))

        if data == "parameter_received":
            #Send a list of parameters
            parameter_list = "ALL_PARAMETERS"
            c.send(parameter_list.encode('ascii'))
            chosen_parameter = c.recv(1024)
            chosen_parameter = str(chosen_parameter.decode('ascii'))
            print("Parameter inputted: ", chosen_parameter)


            #RE WRITE WITH DATAFRAMES
            #Check if parameter is within the list:
            if chosen_parameter == "Precipitation":
                c.send("valid_parameter".encode('ascii'))
            else:
                c.send("wrong_parameter".encode('ascii'))

        if data == "date_received":
            date = c.recv(1024)
            # Check if the received date is in the correct format
            print("Date inputted: ", date.decode('ascii'))

            if not re.match(r"^\d{2}/\d{2}/\d{4}$", date.decode()):
                c.send("wrong_date".encode('ascii'))
            else:
                # Validate the day and month parts of the date
                day, month, year = date.decode().split('/')
                if int(day) > 31 or int(month) > 12:
                    c.send("wrong_date".encode('ascii'))
                else:
                    # Convert the received date string to a datetime object
                    date_obj = datetime.datetime.strptime(date.decode(), "%d/%m/%Y")
                    # Get the current date
                    current_date = datetime.datetime.now()
                    # Compare the received date with the current date
                    if date_obj > current_date:
                        # The received date is in the future
                        c.send("valid_date".encode('ascii'))
                    else:
                        # The received date is in the past or present
                        c.send("wrong_date".encode('ascii'))
        if data == "requested_info":
            print(date_obj)
            predictions = predict_weather(date_obj)
            prediction_1 = predictions[5]
            c.send(str(prediction_1).encode('ascii'))
            c.send("Your requested weather".encode('ascii'))
            
        
    # connection closed
    c.close()

def Main():
    host = ""
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 54321
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to post", port)
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()
if __name__ == '__main__':
    Main()