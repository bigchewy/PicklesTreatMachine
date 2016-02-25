# PicklesTreatMachine
Remote treat dispenser that dispenses treats, takes video and sends it back, making the girlfriend happy


Creator: Eric Page

Contact: eric.w.page.dev@gmail.com

URL: www.playwithpickles.com

Code: https://github.com/bigchewy/PicklesTreatMachine

Mailing List: https://groups.google.com/forum/#!forum/remote-treat-dispenser

Issues: right here on Github - https://github.com/bigchewy/PicklesTreatMachine/issues

The user can currently trigger the machine via
1) email
2) anything that can send an event to an MQTT server

The email listener simply listens to a specific email address and then sends an MQTT message

The MQTT listener listens to the MQTT server. When a message is sent to the designated MQTT feed, the treat dispensing process is activated

