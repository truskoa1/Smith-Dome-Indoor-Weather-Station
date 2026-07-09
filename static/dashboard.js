/*
Frontend behavior for the FOH touchscreen display.

This does the following:
    - Fetches current weather data from /api/weather
    - Updates the visible temperature, humidity, and pressure values
    - Checks camera stream status and updates the button accordingly.
    - Sends camera start/stop requests to /api/camera/toggle
    - Fetches alert state from /api/alerts
    - Applies CSS classes for unknown, warning, and danger alert states.

This pulls from the backend, it does not directly determine alert state or weather data.
*/

async function updateWeather() {
    /*
    Fetch the latest weather data from Flask and update dashboard values.

    /api/weather returns JSON created by sensor_reader.py. This function copies the values from that JSON into the specific HTML 
    spans using their element IDs. 

    To prevent an error breaking the entire page, an API request failure results in an error being logged, but the dashboard stays
    loaded. 
    */
    try {
        const response = await fetch("/api/weather");

        if (!response.ok) {
            throw new Error("Weather API request failed");
        }

        const data = await response.json();

        document.getElementById("inside-temperature-f").textContent = 
            data.inside.temperature_f;

        document.getElementById("inside-temperature-c").textContent = 
            data.inside.temperature_c;

        document.getElementById("inside-humidity").textContent = 
            data.inside.humidity;
        
        document.getElementById("inside-pressure").textContent =
            data.inside.pressure_hpa;

        document.getElementById("inside-last-updated").textContent =
            data.inside.last_updated;
        
        document.getElementById("outside-temperature-f").textContent = 
            data.outside.temperature_f;

        document.getElementById("outside-temperature-c").textContent = 
            data.outside.temperature_c;

        document.getElementById("outside-humidity").textContent = 
            data.outside.humidity;

        document.getElementById("outside-pressure").textContent =
            data.outside.pressure_hpa;
        
        document.getElementById("outside-last-updated").textContent =
            data.outside.last_updated;
            
    } catch (error) {
        console.error("Could not update weather data:", error);
    }
}

// Runs once immediately so dashboard does not wait
updateWeather();

// Weather info will update every 5 seconds (5000 milliseconds)
setInterval(updateWeather, 5000); 

const menuButton = document.getElementById("menu-button");
const sideMenu = document.getElementById("side-menu");
const cameraButton = document.getElementById("camera-button");

menuButton.addEventListener("click", () => {
    /*
    Show or hide the side menu when the user taps the menu button.
    */
    sideMenu.classList.toggle("hidden");
});

async function updateCameraButton() {
    /*
    Fetches camera status and updates the camera button text.

    Inactive camera: "Start Camera" message
    Active camera: "Stop Camera" message
    */
    try {
        const response = await fetch("/api/camera/status");
        const data = await response.json();

        if (data.camera_running) {
            cameraButton.textContent = "Stop Camera";
        } else {
            cameraButton.textContent = "Start Camera";
        }
    } catch (error) {
        console.error("Error checking camera status:", error);
        cameraButton.textContent = "Camera Status Error";
    }
}

cameraButton.addEventListener("click", async () => {
    /*
    Starts or stops camera stream when the user presses the camera button. 

    Sends a POST request because toggling the camera changes the system state. The systemd control occurs in the backend in
    camera_control.py.
     */
    try {
        cameraButton.textContent = "Working...";

        const response = await fetch("/api/camera/toggle", {
            method: "POST"
        });

        const data = await response.json();
        console.log("Camera toggle result:", data);

        if (!data.success) {
            cameraButton.textContent = "Camera Error";
            return;
        }

        await updateCameraButton();
        sideMenu.classList.add("hidden");
    } catch (error) {
        console.error("Error toggling camera:", error);
        cameraButton.textContent = "Camera Error";
    }
});

updateCameraButton();
setInterval(updateCameraButton, 5000)

const alertBox = document.getElementById("alert-box");
const alertTitle = document.getElementById("alert-title");
const alertMessage = document.getElementById("alert-message");
const snoozeAlertButton = document.getElementById("snooze-alert-button");

async function updateAlerts() {
    /*
    Fetch the current alert state from Flask and updates the FOH display.

    Alert states are returned by /api/alerts:
        none: 
            Hide the alert box and use the normal dashboard styles
        unknown:
            Show blue-grey alert state. Outside weather data is unavailable.
        caution:
            Show amber alert state. Warning can be snoozed.
        danger:
            Show red alert state. Danger cannot be snoozed.

    This function does not calculate the alert state. It displays the backend result by adding/removing CSS classes.
     */
    try {
        const response = await fetch("/api/alerts");

        if (!response.ok) {
            throw new Error("Alert API request failed");
        }

        const alert = await response.json();

        // Clears previous alert styling before applying the latest state.
        // This prevents conflicting states. 
        document.body.classList.remove(
            "alert-unknown",
            "alert-warning",
            "alert-danger"
        );

        alertBox.classList.remove("unknown", "warning", "danger");

        if (!alert.active || alert.snoozed) {
            alertBox.classList.add("hidden");
            return;
        }

        alertBox.classList.remove("hidden");

        const messageText = alert.messages.join(" ");

        if (alert.level === "unknown") {
            document.body.classList.add("alert-unknown");
            alertBox.classList.add("unknown");

            alertTitle.textContent = "WEATHER DATA UNAVAILABLE";
            alertMessage.textContent = messageText;

            snoozeAlertButton.classList.add("hidden");
        }

        if (alert.level === "warning") {
            document.body.classList.add("alert-warning");
            alertBox.classList.add("warning");

            alertTitle.textContent = "WARNING";
            alertMessage.textContent = messageText;

            snoozeAlertButton.classList.remove("hidden")
        }

        if (alert.level === "danger") {
            document.body.classList.add("alert-danger");
            alertBox.classList.add("danger");

            alertTitle.textContent = "DANGER";
            alertMessage.textContent = messageText + "Close dome immediately.";

            snoozeAlertButton.classList.add("hidden")
        }
    } catch (error) {
        console.error("Could not update alerts:", error);
    }
}

snoozeAlertButton.addEventListener("click", async () => {
    /*
    Snoozes a caution alert. 

    The frontend sends a POST request to Flask, and weather_warnings.py stores the snooze expiration timestamp. This does not control
    the timer directly
    */
    try {
        const response = await fetch("api/alerts/snooze", {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error("Snooze request failed");
        }

        await response.json();
        await updateAlerts();
    } catch (error) {
        console.error("Could not snooze alert:", error);
    }
});

updateAlerts();
setInterval(updateAlerts, 5000);