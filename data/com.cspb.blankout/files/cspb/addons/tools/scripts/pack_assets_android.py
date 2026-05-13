import os
import zipfile

def create_pk3(output_name):
    """
    Membuat file .pk3 (ZIP) untuk Xash3D Android.
    Mendukung path panjang dan lebih kompatibel untuk ponsel.
    """
    # Karena kita di folder addons/neda, kita ambil file dari sini
    base_dir = '.' 
    
    with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        count = 0
        for root, dirs, files in os.walk(base_dir):
            # Lewati folder tools dan file skrip
            if 'tools' in root or '.git' in root:
                continue
                
            for file in files:
                if file.endswith('.py') or file.endswith('.rar') or file == output_name or file == 'pak0.pak':
                    continue
                    
                full_path = os.path.join(root, file)
                # Path relatif dari neda
                rel_path = os.path.relpath(full_path, base_dir).replace("\\", "/")
                
                # Path yang diharapkan game: addons/neda/...
                pak_path = f"addons/neda/{rel_path}".strip("/")
                
                # Tambahkan ke zip
                zipf.write(full_path, pak_path)
                print(f"Packing: {pak_path}")
                count += 1
                
    print(f"\nSelesai! Berhasil membungkus {count} file ke dalam {output_name}")
    print(f"Lokasi: {os.path.abspath(output_name)}")

if __name__ == "__main__":
    # Gunakan .pk3 agar Xash3D Android bisa baca path panjang
    create_pk3('pak0.pk3')
