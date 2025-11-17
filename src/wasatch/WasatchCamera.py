import numpy as np
from pylablib.devices import IMAQ
from ..shared import ISU_value


class WasatchCamera():

    def __init__(self):

        gain = {
            "args": {
                "label": "Gain",
                "min_value": 0,
                "max_value": 255,
                "default_value": 187,
            },
            "unit": 1,
            "value": 187,
            "tooltip": "The gain for the Awaiba Dragster sensor is an inverse ADC gain (analog gain for step size of ADC) from -6 to 20dB.\n\nA higher setting produces a lower gain, but our firmware probably inverts this so that the highest setting creates more gain.",
            "type": "slider_int"
        }

        offset = {
            "args": {
                "label": "Offset",
                "min_value": 0,
                "max_value": 255,
                "default_value": 255,
            },
            "unit": 1,
            "value": 255,
            "tooltip": "The offset register handles the ADC black level offset.\n\nA lower value should increase the level of the baseline and a higher value would lower it closer to black.",
            "type": "slider_int"
        }

        int = {
            "args": {
                "label": "Int. time [us]",
                "min_value": 0,
                "max_value": 32767,
                "default_value": 90,
            },
            "unit": 1e-6,
            "value": 90,
            "tooltip": "The integration time is the collection time. Then it is sampled/held for readout.\n\nThe integration time can typically be anything 2us or more less than the line time.",
            "type": "input_int"
        }

        ltm = {
            "args": {
                "label": "Line time [us]",
                "min_value": 22,
                "max_value": 65535,
                "default_value": 100,
            },
            "unit": 1e-6,
            "value": 100,
            "tooltip": "The line time is a line period that includes the additional time needed between integrations for transfers/resets.\n\nThis line period establishes the maximum line rate that can be achieved.",
            "type": "input_int"
        }

        self.parameters = {
            "gain": gain,
            "offset": offset,
            "int": int,
            "ltm": ltm
        }

        self.cam = None

        self.nframes = 100

        self.acq_time = {
            "args": {
                "label": "Acq. time [ms]",
                "default_value": 100,
            },
            "unit": 1e-3,
            "value": 100
        }

        self.acq_name = "data"

        self.data = None

    def list_cameras(self):
        return IMAQ.list_cameras()

    def msg_cam(self, msg: str):
        if isinstance(self.cam, IMAQ.IMAQCamera):
            self.cam.serial_write(msg)
            return f"write: {msg}\n read: {self.cam.serial_readline()}"
        return "no camera selected"

    def update_parameters(self):
        if isinstance(self.cam, IMAQ.IMAQCamera):
            messages = f""
            for key, parameter in self.parameters.items():
                messages += self.msg_cam(f"{key} {parameter['value']}\r")
            return messages
        return "no camera selected"

    def I(self):
        if isinstance(self.cam, IMAQ.IMAQCamera):
            self.msg_cam(f"lsc 1\r")
            snap = self.cam.snap()
            self.msg_cam(f"lsc 0\r")
            return snap[0, :]
        return np.zeros(shape=2048)

    def set_parameter(self, key: str, value):
        self.parameters[key]["value"] = value
        if isinstance(self.cam, IMAQ.IMAQCamera):
            return self.update_parameters()
        return "no camera selected"

    def set_acq_time(self, acq_time):
        self.acq_time["value"] = acq_time
        # acq_time = nframes * frame_time = nframes * 100 * line_time
        self.nframes = int(ISU_value(self.acq_time) // (100 *
                                                    ISU_value(self.parameters["ltm"])))
        return f"nframes set to {self.nframes}"

    def select_cam(self, cam_id: str):
        if isinstance(self.cam, IMAQ.IMAQCamera):
            self.cam.close()
        self.cam = IMAQ.IMAQCamera(cam_id)
        messages = f""
        messages += self.msg_cam(f"init\r")
        messages += self.update_parameters()
        messages += f"using camera {cam_id}"
        return messages

    def acquire(self):
        if isinstance(self.cam, IMAQ.IMAQCamera):
            messages = f""
            messages += self.update_parameters()
            messages += self.msg_cam(f"lsc 1\r")
            self.cam.setup_acquisition(mode="sequence", nframes=self.nframes)
            self.cam.start_acquisition()
            self.cam.wait_for_frame(since="start", nframes=self.nframes)
            self.cam.stop_acquisition()
            messages += self.msg_cam(f"lsc 0\r")
            self.data = np.vstack(self.cam.read_multiple_images())
            np.save(f"{self.acq_name}.npy", self.data)
            return messages
        return "no camera selected"

    def close_cam(self):
        if isinstance(self.cam, IMAQ.IMAQCamera):
            self.cam.close()
