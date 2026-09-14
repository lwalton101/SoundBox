
import platform
import subprocess
import re


def get_rpi_gpu_memory():
    """
    Get GPU memory allocated on a Raspberry Pi.

    Returns:
        int: GPU memory in MB
        None: If it cannot be determined
    """

    try:
        result = subprocess.run(
            ["vcgencmd", "get_mem", "gpu"],
            capture_output=True,
            text=True,
            check=True
        )

        match = re.search(r"gpu=(\d+)([MG])", result.stdout)

        if not match:
            return None

        value = int(match.group(1))
        unit = match.group(2)

        if unit == "G":
            value *= 1024

        return value

    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def get_windows_gpu_memory():
    """
    Get GPU memory available on Windows.

    Returns:
        dict containing:
            dedicated_total
            dedicated_used
            dedicated_free
            shared_total
            shared_used
            shared_free
            total_available

        Values are in MB.
    """

    powershell_script = r"""
    $gpus = Get-Counter '\GPU Adapter Memory(*)\Dedicated Usage',
                         '\GPU Adapter Memory(*)\Shared Usage'

    $dedicated = 0
    $shared = 0

    foreach ($sample in $gpus.CounterSamples) {

        if ($sample.Path -like '*Dedicated Usage') {
            $dedicated += $sample.CookedValue
        }

        if ($sample.Path -like '*Shared Usage') {
            $shared += $sample.CookedValue
        }
    }

    $memory = Get-CimInstance Win32_ComputerSystem

    $ram = $memory.TotalPhysicalMemory

    Write-Output "$dedicated,$shared,$ram"
    """

    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                powershell_script
            ],
            capture_output=True,
            text=True,
            check=True
        )

        output = result.stdout.strip()

        dedicated_used, shared_used, total_ram = map(
            float,
            output.split(",")
        )

        # Windows normally allows roughly half of system RAM
        # to be used as shared GPU memory.
        shared_total = total_ram / 2

        # Dedicated VRAM total is obtained from the GPU.
        gpu_info = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                r"""
                Get-CimInstance Win32_VideoController |
                Where-Object {$_.AdapterRAM -ne $null} |
                Select-Object -First 1 -ExpandProperty AdapterRAM
                """
            ],
            capture_output=True,
            text=True,
            check=True
        )

        dedicated_total = float(gpu_info.stdout.strip())

        # Convert bytes to MB
        dedicated_total_mb = dedicated_total / (1024 ** 2)
        dedicated_used_mb = dedicated_used / (1024 ** 2)

        shared_total_mb = shared_total / (1024 ** 2)
        shared_used_mb = shared_used / (1024 ** 2)

        dedicated_free_mb = max(
            0,
            dedicated_total_mb - dedicated_used_mb
        )

        shared_free_mb = max(
            0,
            shared_total_mb - shared_used_mb
        )

        return {
            "dedicated_total": dedicated_total_mb,
            "dedicated_used": dedicated_used_mb,
            "dedicated_free": dedicated_free_mb,

            "shared_total": shared_total_mb,
            "shared_used": shared_used_mb,
            "shared_free": shared_free_mb,

            "total_available":
                dedicated_free_mb + shared_free_mb
        }

    except (subprocess.CalledProcessError, ValueError):
        return None


def get_gpu_memory():
    """
    Automatically select the correct implementation.

    Returns:
        On Raspberry Pi:
            int -> GPU memory in MB

        On Windows:
            dict -> GPU memory information

        None if unsupported.
    """

    system = platform.system()

    if system == "Windows":
        return get_windows_gpu_memory()

    elif system == "Linux":
        # Check if this is a Raspberry Pi
        try:
            with open("/proc/device-tree/model", "r") as f:
                model = f.read().replace("\x00", "")

            if "Raspberry Pi" in model:
                return get_rpi_gpu_memory()

        except FileNotFoundError:
            pass

    return None


# ---------------------------------------------------------
# Example
# ---------------------------------------------------------

if __name__ == "__main__":

    system = platform.system()

    if system == "Windows":

        memory = get_windows_gpu_memory()

        if memory is None:
            print("Could not determine GPU memory.")
        else:
            print("Windows GPU Memory")
            print("------------------")
            print(
                f"Dedicated VRAM free: "
                f"{memory['dedicated_free']:.0f} MB"
            )
            print(
                f"Shared GPU memory free: "
                f"{memory['shared_free']:.0f} MB"
            )
            print(
                f"Total GPU memory available: "
                f"{memory['total_available']:.0f} MB"
            )

    elif system == "Linux":

        memory = get_rpi_gpu_memory()

        if memory is None:
            print("Could not determine Raspberry Pi GPU memory.")
        else:
            print("Raspberry Pi GPU Memory")
            print("-----------------------")
            print(f"GPU memory: {memory} MB")

    else:
        print(f"Unsupported operating system: {system}")
