from adaflow.av.utils import gst_video_format_from_string, get_num_channels, NumpyArrayEncoder
from adaflow.av.metadata.flow_json_meta import flow_meta_add, flow_meta_get, flow_meta_remove
from .av_data_frame import AVDataFrame

import gi
gi.require_version('Gst', '1.0')
gi.require_version("GstVideo", "1.0")
gi.require_version('GObject', '2.0')

from gi.repository import GObject, Gst, GstVideo


class AVDataPacket:
    def __init__(self, buffer: Gst.Buffer, caps: Gst.Caps):
        """
        Construct AVDataPacket instance from Gst.Buffer and Gst.Caps.
        :param buffer:Gst.Buffer to which metadata is attached and retrieved.
        :param caps:Gst.Caps from which video information is obtained.
        """
        self.__buffer = buffer
        self.__caps = caps
        #cal frame size
        struct = caps.get_structure(0)
        self.width = struct.get_int("width").value
        self.height = struct.get_int("height").value
        video_format = gst_video_format_from_string(struct.get_value('format'))
        self.channel = get_num_channels(video_format)
        self.frame_size = self.width * self.height * self.channel
        #cal buffer size
        self.buffer_size = Gst.Buffer.get_size(self.__buffer)
        #cal frame num
        self.frame_num = int(self.buffer_size/self.frame_size)
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.frame_size:
            frame = AVDataFrame(buffer=self.__buffer, caps=self.__caps, offset=self.i * self.frame_size)
            self.i += 1
            return frame
        else:
            raise StopIteration

    def __len__(self):
        return self.frame_num



