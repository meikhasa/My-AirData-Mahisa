class ISPUConverter:
    # Tabel Batas Konversi ISPU (Permen LHK No. 14 Tahun 2020)
    # Format: (Xb, Xa, Ib, Ia) - Batas kontinu tanpa gap
    BOUNDS = {
        "PM25": [
            (0.0, 15.0, 0, 50),
            (15.0, 55.0, 51, 100),
            (55.0, 150.0, 101, 200),
            (150.0, 250.0, 201, 300),
            (250.0, 500.0, 301, 500),
        ],
        "PM10": [
            (0.0, 50.0, 0, 50),
            (50.0, 150.0, 51, 100),
            (150.0, 350.0, 101, 200),
            (350.0, 420.0, 201, 300),
            (420.0, 500.0, 301, 500),
        ],
        "CO": [
            (0.0, 4000.0, 0, 50),
            (4000.0, 8000.0, 51, 100),
            (8000.0, 15000.0, 101, 200),
            (15000.0, 30000.0, 201, 300),
            (30000.0, 45000.0, 301, 500),
        ],
        "NO2": [
            (0.0, 80.0, 0, 50),
            (80.0, 200.0, 51, 100),
            (200.0, 1130.0, 101, 200),
            (1130.0, 2260.0, 201, 300),
            (2260.0, 3000.0, 301, 500),
        ],
        "SO2": [
            (0.0, 52.0, 0, 50),
            (52.0, 180.0, 51, 100),
            (180.0, 400.0, 101, 200),
            (400.0, 800.0, 201, 300),
            (800.0, 1200.0, 301, 500),
        ],
        "O3": [
            (0.0, 120.0, 0, 50),
            (120.0, 235.0, 51, 100),
            (235.0, 400.0, 101, 200),
            (400.0, 800.0, 201, 300),
            (800.0, 1000.0, 301, 500),
        ],
    }

    @classmethod
    def calculate_ispu(cls, pollutant_type, conc):
        """Menhitung Sub-Indeks ISPU berdasarkan konsentrasi mentah."""
        if conc is None or pollutant_type not in cls.BOUNDS:
            return None

        try:
            conc = float(conc)
        except (ValueError, TypeError):
            return None

        # Antisipasi konsentrasi negatif
        if conc <= 0:
            return 0

        # Loop cek rentang
        for Xb, Xa, Ib, Ia in cls.BOUNDS[pollutant_type]:
            if Xb <= conc <= Xa:
                ispu_val = ((Ia - Ib) / (Xa - Xb)) * (conc - Xb) + Ib
                return round(ispu_val)

        # Jika konsentrasi melebihi batas teratas tabel Permen LHK
        last_Xb, last_Xa, last_Ib, last_Ia = cls.BOUNDS[pollutant_type][-1]
        if conc > last_Xa:
            ispu_val = ((last_Ia - last_Ib) / (last_Xa - last_Xb)) * (conc - last_Xb) + last_Ib
            return round(ispu_val)

        return 0

    @classmethod
    def get_category(cls, ispu_val):
        """Menentukan kategori berdasarkan nilai ISPU."""
        if ispu_val is None:
            return "Tidak Ada Data"
        if ispu_val <= 50:
            return "Baik"
        elif ispu_val <= 100:
            return "Sedang"
        elif ispu_val <= 200:
            return "Tidak Sehat"
        elif ispu_val <= 300:
            return "Sangat Tidak Sehat"
        else:
            return "Berbahaya"