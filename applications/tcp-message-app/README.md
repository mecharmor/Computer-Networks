# Multithreaded Client/Server TCP Message APP With Primitive Sockets. 

* Description: TCP Client/Server app that uses the socket library in python to develop a server and client class that utilize these sockets in
talking with one another.
* Purpose: The purpose of this assignment is to better understand the TCP protocol with implementation of sockets and threading.
* Clear instructions about how to clone/download/install/execute the project
    * to clone the project go to Terminal (OSX/Linux) and type `git clone https://github.com/mecharmor/Networking-in-Python.git`
    * navigate to directory /applications/tcp-message-app/
    * once you are in the directory you can either double click the server.py and client.py or you can launch these in terminal by using the command 
    `python3 server.py` and `python3 client.py`. (Note: you must be in the directory of these files to launch)
    * WARNING: It is crucial that you start the server.py BEFORE the client.py. (For testing I used IP: `localhost`, and PORT: `8008`)

* Compatibility issues: This project was developed in python `3.7` if you run any version below `3` the program will fail.
* Challenges faced in assignment and euphoric moments:
    * This project was a very good learning experience for understanding sockets and their low level implementation. The amount of code
needed to complete this assignment was minimal since we were developing using `python 3.7` however it was very conceptual. I had to
stop myself multiple times while developing because I needed to diagram the flow of the program. Additionally, debugging became difficult
due to sockets being closed or connections dropped which challenged my error handling abilities. 
    * Overall my greatest challenge in this assignment was checking edge cases. When I thought the project was complete I managed to
    crash it in some way which revealed areas that needed proper error handling. I managed to get the channel to display live feed
of messages (EXTRA CREDIT?) but this proved difficult due to the input() block which forced me to create more threads to display.

## Sample Runs of options 4 and 5. EXTRA credit #2 included in second gif.

### [VIEW create channel and connect gif](https://github.com/sfsu-joseo/csc645-01-fall2019-projects-mecharmor/blob/master/applications/tcp-message-app/sample%20runs/create%20and%20connect%20to%20channel.gif)
 ![gif](https://github.com/sfsu-joseo/csc645-01-fall2019-projects-mecharmor/blob/master/applications/tcp-message-app/sample%20runs/create%20and%20connect%20to%20channel.gif)

### [VIEW Extra credit #2 live channel updates](https://github.com/sfsu-joseo/csc645-01-fall2019-projects-mecharmor/blob/master/applications/tcp-message-app/sample%20runs/connect%20to%20channel%20extra%20credit%20(2).gif)
 ![gif](https://github.com/sfsu-joseo/csc645-01-fall2019-projects-mecharmor/blob/master/applications/tcp-message-app/sample%20runs/connect%20to%20channel%20extra%20credit%20(2).gif)
