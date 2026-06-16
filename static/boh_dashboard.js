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
        document.getElementById("outside-temperature-f").textContent =
            data.outside.temperature_f;
        document.getElementById("outside-temperature-c").textContent =
            data.outside.temperature_c;
        document.getElementById("outside-humidity").textContent =
            data.outside.humidity;
    } catch (error) {
        console.error("Could not update current weather data:", error);
    }
}

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

            addCell(
                tr,
                row.outside_temperature_f + "°F / " +
                row.outside_temperature_c + "°C"
            );

            addCell(tr, row.outside_humidity + "%");

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