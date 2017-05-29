import subprocess
import logging

__author__ = 'letessier'

blink1_path = "X:/depots/todbot/blink1/windows/scripts/blink1-tool"  # path to blink1-tool
milli = 1000  # duration for blink commands

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

LED_ALL=0
LED_TOP=1
LED_BOTTOM=2


# Wrapper for blink1-tool, only rgb and off commands supported
class Blink(object):

    def test(self):
        # subprocess.check_call([blink1_path,
        #                     "--white", "--blink", "5", "-m", "50", "-t", "50"],
        #                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.blink("#000000", 3, LED_TOP)
        self.blink("#000000", 3, LED_BOTTOM)


    # takes rgb values in a list
    def rgb(self, rgb, m):
        subprocess.check_call([blink1_path,
                            "--rgb", ','.join(str(x) for x in rgb), "-m", str(m)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    def rgbHex(self, rgbHex, led):
        subprocess.check_call([blink1_path,
                            "--rgb", rgbHex, "-m", str(milli), "-l", str(led)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    def blink(self, rgbHex, nTimes, led):
        subprocess.check_call([blink1_path,
                            "--rgb", rgbHex, "--blink", str(nTimes), "-m", str(500), "-l", str(led)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    def flash(self, rgbHex, nTimes, led):
        subprocess.check_call([blink1_path,
                            "--rgb", rgbHex, "--blink", str(nTimes), "-m", str(50), "-t", str(100), "-l", str(led)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    def alert(self, rgbHex, led):
        nTimes = 5
        self.blink(rgbHex, nTimes, led)
        self.rgbHex(rgbHex, led)


    # shuts off the light
    def off(self, m=milli, led=LED_ALL):
        subprocess.check_call([blink1_path,
                            "--off", "-m", str(milli), "-l", str(led)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
