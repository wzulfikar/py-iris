import os

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

    if 'disable_pipelines' in conf:
        for disable_pipeline in conf['disable_pipelines']:
            if disable_pipeline in pipelines:
                del pipelines[disable_pipeline]
                print('[INFO] pipeline disabled:', disable_pipeline)
            else:
                print('[WARN] could not disable invalid pipeline:', disable_pipeline)

    return PipelineRegister(pipelines, register_event_listeners.register(), runtime_vars)


def _prepare_storage(storage: dict):
    for key, path in storage.items():
        if not os.path.exists(path):
            print("- creating '{}' storage at {}".format(key, path))
            os.makedirs(path)

    return storage
