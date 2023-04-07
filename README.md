### ELEC0088 Software for Network and Services Design (SNS) - 2022/23
This is a ML-driven chatbot designed for educational purposes. The task of the bot is to answer simple questions regarding weather predictions with a use of a machine learning model. The user asks a pre-defined question, the client app deconstructs the question, sends a TCP-based request to the server, and the server responds with a future weather prediction based on its pre-trained neural network which in this case is a bidirectional long short-term memory neural network. 

The project is organized as follows:

- [client.py](client.py) - contains a Python code for the client app which uses the socket library to establish a TCP connection with the server and send requests about the weather predictions

- [server.py](server.py) - contains a Python code for the server app which is supposed to be run on a separate machine. It listens on an open TCP port for clients to connect. It can access the [model.h5](model.h5) file and use the pre-trained model to answer the prediction questions. Then it sends the results back to the client and closes the TCP connection.

- [model.h5](model.h5) - this is the pre-trained LSTM model

<span style="color:#E75480">TODO:</span> 
for today
- go through all files to see whats useful.. choose the files and delete the rest
- decide if we have enough stuff
- cosmetic changes to all files 
- add files to readme description
- add description of how to test code in readme


For Lazim:
- add comments to the code and make it relatively readable (in the classical_regression_models file)
- the bottom code cell in your file gives an error so probably either delete it or make it work
- explain your models in the report ... maybe just put it in METHODOLOGY section at the beginning and be like "oh we first decided to explore what models we can use and so we started with classical / statistical models and then we decided LSTM was either better or we wanted to learn how it works and hence we used it
 


