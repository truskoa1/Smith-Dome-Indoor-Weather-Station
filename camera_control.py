import subprocess

SERVICE_NAME = "camera-stream.service"

def run_systemctl(command):
    result = subprocess.run( 
        ["sudo", "systemctl", command, SERVICE_NAME],
        capture_output=True,
        text=True
    )

    return result

def camera_on():
    result = run_systemctl("is-active")

    return result.stdout.strip() == "active"

def start_camera():
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
    if camera_on():
        return stop_camera()
    
    return start_camera()
   