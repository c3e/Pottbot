import pydle
import paho.mqtt.client as mqtt

CHANNEL = "#chaospott"
OPS_ONLY = True
print("Bot im Pot!")
class Pottbot(pydle.Client):
    """ This is a simple bot that will greet people as they join the channel. """

    def on_connect(self):
        super().on_connect()
        self.join(CHANNEL)

    @pydle.coroutine
    def is_admin(self, nickname, channel=CHANNEL):
        """
        Check whether or not a user has administrative rights for this bot.
        This is a blocking function: use a coroutine to call it.
        See pydle's documentation on blocking functionality for details.
        """

        if nickname in self.channels['#chaospott']['modes']['o']:
            return True
        return False

    @pydle.coroutine
    def on_channel_message(self, target, by, message):
        if target == CHANNEL:
            admin = yield self.is_admin(by)
            if message == "!GTFO":
                if admin:
                    self.message(CHANNEL, "Well, fuck you! I'm going home!")
                    self.quit()
                else:
                    self.message(CHANNEL, "Who the fuck are you?!")

            elif message.startswith("!MQTT"):
                cmd = message.split(" ")
                if (OPS_ONLY and admin) or not OPS_ONLY:
                    if len(cmd) < 2:
                        self.message(CHANNEL, "Usage: !MQTT <topic> <message>")
                    elif len(cmd) == 2:
                        # READ MQTT TOPIC
                        pass

                    elif len(cmd) >= 3:
                        # PUBLISH ON MQTT TOPIC
                        msg = " ".join(cmd[2:])
                        mqtt.single(cmd[1], payload=msg, qos=0, retain=False, hostname="localhost",
                                    port=1883, client_id="Pottbot", keepalive=60, will=None, auth=None, tls=None,
                                    protocol=mqtt.MQTTv311, transport="tcp")
                else:
                    self.message(CHANNEL, "You're not allowed to do this.")
            elif "Kaffee" in message:
                self.message(CHANNEL, "Heisser, schwarzer, extrem leckerer Kaffe, echt jetz!")
            else:
                pass


def run_bot():
    client = Pottbot('Pottbot')
    client.connect('irc.hackint.net', 6697, tls=True)
    client.handle_forever()

if __name__ == '__main__':
    run_bot()
