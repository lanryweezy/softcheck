# softcheck
Title:  System Information Script (descriptive and concise title)

Description:  This script gathers information about your system, including CPU usage, RAM usage, disk usage, network usage, and some general system information like username, system model, hostname, and OS version.  It can be run on Windows or Linux systems.

Features:

Gathers a variety of system information
Works on Windows and Linux systems
Easy to use - run the script and view the information
How to Use:

Save the script as a Python file (e.g., system_info.py)
Open a terminal or command prompt and navigate to the directory where you saved the script
Run the script using the following command: python system_info.py
Output:

The script will print the following information to the console:

Username
System model
System name (hostname)
OS version
Serial number (if available on Windows)
RAM size (total)
Used memory
RAM usage percentage
Total disk space
Used disk space
Disk usage percentage
CPU usage percentage
Network usage - bytes received and bytes sent
Dependencies:

The script uses the following Python modules:

os
platform
subprocess
socket
psutil (for Windows systems, you may need to install this using pip install psutil)
winreg (on Windows only)
Note: Retrieving the system serial number on Windows requires administrator privileges.
