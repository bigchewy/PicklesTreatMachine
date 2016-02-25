# PicklesTreatMachine
Remote treat dispenser that a user anywhere in the world can trigger to dispense treats, takes video and sends it back. This makes my girlfriend and Pickles happy.

Creator: Eric Page

Contact: eric.w.page !@! gmail

URL: www.playwithpickles.com

Code: https://github.com/bigchewy/PicklesTreatMachine

Mailing List: https://groups.google.com/forum/#!forum/remote-treat-dispenser

Issues: right here on Github - https://github.com/bigchewy/PicklesTreatMachine/issues
message is sent to the designated MQTT feed, the treat dispensing process is activated

The process
1) Trigger the machine. It can currently can be triggered via
 a) an email sent to an email address, specified in the config file. The email listener simply listens for the email and sends an event to an MQTT server, currently Adafruit IO 
 OR
 b) send an event directly to an MQTT server 
 
2) Activate the speakers. It plays whatever is in makeNoise.wav e.g. your voice saying, "[your dog's name], come get your treat!"

3) Activate the stepper motor. The stepper motor turns a cylinder one full revolution. The cylinder, which should contain treats, is angled slightly down such that gravity pulls the treats down to one end. At that end is a opening, through which the treats drop onto a chute, and then onto the ground

4) Activate the motion detection system. Currently using code built off of pyimagesearch.com's amazing tutorials

5) If motion is detected (aka the dog enters the view), take and then save a video

6) Send that video back to the person who initially triggered the event, right now via email.

The Illustrator files can be used to create your own Treat Machine, perhaps using a laser cutter. The Base is an 18x24" sheet and I generally use 1/4" acrylic. The outer cylinder is 12" long and has a 3" outer diameter. The inner cylinder is 8.5" long and has a 2.5" outer diameter. Both cylinders are 1/4" thickness. 

The base is fairly straightforward but the cylinders require a decent amount of laser cutting or machining skill for it to look nice. 
