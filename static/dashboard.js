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
        
        document.getElementById("outside-temperature-f").textContent = 
            data.outside.temperature_f;

        document.getElementById("outside-temperature-c").textContent = 
            data.outside.temperature_c;

        document.getElementById("outside-humidity").textContent = 
            data.outside.humidity;
    } catch (error) {
        console.error("Could not update weather data:", error);
    }
}

updateWeather();

setInterval(updateWeather, 5000); // 5000 = weather info updates every 5 seconds