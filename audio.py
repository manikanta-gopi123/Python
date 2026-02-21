import requests
import zipfile
import os

links = [
    "https://wa.me.synapselive.com/images/908143438293060.ogg",
    "https://wa.me.synapselive.com/images/938279615206180.ogg",
    "https://wa.me.synapselive.com/images/3995332664091499.ogg"
]

output_zip = "my_audio_collection.zip"
temp_folder = "downloaded_audio"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def download_and_zip(url_list, zip_name):
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    downloaded_files = []
    seen_links = set()

    print("--- Starting Downloads ---")
    for url in url_list:
        if url in seen_links:
            print(f"Skipping duplicate: {url}")
            continue

        # KEEP ORIGINAL EXTENSION (.ogg)
        original_name = url.split("/")[-1]
        file_name = original_name  # <-- IMPORTANT FIX
        file_path = os.path.join(temp_folder, file_name)

        try:
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Success: {file_name}")
            downloaded_files.append(file_path)
            seen_links.add(url)

        except Exception as e:
            print(f"Failed to download {url}: {e}")

    if downloaded_files:
        print("\n--- Zipping files ---")
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file in downloaded_files:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
                    os.remove(file)

        print(f"Done! Your files are in {zip_name}")
    else:
        print("\nNo files were downloaded, so no ZIP was created.")

    if os.path.exists(temp_folder) and not os.listdir(temp_folder):
        os.rmdir(temp_folder)

if __name__ == "__main__":
    download_and_zip(links, output_zip)