let pollutantChart = null;
let popupChart = null;
let currentChartData = null;
let currentDetails = null; // Menyimpan cache data untuk pop-up modal

// LOGIKA REALTIME CLOCK (TANGGAL & JAM)
function updateRealtimeClock() {
    const dateElement = document.getElementById('current-date');
    const timeElement = document.getElementById('current-time');

    if (!dateElement || !timeElement) return;

    const now = new Date();

    // Format Tanggal Indonesia (contoh: Kamis, 27 Agustus 2026)
    const optionsDate = {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    };
    dateElement.innerText = now.toLocaleDateString('id-ID', optionsDate);

    // Format Jam 24 Jam (HH:MM:SS)
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    timeElement.innerText = `${hours}:${minutes}:${seconds}`;
}

// LOGIKA CUSTOM DROPDOWN
function toggleCustomDropdown() {
    const menu = document.getElementById('dropdownMenu');
    const arrow = document.getElementById('dropdownArrow');
    if (!menu) return;

    menu.classList.toggle('hidden');
    if (arrow) {
        arrow.classList.toggle('rotate-180');
    }
}

function selectLocation(locationId, labelText) {
    const label = document.getElementById('selectedLocationText');
    if (label) label.innerText = labelText;

    toggleCustomDropdown();
    updateDashboard(locationId);
}

// Tutup dropdown jika klik di luar area
window.addEventListener('click', (e) => {
    const btn = document.getElementById('dropdownBtn');
    const menu = document.getElementById('dropdownMenu');
    if (btn && menu && !btn.contains(e.target) && !menu.contains(e.target)) {
        menu.classList.add('hidden');
        const arrow = document.getElementById('dropdownArrow');
        if (arrow) arrow.classList.remove('rotate-180');
    }
});

// LOGIKA POP-UP MODAL (SHOW & CLOSE WITH ANIMATION)
function showModal(htmlContent, isLarge = false) {
    const container = document.getElementById('modalContainer');
    const modalBox = document.getElementById('modalBox');
    const content = document.getElementById('modalContent');

    if (!container || !modalBox || !content) return;

    content.innerHTML = htmlContent;

    // Atur lebar modal (apakah modal besar untuk chart atau modal standar)
    if (isLarge) {
        modalBox.className = "card-box w-full max-w-5xl p-6 md:p-8 rounded-3xl shadow-2xl transform scale-90 transition-all duration-300 relative";
    } else {
        modalBox.className = "card-box w-full max-w-md p-6 rounded-3xl shadow-2xl transform scale-90 transition-all duration-300 relative";
    }

    // Tampilkan container modal
    container.classList.remove('hidden');

    // Delay untuk memicu animasi scale & opacity
    setTimeout(() => {
        container.classList.remove('opacity-0');
        modalBox.classList.remove('scale-90');
        modalBox.classList.add('scale-100');
    }, 10);
}

function closeModal() {
    const container = document.getElementById('modalContainer');
    const modalBox = document.getElementById('modalBox');

    if (!container || !modalBox) return;

    container.classList.add('opacity-0');
    modalBox.classList.remove('scale-100');
    modalBox.classList.add('scale-90');

    setTimeout(() => {
        container.classList.add('hidden');
        if (popupChart) {
            popupChart.destroy();
            popupChart = null;
        }
    }, 300);
}

// Event Listener klik area luar modal untuk menutup modal
window.addEventListener('click', (e) => {
    const container = document.getElementById('modalContainer');
    if (e.target === container) {
        closeModal();
    }
});

// POP-UP HANDLERS
function openPollutantModal(type) {
    if (!currentDetails || !currentDetails.pollutants) return;

    const names = {
        'CO': 'Karbon Monoksida (CO)',
        'NO2': 'Nitrogen Dioksida (NO₂)',
        'PM25': 'Partikulat PM2.5',
        'PM10': 'Partikulat PM10',
        'O3': 'Ozon (O₃)',
        'SO2': 'Sulfur Dioksida (SO₂)'
    };

    const descs = {
        'CO': 'Gas tidak berwarna dan tidak berbau yang dihasilkan dari pembakaran tidak sempurna pada mesin kendaraan bermotor.',
        'NO2': 'Gas polutan udara utama yang berasal dari emisi kendaraan dan industri, dapat mengiritasi saluran pernapasan.',
        'PM25': 'Partikel udara mikroskopis berukuran ≤ 2.5 mikron yang sangat halus dan sanggup menembus paru-paru secara mendalam.',
        'PM10': 'Partikel udara berukuran ≤ 10 mikron seperti debu, jelaga, dan asap yang dapat mempengaruhi saluran pernapasan atas.',
        'O3': 'Ozon permukaan tanah yang terbentuk akibat reaksi kimia antara polutan primer dan sinar matahari.',
        'SO2': 'Gas yang dihasilkan dari pembakaran bahan bakar fosil yang mengandung sulfur seperti batu bara dan minyak bumi.'
    };

    const val = currentDetails.pollutants[type] || 'N/A';
    const title = names[type] || type;
    const desc = descs[type] || 'Detail parameter kualitas udara.';

    const html = `
        <div class="text-center">
            <div class="text-3xl mb-2">🌫️</div>
            <h3 class="text-lg font-bold mb-1">${title}</h3>
            <div class="text-3xl font-extrabold text-sky-500 dark:text-sky-400 my-3">${val} µg/m³</div>
            <p class="text-xs opacity-85 leading-relaxed card-box-inner p-3 rounded-xl">${desc}</p>
        </div>
    `;

    showModal(html, false);
}

function openIspuModal(index) {
    if (!currentDetails || !currentDetails.ispu_forecast) return;
    const item = currentDetails.ispu_forecast[index];
    if (!item) return;

    const html = `
        <div class="text-center">
            <div class="text-4xl mb-2">${item.icon}</div>
            <div class="text-xs opacity-75 font-semibold">${item.date}</div>
            <h3 class="text-xl font-bold mt-1">Prakiraan ISPU</h3>
            <div class="text-4xl font-extrabold text-sky-500 dark:text-sky-400 my-3">${item.value}</div>
            <div class="inline-block px-4 py-1.5 rounded-full card-box-inner text-sm font-bold">${item.status}</div>
            <p class="text-xs opacity-80 mt-4 leading-relaxed">
                Nilai Indeks Standar Pencemar Udara (ISPU) untuk tanggal ${item.date} menunjukkan kondisi ${item.status.toLowerCase()}.
            </p>
        </div>
    `;

    showModal(html, false);
}

function openWeatherModal(index) {
    if (!currentDetails || !currentDetails.weather_forecast) return;
    const item = currentDetails.weather_forecast[index];
    if (!item) return;

    let icon = '☀️';
    const cond = item.condition ? item.condition.toLowerCase() : '';
    if (cond.includes('hujan')) icon = '🌧️';
    else if (cond.includes('berawan') || cond.includes('mendung')) icon = '⛅';

    const html = `
        <div class="text-center">
            <div class="text-4xl mb-2">${icon}</div>
            <div class="text-xs opacity-75 font-semibold">Jam ${item.time}</div>
            <h3 class="text-xl font-bold mt-1">${item.condition}</h3>
            <div class="text-4xl font-extrabold text-sky-500 dark:text-sky-400 my-3">${item.temp}</div>
            <p class="text-xs opacity-80 card-box-inner p-3 rounded-xl leading-relaxed">
                Prediksi cuaca pada pukul <strong>${item.time}</strong> diperkirakan <strong>${item.condition}</strong> dengan suhu sekitar <strong>${item.temp}</strong>.
            </p>
        </div>
    `;

    showModal(html, false);
}

// POP-UP GRAFIK BESAR & DETAIL
function openChartModal() {
    if (!currentChartData) return;

    const html = `
        <div class="flex flex-col h-full">
            <h3 class="text-base sm:text-lg font-bold text-center mb-1">Perbandingan 6 Polutan Berdasarkan Prediksi Tanggal</h3>
            <p class="text-xs text-center opacity-70 mb-4">Grafik Detail Tren Prediksi Konsentrasi Polutan (µg/m³)</p>
            <div class="relative card-box-inner rounded-2xl p-4 h-[420px] sm:h-[500px] w-full">
                <canvas id="popupPollutantChart"></canvas>
            </div>
        </div>
    `;

    showModal(html, true);

    setTimeout(() => {
        renderPopupChart(currentChartData);
    }, 50);
}

function renderPopupChart(chartData) {
    const canvas = document.getElementById('popupPollutantChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    if (popupChart) {
        popupChart.destroy();
    }

    const isDarkMode = document.documentElement.classList.contains('dark');
    const textColor = isDarkMode ? '#f8fafc' : '#1e293b';
    const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.15)' : 'rgba(0, 0, 0, 0.1)';

    popupChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [
                { label: 'CO', data: chartData.CO, borderColor: '#ff4d4d', backgroundColor: '#ff4d4d', borderWidth: 3, pointRadius: 5, pointHoverRadius: 8, tension: 0.3, fill: false },
                { label: 'NO2', data: chartData.NO2, borderColor: '#38bdf8', backgroundColor: '#38bdf8', borderWidth: 3, pointRadius: 5, pointHoverRadius: 8, tension: 0.3, fill: false },
                { label: 'O3', data: chartData.O3, borderColor: '#facc15', backgroundColor: '#facc15', borderWidth: 3, pointRadius: 5, pointHoverRadius: 8, tension: 0.3, fill: false },
                { label: 'SO2', data: chartData.SO2, borderColor: '#fb923c', backgroundColor: '#fb923c', borderWidth: 3, pointRadius: 5, pointHoverRadius: 8, tension: 0.3, fill: false },
                { label: 'PM10', data: chartData.PM10, borderColor: '#4ade80', backgroundColor: '#4ade80', borderWidth: 3, pointRadius: 5, pointHoverRadius: 8, tension: 0.3, fill: false },
                { label: 'PM2.5', data: chartData.PM25, borderColor: '#c084fc', backgroundColor: '#c084fc', borderWidth: 3, pointRadius: 5, pointHoverRadius: 8, tension: 0.3, fill: false }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: textColor,
                        font: { size: 13, weight: 'bold' },
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    padding: 12,
                    titleFont: { size: 14, weight: 'bold' },
                    bodyFont: { size: 13 },
                    callbacks: {
                        label: function (context) {
                            return ` ${context.dataset.label}: ${context.raw} µg/m³`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: { color: textColor, font: { size: 12, weight: '600' } },
                    grid: { color: gridColor }
                },
                y: {
                    ticks: {
                        color: textColor,
                        font: { size: 12, weight: '600' },
                        callback: function (value) {
                            return value + ' µg/m³';
                        }
                    },
                    grid: { color: gridColor }
                }
            }
        }
    });
}

// // LOGIKA BACKGROUND CUACA DINAMIS (DYNAMICBACKGROUND)
// function updateDynamicBackground(weatherForecastList, fallbackCondition) {
//     const body = document.body;
//     const currentHour = new Date().getHours();

//     let currentCondition = fallbackCondition || 'Cerah';

//     if (weatherForecastList && weatherForecastList.length > 0) {
//         const matchedForecast = weatherForecastList.find(item => {
//             const forecastHour = parseInt(item.time.split(/[:.]/)[0], 10);
//             return forecastHour === currentHour;
//         });

//         if (matchedForecast && matchedForecast.condition) {
//             currentCondition = matchedForecast.condition;
//         }
//     }

//     const cond = currentCondition.toLowerCase();
//     const isRain = cond.includes('hujan');
//     const isCloudy = cond.includes('berawan') || cond.includes('mendung');

//     body.className = "min-h-screen text-slate-800 dark:text-slate-100 transition-all duration-1000 font-sans overflow-x-hidden bg-gradient-to-b";

//     let bgClasses = "";

//     if (isRain) {
//         bgClasses = "from-[#334155] via-[#1e293b] to-[#0f172a]";
//     } else if (isCloudy && (currentHour >= 6 && currentHour < 18)) {
//         bgClasses = "from-[#64748b] via-[#475569] to-[#334155]";
//     } else {
//         if (currentHour >= 0 && currentHour < 3) {
//             bgClasses = "from-[#020617] via-[#0f172a] to-[#1e1b4b]"; // Tengah Malam
//         } else if (currentHour >= 3 && currentHour < 6) {
//             bgClasses = "from-[#0f172a] via-[#2e1065] to-[#581c87]"; // Subuh
//         } else if (currentHour >= 6 && currentHour < 9) {
//             bgClasses = "from-[#38bdf8] via-[#818cf8] to-[#c084fc]"; // Pagi
//         } else if (currentHour >= 9 && currentHour < 12) {
//             bgClasses = "from-[#0284c7] via-[#38bdf8] to-[#7dd3fc]"; // Menjelang Siang
//         } else if (currentHour >= 12 && currentHour < 15) {
//             bgClasses = "from-[#0369a1] via-[#0284c7] to-[#38bdf8]"; // Siang
//         } else if (currentHour >= 15 && currentHour < 18) {
//             bgClasses = "from-[#1d4ed8] via-[#7e22ce] to-[#c2410c]"; // Sore/Senja
//         } else if (currentHour >= 18 && currentHour < 21) {
//             bgClasses = "from-[#0f172a] via-[#1e1b4b] to-[#311042]"; // Malam Awal
//         } else {
//             bgClasses = "from-[#090d16] via-[#0f172a] to-[#1e1b4b]"; // Malam Larut
//         }
//     }

//     body.classList.add(...bgClasses.split(' '));
// }

// LOGIKA BACKGROUND CUACA DINAMIS (DYNAMICBACKGROUND)
function updateDynamicBackground(weatherForecastList, fallbackCondition) {
    const body = document.body;
    const currentHour = new Date().getHours();
    const isDarkMode = document.documentElement.classList.contains('dark');

    let currentCondition = fallbackCondition || 'Cerah';

    if (weatherForecastList && weatherForecastList.length > 0) {
        const matchedForecast = weatherForecastList.find(item => {
            const forecastHour = parseInt(item.time.split(/[:.]/)[0], 10);
            return forecastHour === currentHour;
        });

        if (matchedForecast && matchedForecast.condition) {
            currentCondition = matchedForecast.condition;
        }
    }

    const cond = currentCondition.toLowerCase();
    const isRain = cond.includes('hujan');
    const isCloudy = cond.includes('berawan') || cond.includes('mendung');

    let bgClasses = "";

    if (isDarkMode) {
        // ==========================================
        // DARK MODE (Makin Malam Makin Gelap Pekat)
        // ==========================================
        if (isRain) {
            bgClasses = "from-[#334155] via-[#1e293b] to-[#0f172a]";
        } else if (isCloudy && (currentHour >= 6 && currentHour < 18)) {
            bgClasses = "from-[#475569] via-[#334155] to-[#1e293b]";
        } else {
            if (currentHour >= 0 && currentHour < 3) {
                bgClasses = "from-[#020617] via-[#090d16] to-[#0f172a]"; 
            } else if (currentHour >= 3 && currentHour < 6) {
                bgClasses = "from-[#0f172a] via-[#2e1065] to-[#3b0764]"; 
            } else if (currentHour >= 6 && currentHour < 9) {
                bgClasses = "from-[#1e3a8a] via-[#1e1b4b] to-[#0f172a]"; 
            } else if (currentHour >= 9 && currentHour < 12) {
                bgClasses = "from-[#0369a1] via-[#0f172a] to-[#1e293b]"; 
            } else if (currentHour >= 12 && currentHour < 15) {
                bgClasses = "from-[#0284c7] via-[#1e293b] to-[#0f172a]"; 
            } else if (currentHour >= 15 && currentHour < 18) {
                bgClasses = "from-[#1d4ed8] via-[#7e22ce] to-[#c2410c]"; 
            } else if (currentHour >= 18 && currentHour < 21) {
                bgClasses = "from-[#0f172a] via-[#1e1b4b] to-[#311042]"; 
            } else {
                bgClasses = "from-[#090d16] via-[#0f172a] to-[#1e1b4b]"; 
            }
        }
    } else {
        // ==========================================
        // LIGHT MODE (Makin Malam Makin Redup Soft)
        // ==========================================
        if (isRain) {
            bgClasses = "from-[#cbd5e1] via-[#e2e8f0] to-[#f1f5f9]";
        } else if (isCloudy) {
            bgClasses = "from-[#e2e8f0] via-[#f1f5f9] to-[#ffffff]";
        } else {
            if (currentHour >= 0 && currentHour < 3) {
                bgClasses = "from-[#94a3b8] via-[#cbd5e1] to-[#e2e8f0]"; 
            } else if (currentHour >= 3 && currentHour < 6) {
                bgClasses = "from-[#fbcfe8] via-[#f3e8ff] to-[#e0e7ff]"; 
            } else if (currentHour >= 6 && currentHour < 9) {
                bgClasses = "from-[#7dd3fc] via-[#bae6fd] to-[#e0f2fe]"; 
            } else if (currentHour >= 9 && currentHour < 12) {
                bgClasses = "from-[#38bdf8] via-[#7dd3fc] to-[#bae6fd]"; 
            } else if (currentHour >= 12 && currentHour < 15) {
                bgClasses = "from-[#0ea5e9] via-[#38bdf8] to-[#7dd3fc]"; 
            } else if (currentHour >= 15 && currentHour < 18) {
                bgClasses = "from-[#fdba74] via-[#fbcfe8] to-[#ddd6fe]"; 
            } else if (currentHour >= 18 && currentHour < 21) {
                bgClasses = "from-[#c7d2fe] via-[#e0e7ff] to-[#eef2ff]"; 
            } else {
                bgClasses = "from-[#cbd5e1] via-[#e2e8f0] to-[#f1f5f9]"; 
            }
        }
    }

    // Reset total class body agar tidak bentrok dengan warna lama
    body.className = "min-h-screen text-slate-800 dark:text-slate-100 transition-all duration-1000 font-sans overflow-x-hidden bg-gradient-to-b " + bgClasses;
}

// LOGIKA DARK MODE TAILWIND
// function toggleDarkMode() {
//     const isDark = document.documentElement.classList.toggle('dark');
//     localStorage.setItem('theme', isDark ? 'dark' : 'light');
//     updateThemeButton(isDark);

//     if (currentChartData) {
//         renderChart(currentChartData);
//         if (popupChart) {
//             renderPopupChart(currentChartData);
//         }
//     }
// }

// LOGIKA DARK MODE TAILWIND
function toggleDarkMode() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeButton(isDark);

    // FIX: Panggil update background agar background langsung berubah saat tombol diklik!
    if (currentDetails) {
        updateDynamicBackground(currentDetails.weather_forecast, currentDetails.weather_current.condition);
    } else {
        updateDynamicBackground([], 'Cerah');
    }

    if (currentChartData) {
        renderChart(currentChartData);
        if (popupChart) {
            renderPopupChart(currentChartData);
        }
    }
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const isDark = savedTheme === 'light' ? false : true;

    if (isDark) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
    updateThemeButton(isDark);
}

function updateThemeButton(isDark) {
    const btn = document.getElementById('theme-btn');
    if (btn) {
        btn.innerText = isDark ? '🌙 Dark Mode' : '☀️ Light Mode';
    }
}

// LOGIKA DASHBOARD & FETCH API
function updateDashboard(locationId) {
    console.log("Mengubah lokasi ke:", locationId);

    fetch(`/api/dashboard/${locationId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Data berhasil diambil:", data);
            const details = data.details;
            const chartData = data.chart_data;

            currentDetails = details;
            currentChartData = chartData;

            // 0. Update Background Cuaca Dinamis berdasarkan Jam & Prakiraan Cuaca
            updateDynamicBackground(details.weather_forecast, details.weather_current.condition);

            // 1. Update Widget Ringkasan Cuaca
            document.getElementById('widget-temp').innerText = details.weather_current.temp;
            document.getElementById('widget-wind').innerText = details.weather_current.wind;
            document.getElementById('widget-cond').innerText = details.weather_current.condition;

            // 2. Update Kartu Polutan
            document.getElementById('val-co').innerText = `${details.pollutants.CO} µg/m3`;
            document.getElementById('val-no2').innerText = `${details.pollutants.NO2} µg/m3`;
            document.getElementById('val-pm25').innerText = `${details.pollutants.PM25} µg/m3`;
            document.getElementById('val-pm10').innerText = `${details.pollutants.PM10} µg/m3`;
            document.getElementById('val-o3').innerText = `${details.pollutants.O3} µg/m3`;
            document.getElementById('val-so2').innerText = `${details.pollutants.SO2} µg/m3`;

            // 3. Update Catatan
            document.getElementById('note-text').innerText = details.note;

            // 4. Render Forecast ISPU
            renderIspuForecast(details.ispu_forecast);

            // 5. Render Forecast Cuaca
            renderWeatherForecast(details.weather_forecast);

            // 6. Update Line Chart
            renderChart(chartData);
        })
        .catch(err => console.error("Error fetching data:", err));
}

function renderIspuForecast(forecastList) {
    const container = document.getElementById('ispu-forecast-container');
    if (!container) return;
    container.innerHTML = '';
    forecastList.forEach((item, index) => {
        container.innerHTML += `
            <div onclick="openIspuModal(${index})" class="card-box card-interactive p-3 rounded-2xl text-center">
                <div class="text-xs opacity-75">${item.date}</div>
                <div class="text-xl my-1">${item.icon}</div>
                <div class="font-bold text-sm mb-0.5">${item.value}</div>
                <div class="text-[11px] opacity-90">${item.status}</div>
            </div>
        `;
    });
}

function renderWeatherForecast(forecastList) {
    const container = document.getElementById('weather-forecast-container');
    if (!container) return;
    container.innerHTML = '';
    forecastList.forEach((item, index) => {
        let icon = '☀️';
        const cond = item.condition ? item.condition.toLowerCase() : '';
        if (cond.includes('hujan')) icon = '🌧️';
        else if (cond.includes('berawan') || cond.includes('mendung')) icon = '⛅';

        container.innerHTML += `
            <div onclick="openWeatherModal(${index})" class="card-box card-interactive p-3 rounded-2xl text-center">
                <div class="text-xs opacity-75">${item.time}</div>
                <div class="text-xl my-1">${icon}</div>
                <div class="font-bold text-sm mb-0.5">${item.temp}</div>
                <div class="text-[11px] opacity-90">${item.condition}</div>
            </div>
        `;
    });
}

function renderChart(chartData) {
    const canvas = document.getElementById('pollutantChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    if (pollutantChart) {
        pollutantChart.destroy();
    }

    const isDarkMode = document.documentElement.classList.contains('dark');
    const textColor = isDarkMode ? '#f8fafc' : '#1e293b';
    const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.15)' : 'rgba(0, 0, 0, 0.1)';

    pollutantChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [
                { label: 'CO', data: chartData.CO, borderColor: '#ff4d4d', tension: 0.3, fill: false },
                { label: 'NO2', data: chartData.NO2, borderColor: '#38bdf8', tension: 0.3, fill: false },
                { label: 'O3', data: chartData.O3, borderColor: '#facc15', tension: 0.3, fill: false },
                { label: 'SO2', data: chartData.SO2, borderColor: '#fb923c', tension: 0.3, fill: false },
                { label: 'PM10', data: chartData.PM10, borderColor: '#4ade80', tension: 0.3, fill: false },
                { label: 'PM2.5', data: chartData.PM25, borderColor: '#c084fc', tension: 0.3, fill: false }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            resizeDelay: 100,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: textColor }
                }
            },
            scales: {
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                y: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                }
            }
        }
    });
}

// JALANKAN CLOCK REALTIME
updateRealtimeClock();
setInterval(updateRealtimeClock, 1000);

// ======================================================
// FIX LAYOUT & CHART SAAT MINIMIZE -> MAXIMIZE
// ======================================================

let resizeTimeout;

function handleDashboardResize() {
    clearTimeout(resizeTimeout);

    resizeTimeout = setTimeout(() => {

        // Tunggu browser menyelesaikan perubahan ukuran/layout
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {

                if (currentChartData) {

                    // Buat ulang chart dengan ukuran container terbaru
                    renderChart(currentChartData);

                    // Kalau popup chart sedang terbuka
                    if (popupChart) {
                        renderPopupChart(currentChartData);
                    }
                }

            });
        });

    }, 250);
}


// Resize browser
window.addEventListener('resize', handleDashboardResize);


// Beberapa browser Windows lebih konsisten menangkap perubahan
// viewport melalui visualViewport
if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', handleDashboardResize);
}


// Saat halaman kembali aktif
window.addEventListener('pageshow', () => {
    handleDashboardResize();
});