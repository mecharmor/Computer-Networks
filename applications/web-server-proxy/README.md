# Web Proxy Server

- Cory Lewis

- Proxy Server
- Description: Proxy server that has levels of authentication for admins, managers, and normal users. Data will be cached and a history will be kept of when data is accessed and modified. admins can access all websites. managers can access most websites. normal users can access the smallest subset of websites.
- Purpose: This project has the purpose of learning basic implementations of proxy servers, building and parsing http responses/requests while also familiarizing ourselves with persistent vs non persistent http connections.

  - to clone the project go to Terminal (OSX/Linux) and type `git clone https://github.com/mecharmor/Networking-in-Python.git`
  - navigate to directory //applications/web-server-proxy
  - once you are in the directory you can either double click the server.py and client.py or you can launch these in terminal by using the command
    `python3 web-proxy-server.py` (web proxy) and `python3 proxy_server.py` (proxy server, type 'quit' to safely stop server). (Note: you must be in the directory of these files to run)
  - proxy server is defaulted to : `127.0.0.1` Port: `9000` (no need to set this)

- Compatibility issues: This project was developed in python `3.7` if you run any version below `3` the program will fail.
- Challenges faced in assignment and euphoric moments:
  This project was a major challenge for me mainly due to busy scheduling. I managed to get everything done given the many extensions given (thank you). I learned so much in terms of using python with websockets, building/parsing http requests/responses. I also learned how to handle JSON data so the server is persistent with ALL data. I created a httpHelper and Database class that help me accomplish my tasks more efficiently. To be honest my biggest challenge was importing modules in python, it became a major headache with so many classes and the pathing changing for different files. I know it sounds silly but truly that was the hardest part XD. Not sure if I can get extra credit for making the database persistent but that would be great :). Proxy-settings page adds/displays live data for all database interactions which also work with the proxy. So if you add a new manager or manager only site then a normal user will receive a `401` response. Thank you again for all the extensions :) (this was very needed due to mid terms + work)

- NOTE: database will rebuild if you delete contents or file itself.

## Sample Run

### [General Usage of proxy server](https://github.com/sfsu-joseo/csc645-01-fall2019-projects-mecharmor/blob/master/applications/web-server-proxy/test_run.gif)

![gif](https://github.com/sfsu-joseo/csc645-01-fall2019-projects-mecharmor/blob/master/applications/web-server-proxy/test_run.gif)
