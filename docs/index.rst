.. dice-detection documentation master file, created by
   sphinx-quickstart on Tue Nov 14 08:31:45 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to dice-detection's documentation!
==========================================
Welcome to the documentation for our Computer Vision class project.
This Python library has been developed to detect live-streamed dice numbers. 
The objective is to provide a straightforward tool for identifying and analyzing 
dice numbers in real-time. This documentation offers detailed information on 
the library's functionalities, installation procedures, and practical examples 
to facilitate the utilization of our solution. The project is a reflection of our 
exploration into the world of Computer Vision, born out of the requirements
of our class assignment. We invite you to navigate through this documentation as
we delve into the intricacies of dice detection using Python

Using the Repository
--------------------

1. Clone the repo
   ::

      git clone https://github.com/Vigrel/dice-detection.git

2. Create and activate virtualenv
   ::

      cd dice-detection/
      python3 -m virtualenv .venv
      source .venv/bin/activate

3. Run a demo
   ::

      python3 src/dice_detection_demo.py

Configuring the Environment
---------------------------

To ensure dice detection accuracy, set up the environment as follows:

1. **Surface**: Place a white piece of paper on the table for dice rolling. The white background enhances contrast for better detection.

2. **Camera Position**: Position the camera in a top-down view, parallel to the table surface. The camera height should be 40 centimeters above the table for a clear and consistent perspective.

3. **Adjust CAMERA_DISTANCE**: In the configuration module, adjust the `CAMERA_DISTANCE` parameter to reflect the actual distance in centimeters between the camera and the table surface. This parameter is crucial for accurate calculations and reliable dice number detection.

4. **Camera Calibration (if necessary)**: Calibrate the camera if needed for accurate measurements. Refer to your camera documentation for calibration procedures.

Follow these guidelines to create an environment for effective dice detection, ensuring optimal system performance.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
