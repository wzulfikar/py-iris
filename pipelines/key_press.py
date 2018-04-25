from datetime import datetime

import numpy as np
import cv2


class KeyPressPipeline:
    def __init__(self, pipeline_register,
                 screenshots_storage: str):
        self.p_reg = pipeline_register
        self.p_reg.require(self.__class__.__name__,
                           ['recorder', 'display_feedbacks'])

        # don't run the pipeline automatically
        self.defer = True

        self.storage = {
            'screenshots': screenshots_storage
        }

        self.window_enabled = self.p_reg.runtime_vars['window_enabled']
        self.demomode = self.p_reg.runtime_vars['demomode']

        self._rc = self.p_reg.pipelines['recorder']
        self._display_feedback = self.p_reg.pipelines['display_feedbacks']

    def process(self, frame: np.ndarray,
                # c arg is from `cv2.waitkey`
                c: int):

        # Hit 'q' on the keyboard to quit!
        if c == ord('q'):
            if self.window_enabled and self.demomode:
                self._display_feedback.display('demoalert')
            else:
                self.p_reg.runtime_vars['quitting'] = True

        elif c == ord('h'):
            self.p_reg.runtime_vars['flip_h'] = not self.p_reg.runtime_vars['flip_h']

        elif c == ord('v'):
            self.p_reg.runtime_vars['flip_v'] = not self.p_reg.runtime_vars['flip_v']

        elif c == ord('r'):
            self._rc.isrecording = not self._rc.isrecording
            if self._rc.isrecording:
                fps_record_adjustment = 2
                self._rc.start_recording(
                    int(self.p_reg.runtime_vars['current_fps']) + fps_record_adjustment)
                self._display_feedback.display('recordingstarted')
            else:
                self._rc.stop_recording()
                self._display_feedback.display('recordingstopped')

            print('[RECORDING] {}'.format(self._rc.isrecording))

        elif c == ord('s'):
            now = datetime.now()
            filename = '{}/{}_{}.jpg'.format(
                self.storage["screenshots"],
                now.strftime('%Y-%m-%d_%H%M%S'),
                now.microsecond)
            cv2.imwrite(filename, frame)
            self._display_feedback.display('screenshots')
            print('[SAVED] {}'.format(filename))
