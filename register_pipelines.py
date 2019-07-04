import os
import sys

# import pipeline register and event listeners
from lib.pipeline_register import PipelineRegister
import register_event_listeners

from pipelines.lookback import LookbackPipeline
from pipelines.display_info import DisplayInfoPipeline
from pipelines.display_feedbacks import DisplayFeedbacksPipeline
from pipelines.draw_face_labels import DrawFaceLabelsPipeline
from pipelines.lookback import LookbackPipeline
from pipelines.presence import PresencePipeline
from pipelines.recorder import RecorderPipeline
from pipelines.key_press import KeyPressPipeline
from pipelines.http import HttpPipeline
from modules.facerec.facerec_pg import FacerecPG

def register(conf: dict, runtime_vars: dict, video_capture):
    """register pipelines to be used by the application"""

    facerec = FacerecPG(conf['postgres'])
    storage = _prepare_storage({
        "screenshots": '{}/screenshots'.format(conf["storage"]),
        "recordings": '{}/recordings'.format(conf["storage"]),
    })

    # register your pipelines here
    pipelines = {
        'lookback': LookbackPipeline,
        'display_info': DisplayInfoPipeline,
        'display_feedbacks': DisplayFeedbacksPipeline,
        'draw_face_labels': (DrawFaceLabelsPipeline, facerec.findfaces),
        'presence': PresencePipeline,
        'http': HttpPipeline,
        'recorder': (RecorderPipeline, video_capture,
                                       storage['recordings'],
                                       conf['frame']['recordonstart']),
        'key_press': (KeyPressPipeline, storage['screenshots']),
    }

    if 'pipeline_env' in conf:
        for pipeline_name in conf['pipeline_env']:
            is_disabled = False
            if 'disable' in conf['pipeline_env'][pipeline_name]:
                is_disabled = conf['pipeline_env'][pipeline_name]['disable']

            if pipeline_name in pipelines:
                if is_disabled:
                    del pipelines[pipeline_name]
                    print('[INFO] pipeline disabled:', pipeline_name)
            else:
                print('[ERROR] invalid pipeline listed in `pipeline_env`:', pipeline_name)
                sys.exit(1)

    return PipelineRegister(pipelines, register_event_listeners.register(), runtime_vars)


def _prepare_storage(storage: dict):
    for key, path in storage.items():
        if not os.path.exists(path):
            print("- creating '{}' storage at {}".format(key, path))
            os.makedirs(path)

    return storage
