import os
import platform
import subprocess
import socket
import psutil
import winreg

# Function to get CPU usage
def get_cpu_usage():
    if platform.system() == 'Windows':
        return psutil.cpu_percent(interval=1)
    else:
        result = subprocess.run(['top', '-bn1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        for line in result.stdout.strip().split('\n'):
            if line.startswith('%Cpu'):
                cpu_load = line.split()[1]
                return int(cpu_load)

# Function to get RAM usage
def get_ram_usage():
    if platform.system() == 'Windows':
        ram = psutil.virtual_memory()
        total_memory_gb = ram.total / (1024 ** 3)  # Convert to GB
        used_memory_gb = ram.used / (1024 ** 3)  # Convert to GB
        return total_memory_gb, used_memory_gb, ram.percent
    else:
        result = subprocess.run(['free', '-m'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        for line in result.stdout.strip().split('\n'):
            if line.startswith('Mem:'):
                total_memory, used_memory, _, _, _, _ = map(int, line.split()[1:])
                total_memory_gb = total_memory / 1024  # Convert to GB
                used_memory_gb = used_memory / 1024  # Convert to GB
                return total_memory_gb, used_memory_gb, (used_memory_gb / total_memory_gb) * 100

# Function to get disk usage
def get_disk_usage():
    if platform.system() == 'Windows':
        disk = psutil.disk_usage('/')
        total_disk_gb = disk.total / (1024 ** 3)  # Convert to GB
        used_disk_gb = disk.used / (1024 ** 3)  # Convert to GB
        return total_disk_gb, used_disk_gb, disk.percent
    else:
        disk = os.statvfs('/')
        total_disk = disk.f_frsize * disk.f_blocks
        used_disk = disk.f_frsize * (disk.f_blocks - disk.f_bfree)
        total_disk_gb = total_disk / (1024 ** 3)  # Convert to GB
        used_disk_gb = used_disk / (1024 ** 3)  # Convert to GB
        disk_percent = (used_disk_gb / total_disk_gb) * 100
        return total_disk_gb, used_disk_gb, disk_percent

# Function to get network usage
def get_network_usage():
    if platform.system() == 'Windows':
        network = psutil.net_io_counters()
        return network.bytes_sent, network.bytes_recv
    else:
        result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        for line in result.stdout.strip().split('\n'):
            if 'RX packets' in line:
                rx_bytes = int(line.split('RX packets')[1].split()[0])
            elif 'TX packets' in line:
                tx_bytes = int(line.split('TX packets')[1].split()[0])
        return rx_bytes, tx_bytes

# Function to get system information
def get_system_info():
    user_name = os.environ.get('USERNAME')
    system_model = platform.machine()
    system_name = socket.gethostname()
    os_version = platform.platform()

    if platform.system() == 'Windows':
        try:
            result = subprocess.run(['wmic', 'bios', 'get', 'serialnumber'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            serial_number = result.stdout.strip().split('\n')[-1]
        except Exception:
            serial_number = "Not available"
    else:
        serial_number = "Not available"

    total_memory, used_memory, ram_percent = get_ram_usage()
    total_disk, used_disk, disk_percent = get_disk_usage()

    return user_name, system_model, system_name, os_version, serial_number, total_memory, used_memory, ram_percent, total_disk, used_disk, disk_percent

# Main function
def main():
    user_name, system_model, system_name, os_version, serial_number, total_memory, used_memory, ram_percent, total_disk, used_disk, disk_percent = get_system_info()
    cpu_usage = get_cpu_usage()
    rx_bytes, tx_bytes = get_network_usage()

    print("USER NAME:", user_name)
    print("SYSTEM MODEL:", system_model)
    print("SYSTEM NAME:", system_name)
    print("OS Version:", os_version)
    print("SERIAL NUMBER:", serial_number)
    print("RAM SIZE:", round(total_memory, 2), "GB")  # Round to 2 decimal places
    print("USED MEMORY:", round(used_memory, 2), "GB")  # Round to 2 decimal places
    print("RAM USAGE:", ram_percent, "%")
    print("TOTAL DISK:", round(total_disk, 2), "GB")  # Round to 2 decimal places
    print("USED DISK:", round(used_disk, 2), "GB")  # Round to 2 decimal places
    print("DISK USAGE:", round(disk_percent, 2), "%")  # Round to 2 decimal places
    print("CPU USAGE:", cpu_usage, "%")
    print("NETWORK USAGE - Bytes Received:", rx_bytes, "| Bytes Sent:", tx_bytes)
    input("Press Enter to exit...")
if __name__ == "__main__":
    main()
