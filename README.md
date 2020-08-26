# Kinect V2 Loopback
This Python script connects the dots between libfreenect2 and v4l2loopback in order to use a Kinect V2 device as a webcam on Linux.

# Requirments
* A Microsoft Kinect V2
* [libfreenect2](https://github.com/OpenKinect/libfreenect2)
* [v4l2loopback](https://github.com/umlaeute/v4l2loopback)
* [FFmpeg](https://ffmpeg.org/)
* [Python 3](https://www.python.org/)
* Python libraries
    * [pylibfreenect2](https://github.com/r9y9/pylibfreenect2)
    * [virtualvideo](https://github.com/Flashs/virtualvideo)

# Future work:
* Add udev rule to automatically start and stop the script
* Fix cleanup of v4l2loopback devices
    * Find a better way to clean them up than unloading the whole module and removing every loopback device
* Create Arch Package in the  AUR
* Create packages for other distros

# Credits
This script relies on [pylibfreenect2](https://github.com/r9y9/pylibfreenect2), [virtualvideo](https://github.com/Flashs/virtualvideo), [v4l2loopback](https://github.com/umlaeute/v4l2loopback), [libfreenect2](https://github.com/OpenKinect/libfreenect2) and [FFmpeg](https://ffmpeg.org/) to do the heavy lifting. Thanks to all the contributors of those projects, their dependencies and [Python](https://www.python.org/) for their work.
