async function updateCurrentWeather() {
    try {
        const response = await fetch("/api/weather")

        if (!response.ok) {
            throw new Error("Weather API request failed.")
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
        console.error("Could not update current weather data:", error);
    }
}

async function updateCameraStatus() {
    try {
        const response = await fetch("/api/camera/status");
        const data = await response.json();

        const statusText = document.getElementById("camera-status-text");
        const cameraStream = document.getElementById("camera-stream");

        if (data.camera_running) {
            statusText.classList.add("hidden");
            cameraStream.classList.remove("hidden");
        } else {
            statusText.textContent = "Camera stream is off.";
            statusText.classList.remove("hidden");
            cameraStream.classList.add("hidden");
        }
    }
    catch (error) {
        console.error("Error checking camera status:", error);

        const statusText = document.getElementById("camera-status-text");
        const cameraStream = document.getElementById("camera-stream");

        statusText.textContent = "Camera status unavailable.";
        statusText.classList.remove("hidden");
        cameraStream.classList.add("hidden");
    }
}

setInterval(updateCameraStatus, 2000);
updateCameraStatus();

function addCell(rowElement, text) {
    const cell = document.createElement("td");
    cell.textContent = text;
    rowElement.appendChild(cell);
}

async function updateWeatherLog() {
    try {
        const response = await fetch("/api/weather-log");

        if (!response.ok) {
            throw new Error("Weather log request failed");
        }

        const logRows = await response.json();
        const tableBody = document.getElementById("weather-log-body");

        tableBody.innerHTML = "";

        for (const row of logRows) {
            const tr = document.createElement("tr");

            addCell(tr, row.timestamp_utc);

            addCell(
                tr,
                row.inside_temperature_f + "°F / " +
                row.inside_temperature_c + "°C"
            );

            addCell(tr, row.inside_humidity + "%");

            addCell(tr, row.inside_pressure_hpa + " hPa");

            addCell(
                tr,
                row.outside_temperature_f + "°F / " +
                row.outside_temperature_c + "°C"
            );

            addCell(tr, row.outside_humidity + "%");

            addCell(tr, row.outside_pressure_hpa + " hPa");

            tableBody.appendChild(tr);
        }
    } catch (error) {
        console.error("Could not update weather log:", error);
    }
}

function updateDashboard() {
    updateCurrentWeather();
    updateWeatherLog();
}

updateDashboard();

setInterval(updateDashboard, 5000);