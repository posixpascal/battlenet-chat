# battlenet-chat

A **non-working** battle.net chat client written in TypeScript and Python. 
It aims to be a simple yet complete mobile chat application. 

The python server is a proxy to communicate with the battlenet server because Websockets can't do this.
Maybe I'll try to make a "standalone" app in the future but that's not a goal on my list at the moment.

The server is able to log into battle.net and receives messages (whispers) from friend contacts,
it then stores these messages inside a JSON file which is available through an HTTP server.
For the server to log in you need to obtain a specific token after login, I could not automate this in time but I certainly will in the future.

To get the token you need to launch `main.py` and view the console logs – it'll print the URL you need to open with your browser.
Once opened you'll need to log in, then the website tries to redirect you to: http://localhost:0/?<your-token-is-here> – since this obviously won't receive the python instance, you have to manually copy the token and paste it into `main.pyL40`.

# Other resources
I've used most of the ProtoBuf files from Eion Robb's "purple-battlenet" Pidgen Plugin (https://bitbucket.org/EionRobb/purple-battlenet/src).
The server side is based on HearthSim's python-bnet library (https://github.com/HearthSim/python-bnet).
I modified it to serve a flask instance as well as storing messages inside JSON files.

# Status
Unfortunately this is not a working chat client at the moment.


# License
Be aware of the HearthSim license

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                        Version 2, December 2004 

    Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 

    Everyone is permitted to copy and distribute verbatim or modified 
    copies of this license document, and changing it is allowed as long 
    as the name is changed. 

                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

    0. You just DO WHAT THE FUCK YOU WANT TO.