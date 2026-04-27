import os
import struct

def create_pak(input_folders, output_pak):
    """
    Membuat file .pak standar GoldSrc/Quake.
    input_folders: List folder yang akan dimasukkan (misal: ['addons', 'image'])
    output_pak: Nama file hasil (misal: 'pak0.pak')
    """
    file_list = []
    current_offset = 12  # Header size (4 + 4 + 4)
    
    # Kumpulkan semua file
    for folder in input_folders:
        if not os.path.exists(folder):
            print(f"Peringatan: Folder {folder} tidak ditemukan.")
            continue
            
        for root, dirs, files in os.walk(folder):
            for file in files:
                # Lewati file skrip Python atau git
                if file.endswith('.py') or file.startswith('.') or file.endswith('.rar'):
                    continue
                    
                full_path = os.path.join(root, file)
                # Path di dalam PAK harus pakai forward slash /
                pak_path = full_path.replace("\\", "/").strip("/")
                
                size = os.path.getsize(full_path)
                file_list.append({
                    'path': pak_path,
                    'full_path': full_path,
                    'size': size,
                    'offset': 0 # Akan diisi nanti
                })

    # Tulis data file ke buffer sementara
    with open(output_pak, 'wb') as pak:
        # Tulis placeholder header
        pak.write(struct.pack('<4sII', b'PACK', 0, 0))
        
        # Tulis kontent file
        for f in file_list:
            f['offset'] = pak.tell()
            with open(f['full_path'], 'rb') as src:
                pak.write(src.read())
            print(f"Packing: {f['path']}")

        # Tulis Directory (Lump)
        dir_offset = pak.tell()
        for f in file_list:
            # Entry directory: 56 bytes (52 bytes name, 4 bytes offset, 4 bytes size)
            name_bytes = f['path'].encode('ascii')[:51]
            pak.write(struct.pack('<52sII', name_bytes, f['offset'], f['size']))
        
        dir_size = len(file_list) * 56
        
        # Kembali ke awal untuk isi header asli
        pak.seek(0)
        pak.write(struct.pack('<4sII', b'PACK', dir_offset, dir_size))

    print(f"\nSelesai! File {output_pak} telah dibuat.")
    print(f"Lokasi: {os.path.abspath(output_pak)}")
    print("\nCara pakai:")
    print(f"1. Letakkan {output_pak} di folder utama game (PROJECT LOBBY CSPB).")
    print("2. Anda bisa coba pindahkan (backup) folder /addons dan /image ke tempat lain.")
    print("3. Jalankan game. Jika game tetap tampil, berarti PAK berhasil terbaca.")

if __name__ == "__main__":
    # Karena kita menjalankan dari addons/neda, kita anggap folder ini adalah root sumber
    # Tapi di dalam PAK, game butuh path diawali 'addons/neda/'
    
    # Skrip akan membungkus folder saat ini (.) dan folder image di dalamnya
    # Kita akan memodifikasi prefix-nya agar sesuai standar game
    
    file_list = []
    output_pak = 'pak0.pak'
    
    # Folder-folder yang ingin dimasukkan
    # . berarti semua file di folder neda (character, weapons, dll)
    # image berarti folder image di dalam neda
    source_folders = ['.'] 

    for folder in source_folders:
        for root, dirs, files in os.walk(folder):
            # Hindari folder tools dan file .pak itu sendiri
            if 'tools' in root or '.git' in root:
                continue
                
            for file in files:
                if file.endswith('.py') or file.endswith('.rar') or file == output_pak:
                    continue
                    
                full_path = os.path.join(root, file)
                # Path asli di disk (misal: "character/page1.cfg")
                rel_path = os.path.relpath(full_path, '.').replace("\\", "/")
                
                # Path di dalam PAK yang dicari game (misal: "addons/neda/character/page1.cfg")
                pak_path = f"addons/neda/{rel_path}".strip("/")
                
                size = os.path.getsize(full_path)
                file_list.append({
                    'path': pak_path,
                    'full_path': full_path,
                    'size': size,
                    'offset': 0
                })

    # Tulis PAK
    with open(output_pak, 'wb') as pak:
        pak.write(struct.pack('<4sII', b'PACK', 0, 0))
        for f in file_list:
            f['offset'] = pak.tell()
            with open(f['full_path'], 'rb') as src:
                pak.write(src.read())
            print(f"Packing: {f['path']}")

        dir_offset = pak.tell()
        for f in file_list:
            name_bytes = f['path'].encode('ascii')[:51]
            pak.write(struct.pack('<52sII', name_bytes, f['offset'], f['size']))
        
        dir_size = len(file_list) * 56
        pak.seek(0)
        pak.write(struct.pack('<4sII', b'PACK', dir_offset, dir_size))

    print(f"\nSelesai! {output_pak} dibuat di {os.getcwd()}")
