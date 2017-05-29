__author__ = 'letessier'

import sys
import logging
import json
import urllib.request
from time import sleep
from BlinkTool import Blink


# Debugging config, used during testing
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

CODE_INSEE_NANTES = 4410900
DEPARTEMENT = 44
RAIN_COLORS = ["#FFFF66", "#C8ECF3", "#7FD2E4", "#268DA9", "#1A4555"]

VIGILANCE_COLOR_NAME = ["???","vert", "jaune","orange","rouge"]
VIGILANCE_COLOR_CODE = ["#000000","#004400", "#ffff00","#ff8c00","#ff0000"]

LED_VIGI=2
LED_RAIN=1


def check_vigilance():
    # source
    # http://www.touteladomotique.com/forum/viewtopic.php?f=18&t=14699&start=36
    url = 'http://api.domogeek.fr/vigilance/%s/all' % (str(DEPARTEMENT))

    # try:
    # fetch the data
    logging.debug("request %s" % url)
    response = urllib.request.urlopen(url)
    result = json.loads(response.readall().decode('utf-8'))

    # extract the color
    color = result['vigilancecolor']
    logging.debug("color %s" % color)
    risk = result['vigilancerisk']
    logging.debug("vigilancerisk %s" % risk)
    # b = Blink()
    # if color == "vert":
    #     b.rgbHex()
    # elif color == "jaune":
    #     b.rgbHex()
    # elif color == "orange":
    #     b.alert()
    # elif color == "rouge":
    #     b.alert()


def check_pluie():
    # source
    # https://github.com/Cqoicebordel/widget-meteo/blob/master/pluie.php
    url = 'http://mobile.meteofrance.com/ws/getPluie/%s.json' % (str(CODE_INSEE_NANTES))

    # fetch the data
    logging.debug("request %s" % url)
    response = urllib.request.urlopen(url)
    result = json.loads(response.readall().decode('utf-8'))

    nom_ville = result['result']['ville']['nom']
    logging.debug("ville : %s" % (nom_ville))

    b = Blink()
    #b.off()

    # vigilance
    vigilanceIndex = int(result['result']['ville']['vigilanceCouleur'])
    if (vigilanceIndex == 1 or vigilanceIndex == 2):
        color = VIGILANCE_COLOR_CODE[vigilanceIndex]
        logging.debug("vigilance : %s" % (VIGILANCE_COLOR_NAME[vigilanceIndex]))
        logging.debug("color : %s" % (color))
        b.rgbHex(color, LED_VIGI)
    elif (vigilanceIndex == 3 or vigilanceIndex == 4):
        color = VIGILANCE_COLOR_CODE[vigilanceIndex]
        logging.debug("vigilance : %s" % (VIGILANCE_COLOR_NAME[vigilanceIndex]))
        logging.debug("alert : %s" % (color))
        b.alert(color, LED_VIGI)

    # pluie 1H
    resarray = result['result']['intervalles']
    cumul=0
    for r in resarray:
        date = r['date']
        pluie = int(r['value'])
        cumul += pluie
        logging.debug("%s : %s" % (date, pluie))
        if (pluie <= 1): b.off(0, LED_RAIN)
        elif (pluie < 3): b.blink(RAIN_COLORS[pluie], 2, LED_RAIN)
        elif (pluie < 5): b.alert(RAIN_COLORS[pluie], LED_RAIN)
        # https://gist.github.com/flyinva/5930271080a895f52837

    if (cumul <=10) :
        b.blink(RAIN_COLORS[0], 1, LED_RAIN)

def main():
    b = Blink()
    b.test()

    while True:
        # check_vigilance()
        # sleep(10)
        # b.off()

        try:
            check_pluie()
        except:
            pass
        sleep(10)
        #b.off()


if __name__ == "__main__":
    sys.exit(main())
