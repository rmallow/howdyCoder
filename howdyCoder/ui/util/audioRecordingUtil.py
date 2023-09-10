from queue import Queue
import tempfile
import typing

import soundfile
import sounddevice
import numpy

assert numpy


class RecordingObject:
    def __init__(self):
        self.keep_running = True
        self._queue = Queue()

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        self._queue.put(indata.copy())

    def record(self, device_num: int) -> str:
        device_info = sounddevice.query_devices(device_num, "input")
        # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info["default_samplerate"])
        channels = device_info["max_input_channels"]
        # Make sure the file is opened before recording anything:
        # TODO: CHANGE DIR TO NONE
        filename = tempfile.mktemp(
            prefix="delme_rec_unlimited_",
            suffix=".wav",
        )
        with soundfile.SoundFile(
            filename,
            mode="x",
            channels=channels,
            samplerate=samplerate,
            subtype=soundfile.default_subtype("WAV"),
        ) as file:
            with sounddevice.InputStream(
                samplerate=samplerate, device=device_num, callback=self.callback
            ):
                while self.keep_running:
                    file.write(self._queue.get())
        return filename


def getInputDevices() -> typing.List[typing.Dict[str, typing.Any]]:
    devices = sounddevice.query_devices()
    return [d for d in devices if d["max_input_channels"] > 0]
