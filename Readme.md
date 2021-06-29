This respository hosts the CrowdTangle automation project created for Professor Jennifer Pan and other researchers.

It uses Python and other packages to automate the task of accessing the CrowdTangle Chrome extension for a given list of articles and downloading data csv files for each social media (Facebook, Twitter, Reddit, Instagram).

One should follow the environment setup steps in the dependcies file first.
Then one should add their Facebook username and password into the 'cred.txt' on the first two lines, plain. I wasn't sure if it was necessary, but one can alter the script slightly to read from an encrypted file or from direct user input if they would like.
Before running the script, one should first input their articles into the 'input.csv' file so that each article link is placed in their own row without adornments.
To run the script, simply open command line/prompt/bash/etc. to the correct base directory, activate the correct environment (assuming one is setup), and run:
	python crowdtangle.py
	(python3 crowdtangle.py in some setups)

During execution, try not to disturb the mouse/keyboard too much. The program may slow down at points during exececution due to hard coded pauses (one may tweak this) or waiting for elements to load. If this happens,
simply wait for a bit, however, if it persists for too long and/or the script crashes, well, something's probably wrong. If this occurs, one can go into the code and/or run the script on different articles on different.
If issues persist, one can contact me at andrew.sy.tao@gmail.com (let's hope this doesn't happen :)

Happy Automating!