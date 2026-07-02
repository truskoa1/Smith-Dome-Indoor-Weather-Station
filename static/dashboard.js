async function updateWeather() {
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
        
        document.getElementById("outside-temperature-f").textContent = 
            data.outside.temperature_f;

        document.getElementById("outside-temperature-c").textContent = 
            data.outside.temperature_c;

        document.getElementById("outside-humidity").textContent = 
            data.outside.humidity;

        document.getElementById("outside-pressure").textContent =
            data.outside.pressure_hpa;
            
    } catch (error) {
        console.error("Could not update weather data:", error);
    }
}

updateWeather();

setInterval(updateWeather, 5000); // 5000 = weather info updates every 5 seconds

const menuButton = document.getElementById("menu-button");
const sideMenu = document.getElementById("side-menu");
const cameraButton = document.getElementById("camera-button");

menuButton.addEventListener("click", () => {
    sideMenu.classList.toggle("hidden");
});

async function updateCameraButton() {
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
    try {
        const response = await fetch("/api/alerts");

        if (!response.ok) {
            throw new Error("Alert API request failed");
        }

        const alert = await response.json();

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