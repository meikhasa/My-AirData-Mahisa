import requests
from flask import jsonify

class column_nasapower:
    
    @staticmethod
    def fetch_data_nasapower():
        url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
        
        # Menggunakan tanggal sesuai permintaan: 20200101 s/d 20251231
        params = {
            "parameters": "T2M,PRECTOTCORR,WS2M,QV2M",
            "community": "RE",
            "latitude": -7.2631,
            "longitude": 112.7425,
            "start": "20200101",
            "end": "20251231",
            "format": "JSON"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            print("Berhasil mengambil data dari NASA POWER API\n")
            
            return jsonify({
                "status": "success",
                "location": "Surabaya Pusat",
                "parameters_fetched": ["T2M", "PRECTOTCORR", "WS2M", "QV2M"],
                "data": data
            }), 200

        except requests.exceptions.RequestException as e:
            print(f"Gagal mengambil data NASA POWER. Error: {e}")
            return jsonify({
                "status": "error",
                "message": f"Gagal mengambil data dari NASA POWER: {str(e)}"
            }), 500