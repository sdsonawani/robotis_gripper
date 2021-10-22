# Test Robotis Gripper

* Install dependencies in virtualenv

``` pip install -r requirements.txt ```

* To start open and close gripper action at an interval of 3 secs

``` python gripper.py --port [/dev/ttyUSB6] --close [closing distance in mm] ```