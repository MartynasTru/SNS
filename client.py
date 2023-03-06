import socket

def Main():
    # local host IP ’127.0.0.1’
    host = '127.0.0.1'
    # Define the port on which you want to connect
    port = 12345
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # connect to server on local computer
    s.connect((host,port))
    # message you send to server
    message = "\n\nHi, I am Oracle the weather predictor."
    
    #Variables for looping back in case of wrong input
    ans = ""
    run = 0
    name_received = 0

    area_list_received = 0

    incorrect_area = 0
    area_selected = 0

    parameter_selected = 0
    incorrect_parameter = 0

    date_selected = 0
    incorrect_date = 0

    while True:

        if run == 0:
            # Static variables received from server during session
            area_list = ''
            area_user = ''
            
            parameter_list = ''
            parameter_user = ''

            date_user = ''
            # message sent to server
            s.send(message.encode('ascii'))
            # print the received message
            print(message)
            # ask the client whether he wants to continue
            ans = input('\nWould you like to learn about future weather?(y/n) :')
        else: 
            s.send("continue".encode('ascii'))
            ans = 'y'
        if ans == 'y':

            #If this loop started then no need to come back to intro
            run = 1

            if name_received == 0:
                # 1: Taking users name
                name = input('\nPerfect, firstly, what is your name? ')
                print(f'\nNice to meet you, {name}.')
                
                #Updating server that name was received
                s.send("name_received".encode('ascii'))
                name_received = 1

            if area_list_received == 1 and area_selected == 0:
                s.send("area_received".encode('ascii'))

            if area_list_received == 0:
            # Getting a list of names from the server
                s.send("area_received".encode('ascii'))
                area_list = s.recv(1024)
                area_list = str(area_list.decode('ascii'))
                area_list_received = 1
            

            if incorrect_area == 0 and area_selected == 0:

                print('Here is the list of available areas: ')
                print(area_list)
                area_user = input('Please select one of the areas:')
                print("area_user_input1:", area_user)
                s.send(area_user.encode('ascii'))

            if incorrect_area == 1 and area_selected == 0:

                print(f'\n{name}, please be more attentive, here is the list again:')
                print(area_list)
                area_user = input('Please select one of THESE areas:')
                print("area_user_input2:", area_user)
                s.send(area_user.encode('ascii'))    
            if area_selected == 0:
                #Checking if area is in the list
                area_valid = s.recv(1024)
                area_valid = str(area_valid.decode('ascii'))
                print("valid area:", area_valid)

            if area_valid == "valid_area" and area_selected == 0:
                print("AREA RECEIVED")
                area_selected = 1
            elif area_valid == "wrong_area" and area_selected == 0:
                incorrect_area = 1
                print("FAILED TO RECEIVE AREA")

            if area_selected == 1 and parameter_selected == 0:
                s.send("parameter_received".encode('ascii'))
                parameter_list = s.recv(1024)
                parameter_list = str(parameter_list.decode('ascii'))

                if incorrect_parameter == 0 and parameter_selected == 0:
                    
                    print(f'\n{name}, choose what precisely you would like to know:')
                    
                    print(parameter_list)
                    parameter_user = input('Please select one of the parameters: ')
                    s.send(parameter_user.encode('ascii'))
                
                if incorrect_parameter == 1 and parameter_selected == 0:
                    
                    print(f'\n{name}, you need to choose from the list:')

                    print(parameter_list)
                    parameter_user = input('Please select one of the parameters: ')
                    s.send(parameter_user.encode('ascii'))

                if parameter_selected == 0:    
                    parameter_valid = s.recv(1024)
                    parameter_valid = str(parameter_valid.decode('ascii'))

                #RE WRITE WITH DATAFRAMES
                if parameter_valid == "valid_parameter":
                    print("PARAMETER RECEIVED")
                    parameter_selected = 1
                else:
                    print("FAILED TO RECEIVE PARAMETER")
                    incorrect_parameter = 1

            if parameter_selected == 1 and date_selected == 0:
                s.send("date_received".encode('ascii'))
                
                if incorrect_date == 0 and date_selected == 0:
                    date_user = input(f'\n{name}, please choose the date in the following format (dd/mm/yyyy): ')
                    s.send(date_user.encode('ascii'))

                elif incorrect_date == 1 and date_selected == 0:  
                    date_user = input(f'\n{name}, You cant select date from the past or in another format, please try again (dd/mm/yyyy): ')
                    s.send(date_user.encode('ascii'))
                
                if date_selected == 0:
                    date_valid = s.recv(1024)
                    date_valid = str(date_valid.decode('ascii'))

                if date_valid == "valid_date":
                    print("DATE RECEIVED")
                    date_selected = 1
                else:
                    print("FAILED TO RECEIVE DATE")
                    incorrect_date = 1
            
            if area_selected == 1 and parameter_selected == 1 and date_selected == 1:
                print("Predicting...")
                print("\nCalculating...")
                print("\nCounting Stars...")
                
                #When received data from ML:
                s.send("requested_info".encode('ascii'))
                response = s.recv(1024)
                print(f"Results:\n {response}")

                ans = input("\nWould you like to do use my service again? (y/n)")
                if ans == 'y':
                    area_list_received = 0

                    incorrect_area = 0
                    area_selected = 0

                    parameter_selected = 0
                    incorrect_parameter = 0

                    date_selected = 0
                    incorrect_date = 0
                    continue
                else: 
                    break
            
            continue
        else:
            run = 0
            break

    # close the connection
    s.close()
if __name__ == '__main__':
    Main()

