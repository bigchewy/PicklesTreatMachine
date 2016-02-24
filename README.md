# PicklesTreatMachine
Remote treat dispenser that dispenses treats, takes video and sends it back, making the girlfriend happy

It currently can be triggered via
1) email
2) MQTT server

The email listener simply listens to a specific email address and then sends an MQTT message

The MQTT listener listens to the MQTT server. When a message is sent to the designated MQTT feed, the treat dispensing process is activated
