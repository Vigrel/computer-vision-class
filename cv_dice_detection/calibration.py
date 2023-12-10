"""
The config module sets parameters for the state of the physical world. 
"""

CAMERA_DISTANCE = 40
"""
Here, you configure the camera's height for the top-down view by
assigning a value to CAMERA_DISTANCE in centimeters.

It allows distance between 30-40 cm.
"""

"""
There are more advanced configs which affects the 
detection of dice blops in a unique way, presented below:
"""

MININERTIARATIO = 0.6
"""
MININERTIARATIO: The ratio between the minor and major axes of a blob. Essentially, 
    this parameter is used to filter out blobs that are not circular enough, discarding oval blobs. 
    The value is set to 0.6, which means that the minor axis must be at least 60% of the major axis.
"""

MEDIANBLUR = 7
"""
MEDIANBLUR: The size of the median filter kernel. Must be an odd integer.
    In an environment with a lot of noise, such as a dark environemnt with a low quality camera,
    this value should be increased to reduce noise. 
"""

SUM_THRESHOLD = 60
"""
SUM_THRESHOLD: The threshold for the length of the sum list. Essentially, this parameter is used to
    determine how many frames of a constant sum are required to stop the detection and assert that the sum is final.
"""
