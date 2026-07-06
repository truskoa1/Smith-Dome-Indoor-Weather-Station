"""
Camera stream control.

This file checks, starts, stops, and toggles the camera-stream systemd service. This allows our FOH touchscreen display to 
start and stop our camera stream through a button.

The actual stream is controlled by stream.py. This script controls the background service, it does not directly capture anything using
the Pi camera. 

The Pi must allow the Flask process to run specific systemctl commands without requiring an interactive password. This is handled
through sudoers. Documentation pending :p
"""

import subprocess

SERVICE_NAME = "camera-stream.service"

def run_systemctl(command):
    """
    Run a systemctl command for the camera stream service. 
    
    Args:
        command (str):
            systemctl command to run. i.e. "start" or "is-active"

    Returns:
        subprocess.CompletedProcess:
            Result object containing return code, stdout, and stderr 
    """
    result = subprocess.run( 
        ["sudo", "systemctl", command, SERVICE_NAME],
        capture_output=True,
        text=True
    )

    return result

def camera_on():
    """
    Returns True is the camera stream service is active.

    Returns:
        bool: 
            True if systemctl reports the service as active.
            False otherwise
    """
    result = run_systemctl("is-active")

    return result.stdout.strip() == "active"

def start_camera():
    """
    Begins camera stream.

    Returns:
        dict: 
            Result dictionary returned to the frontend. Includes whether the camera is running, whether the command succeeded,
            and a message.
    """
    result = run_systemctl("start")

    if result.returncode != 0:
        return {
            "camera_running": camera_on(),
            "success": False,
            "message": result.stderr.strip()
        }
    
    return {
        "camera_running": camera_on(),
        "success": True,
        "message": "Camera stream started."
    }

def stop_camera():
    """
    Stops camera stream.

    Returns:
        dict: 
            Result dictionary returned to the frontend. Includes whether the camera is running, whether the command succeeded,
            and a message.
    """
    result = run_systemctl("stop")

    if result.returncode != 0:
        return {
            "camera_running": camera_on(),
            "success": False,
            "message": result.stderr.strip()
        }
    
    return {
        "camera_running": camera_on(),
        "success": True,
        "message": "Camera stream stopped."
    }

def toggle_stream():
    """
    Toggles the status of stream.

    Returns: 
        dict: 
            Result from stop_camera() if the service is running. Otherwise, result from start_camera().

    """
    if camera_on():
        return stop_camera()
    
    return start_camera()
   