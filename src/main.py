import logging
import sys
import threading
from datetime import datetime
from gpiozero import MotionSensor
from signal import pause
import tomli
from picamera2 import Picamera2
from pathlib import Path

handler = logging.StreamHandler(sys.stderr)
_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)
_log.addHandler(handler)

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)

pir = MotionSensor(4)

mutex = threading.Lock()

with open("settings.toml", mode="rb") as f:
    data = tomli.load(f)
    if "storage" in data and "path" in data["storage"]:
        path = data["storage"]["path"]
    else:
        path = "/media/usb0/"

    if not path.endswith("/"):
        path = path + "/"

    if "storage" in data and "datetime_format" in data["storage"]:
        fmt = data["storage"]["datetime_format"]
    else:
        fmt = "%Y-%d-%mT%H_%M_%S"


def capture_photo():
    # gpiozero runs functions in separate threads.
    # Capturing an image may take longer than the time delay on the PIR sensor
    # and in that case, let's not stack up image processing, so do nothing if the lock is already held.
    if mutex.locked():
        _log.warning("mutex locked: skipping capture")
        return

    try:
        mutex.acquire()

        file_name = f'{datetime.utcnow().strftime(fmt)}.jpg'
        file_path = Path(path) / file_name
        _log.info(f"saving to: {file_path}")

        picam2.start()
        picam2.capture_file(f"{file_path}")
        picam2.stop()
    finally:
        mutex.release()


pir.when_activated = capture_photo

pause()
