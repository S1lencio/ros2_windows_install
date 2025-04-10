## WIP Python install script for ROS2 Jazzy

Installs ROS2 Jazzy Jalisco by following the installation workflow found [here](https://docs.ros.org/en/jazzy/Installation/Windows-Install-Binary.html).

This script is a work in progress and does not work yet. It will only run on Windows 10 or 11.
#

## Current status:
Installation succeeds, but demo nodes fail to start.

### talker error:
```
[ros2run]: Process exited with failure 3221226505
```

### listener error:
```
Traceback (most recent call last):
File "C:\dev\ros2_jazzy\lib\demo_nodes_py\listener-script.py", line 33, in <module>
sys.exit(load_entry_point('demo-nodes-py==0.33.5', 'console_scripts', 'listener')())
File "C:\dev\ros2_jazzy\Lib\site-packages\demo_nodes_py\topics\listener.py", line 33, in main
rclpy.init(args=args)
File "C:\dev\ros2_jazzy\Lib\site-packages\rclpy\__init__.py", line 88, in init
context.init(args, domain_id=domain_id)
File "C:\dev\ros2_jazzy\Lib\site-packages\rclpy\context.py", line 99, in init
self.__context = _rclpy.Context(
rclpy._rclpy_pybind11.RCLError: Failed to initialize init options: failed to load any RMW implementations, at C:\ci\ws\src\ros2\rmw_implementation\rmw_implementation\src\functions.cpp:125, at C:\ci\ws\src\ros2\rcl\rcl\src\rcl\init_options.c:75
[ros2run]: Process exited with failure 1
```
