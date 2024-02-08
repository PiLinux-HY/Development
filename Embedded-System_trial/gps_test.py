import gps
import time,os

session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        report = session.next()
        if report['class'] == 'TPV':
            os.system('clear')
            longitude = getattr(report,'lon', 0.0)
            lattitude = getattr(report,'lat', 0.0)

    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
