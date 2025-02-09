import rasterio
import numpy as np
import pandas as pd
from datetime import datetime
import os
import glob


def extract_dates_from_filename(filename):

    try:
        filename = os.path.basename(filename)

        import re

        dates = re.findall(r"20\d{6}", filename)

        if len(dates) >= 2:
            return dates[0], dates[1]

        print(f"Date non trovate nel file {filename}")
        return None, None
    except Exception as e:
        print(f"Errore nell'estrazione delle date dal file {filename}: {e}")
        return None, None


def read_tif_file(file_path):

    try:
        print(f"Elaborazione del file: {file_path}")

        start_date, end_date = extract_dates_from_filename(os.path.basename(file_path))

        with rasterio.open(file_path) as src:

            raster_data = src.read(1)

            transform = src.transform

            height, width = raster_data.shape
            rows, cols = np.mgrid[0:height, 0:width]

            xs, ys = rasterio.transform.xy(transform, rows, cols)

            lons = np.array(xs)
            lats = np.array(ys)

            df = pd.DataFrame(
                {
                    "longitude": lons.flatten(),
                    "latitude": lats.flatten(),
                    "precipitation": raster_data.flatten(),
                    "start_date": start_date,
                    "end_date": end_date,
                    "source_file": os.path.basename(file_path),
                }
            )

            df = df[df["precipitation"] != src.nodata]
            df = df.dropna()

            return df

    except Exception as e:
        print(f"Errore nella lettura del file {file_path}: {str(e)}")
        return None


def process_multiple_files(directory_path):

    all_data = []

    tif_files = glob.glob(os.path.join(directory_path, "GIOVANNI*precipitation*.tif"))

    if not tif_files:
        print(f"Nessun file TIF trovato in {directory_path}")
        return None

    print("File TIF trovati:")
    for file in tif_files:
        print(f"- {os.path.basename(file)}")

    for file_path in tif_files:
        df = read_tif_file(file_path)
        if df is not None:
            all_data.append(df)

    if all_data:

        combined_df = pd.concat(all_data, ignore_index=True)

        combined_df.sort_values("start_date", inplace=True)

        output_path = os.path.join(directory_path, "precipitation_timeseries.csv")
        combined_df.to_csv(output_path, index=False)
        print(f"\nDati salvati in: {output_path}")

        print("\nStatistiche di base delle precipitazioni:")
        print(combined_df.groupby("start_date")["precipitation"].describe())

        return combined_df

    return None


if __name__ == "__main__":

    directory_path = "."
    print("Inizio elaborazione dei file TIF...")
    data = process_multiple_files(directory_path)

    if data is not None:
        print("\nElaborazione completata con successo!")
    else:
        print("\nErrore nell'elaborazione dei file.")
