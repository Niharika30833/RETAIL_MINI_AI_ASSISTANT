const BASE_URL = "https://retail-mini-ai-assistant-bot.onrender.com";

// CHAT FUNCTION
async function send() {
    let input = document.getElementById("input").value;

    if (!input) return;

    let res = await fetch(`${BASE_URL}/chat/?query=${encodeURIComponent(input)}`);
    let data = await res.json();

    document.getElementById("response").innerText = data.response;
}

// VOICE INPUT
function startVoice() {
    let recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        document.getElementById("input").value = event.results[0][0].transcript;
    };

    recognition.start();
}

// SALES GRAPH FUNCTION
async function getSales() {
    let input = document.getElementById("input").value;

    let yearMatch = input.match(/\d{4}/);
    let year = yearMatch ? yearMatch[0] : 2024;

    let res = await fetch(`${BASE_URL}/sales-by-year/?year=${year}`);
    let data = await res.json();

    let labels = [];
    let values = [];

    data.forEach(item => {
        labels.push(item[0]);
        values.push(item[1]);
    });

    drawChart(labels, values, year);
}

// CHART DRAW FUNCTION
let chart;

function drawChart(labels, data, year) {
    const ctx = document.getElementById('salesChart').getContext('2d');

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: `Sales in ${year}`,
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });
}
