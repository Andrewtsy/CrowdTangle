This respository hosts the CrowdTangle automation project created for Professor Jennifer Pan and other researchers.

It uses Python and other packages to automate the task of accessing the CrowdTangle Chrome extension
for a given list of articles and downloading data csv files for each social media (Facebook, Twitter, Reddit, Instagram).

Steps for setup:
	1. You should follow the environment setup steps in the dependencies file first.
	2. Next, follow the instructions on setting up the images folder (open the file called images_setup_instructions)
	3. You should add your Facebook username and password into the 'cred.txt' on the first two lines.
		Note: I wasn't sure if it was necessary, but you can alter the script slightly to read 
		      from an encrypted file or from direct user input if you would like.
	4. Before running the script, you should input your articles into the 'input.csv' file
	   so that each article link is placed in their own row without adornments.
	5. To run the script, simply open your command line interface (CLI) to the correct base directory,
	   activate the correct environment (assuming one is setup), and run:
	
		python crowdtangle.py

During execution, try not to disturb the mouse/keyboard too much. The program may slow down at points during exececution
due to hard coded pauses (one may tweak this) or waiting for elements to load. If this happens,
simply wait for a bit, however, if it continues for too long and/or the script crashes, well,
something's probably wrong. If issues persist, you can contact me at andrew.sy.tao@gmail.com

Happy Automating!

____________________________________________________________________________________________________