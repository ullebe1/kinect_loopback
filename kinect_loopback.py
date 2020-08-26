#!/usr/bin/env python
import signal
import os
import glob
import atexit
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
import virtualvideo
import numpy as np
import subprocess

def signal_handler(sig, frame):
    exit_handler()

signal.signal(signal.SIGINT, signal_handler)

try:
    from pylibfreenect2 import OpenGLPacketPipeline
    pipeline = OpenGLPacketPipeline()
except:
    try:
        from pylibfreenect2 import OpenCLPacketPipeline
        pipeline = OpenCLPacketPipeline()
    except:
        from pylibfreenect2 import CpuPacketPipeline
        pipeline = CpuPacketPipeline()
print("Packet pipeline:", type(pipeline).__name__)


fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No Kinects connected!")
    sys.exit(1)

serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

print('Registering listeners')
listener = SyncMultiFrameListener(FrameType.Color)
# Register listeners
device.setColorFrameListener(listener)

print('Starting streams')
device.startStreams(rgb=True, depth=False)


#frames = listener.waitForNewFrame()

class MyVideoSource(virtualvideo.VideoSource):
    def __init__(self):
        size = np.empty([1920,1080]).shape
        self._size = size

    def img_size(self):
        return self._size

    def fps(self):
        return 30

    def generator(self):
        
        while True:
            frames = listener.waitForNewFrame()
            color = frames["color"]

            yield color.asarray()[:,:,:3]
            listener.release(frames)

def exit_handler():
    device.stop()
    device.close()
    try:
        print('Not enough priviledges, exiting')
        subprocess.run(['sudo', 'modprobe', '-r', 'v4l2loopback'], check=True)
    except Exception as e:
        print(e)
        sys.exit(1)
    print('V4L2Loopback devices successfully cleaned up')


print('Initializing Kinect')
vidsrc = MyVideoSource()
print('Kinect initialized')
videodevices = glob.glob("/dev/video*")
videodevices.sort(reverse=True)
loopbackdeviceindex = int(videodevices[0][-1:]) + 1
print('Adding new loopback device for kinect as \'{0}\''.format(loopbackdeviceindex))
try:
    subprocess.run(['sudo', 'modprobe', 'v4l2loopback', 'video_nr={0}'.format(loopbackdeviceindex), 'card_label="Microsoft XBox Kinect V2"', 'exclusive_caps=1'], check=True)
except Exception as e:
    print(e)
    exit_handler()
print('V4L2Loopback device successfully added')

print('Map kinect stream to loopback device')
fvd = virtualvideo.FakeVideoDevice()
print('Adding input')
fvd.init_input(vidsrc)
print('Adding loopback device')
fvd.init_output(loopbackdeviceindex, 1920, 1080, fps=30)
print('Starting conversions')
try:
    fvd.run()
except:
    print('Something went wrong')
    exit_handler()

atexit.register(exit_handler)
