# P2P BitTorrent App

- Cory Lewis

- Description: P2P Swarm. A single tracker owns the information to access the swarm. When a new peer connects to the tracker it will be given the list of peers in the swam and it will also be added to that list of peers in the swarm. Peers that are leeching are downloading pieces of the file. Peers that are Seeding have the entire file and will upload pieces upon request. 
- Purpose: The purpose of this project was to familiarize ourselves with the logic and flow behind decentralized P2P networks. Understanding the flow and also how file sharing occurs is fundamental in this project.

  - to clone the project go to Terminal (OSX/Linux) and type `git clone https://github.com/sfsu-joseo/csc645-01-fall2019-projects-mecharmor.git`
  - navigate to directory //applications/peer-to-peer-app or view this repo at URL: https://github.com/sfsu-joseo/csc645-01-fall2019-projects-mecharmor/tree/master/applications/peer-to-peer-app
  - once you are in the directory you can run the tracker and peer in the terminal by using the command
    `python3 tracker.py` (Tracker) and `python3 peer.py`, Note: you MUST run tracker before you run peer.py because the peer is connecting to the tracker server.
  - proxy server is defaulted to : `127.0.0.1` Port: `5000` (no need to set this)

- Compatibility issues: This project was developed in python `3.7` if you run any version below `3` the program will fail.
- Challenges faced in assignment and euphoric moments:
  This project overall was very difficult to implement. Once again the challenge was the amount of time I could dedicate to the project. This semester I bounced between C++, Swift, Objective-C, React.js, Node.js, SQL, JavaScript, Python, Scheme, Ruby, Prolog, lots of bash scripting, some C#. My brain is honestly fried... I tried my best to follow the template but I would consistently find myself asking what this method would do and have to trace code to see what type of data I was being passed. Handling data types in python was honestly the most frustrating because I understood exactly what needed to be done in certain methods but I couldn't tell if it was a list, dictionary, Swarm obj, resource obj... There have been a few weekends I took a hard hit at this project and tried to make progress before I ran out of time but even with diagrams in class and the notes I had taken I honestly didn't know what to write. Handling bits in python is completely new to me consiering I only dealt with basic file i/o and trying to split a file into pieces became a headache. The torrent file provided the hashes in hex so determining how to convert that or properly parse the string was also slightly confusing. I hacked at my server and client classes for a while because testing on a local machine is problematic and spinning up a few linux vm's on my iMac was going to cripple my development time. Overal I will say that I gained very valuable knowledge about P2P decentralized networks and I am thankful for that knowledge however, I think the amount of things I had to build from the ground up put me in an awkward place of using an untested feature on a new feature which in turn caused slippery slopes with exceptions and some extremely challenging networking errors that gave little to no insight as to why a connection would be dropped or a blocking receive call getting null data. it's 2 a.m so i'm sorry if I sound blunt. Have a great winter break! Thank you for this class! I do not regret taking it at all and in fact I feel much more comfortable working with networks in general.

- IMPORTANT NOTE: if this saves some grading time the features I implemented are the following:
   peer.py
      - connects to the tracker successfully and fetches the necessary data to display on the screen
      - torrent file is parsed and used as the requested resource to the tracker
   tracker.py
      - tracker is fully implemented and will add new peers to the swarm
   swarm.py
      - this class is fully implemented
   resource.py
      - this class is mostly implemented but I need to write the data to a file. not sure if I was supposed to implement that in here or not
   logging.py
      - I created a verbose logging class so the entire network will essentially dump critical errors into a .txt file so you can do `tail -f log.txt` to see all the new messages without bogging down your main terminal window. compeltely unnecessary but I figured it would help in troubleshooting
   client.py
      - this was basically a copy paste with some slight modifications so the concept of a client was more generalized
   server.py
      - also a copy and paste but with some slight modifications
   message.py
      - this class is untouched. I was not sure what we would need to implement here other than adding get/set methods
   
   I hope this is helpful :)


