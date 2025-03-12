import json
import struct
import zipfile
import os
import zlib

error_str = ""

def calculate_crc32(filename, chunk_size=4096):
    checksum = 0
    with open(filename, 'rb') as file:
        while chunk := file.read(chunk_size):
            checksum = zlib.crc32(chunk, checksum)
    return checksum

def read_bps_crc32(bps_path):
    with open(bps_path, 'rb') as f:
        data = f.read()
    
    if data[:3] != b'BPS':
        raise ValueError("Invalid BPS file header")
    
    # CRC32 values are stored in the last 12 bytes of the file
    expected_crc32 = struct.unpack('<III', data[-12:])[0]
    return expected_crc32

def create_theme_archive(theme_name, theme_author, theme_id, theme_region, bps_files_info, output_path):
     is_running = True
     do_checksums_match = False
 
     bps_files = []
     og_files = []
     menu_paths = []
 
     for bps_path, og_path, menu_path in bps_files_info:
         bps_checksum = read_bps_crc32(bps_path)
         og_checksum = calculate_crc32(og_path)
 
         if bps_checksum == og_checksum:
             bps_files.append(bps_path)
             og_files.append(og_path)
             menu_paths.append(menu_path)
             do_checksums_match = True
         else:
             print(f"Error: Checksums don't match for BPS file: {bps_path}. You likely inputted the wrong bps or original rom.")
             error_str = f"Error: Checksums don't match for BPS file: {bps_path}. You likely inputted the wrong bps or original rom."
             do_checksums_match = False
             break
     
     if theme_region == "Universal":
         theme_region_str = theme_region.upper()
     elif theme_region == "Japan":
         theme_region_str = "JPN"
     elif theme_region == "America":
         theme_region_str = "USA"
     elif theme_region == "Europe":
         theme_region_str = "EUR"
 
     if do_checksums_match:
         metadata = {
             "Metadata": {
                 "themeName": theme_name,
                 "themeAuthor": theme_author,
                 "themeID": theme_id,
                 "themeRegion": theme_region_str
             }
         }
 
         patches = {}
         for bps, menu in zip(bps_files, menu_paths):
             bps_filename = os.path.basename(bps)
             patches[bps_filename] = menu
 
         data = {**metadata, "Patches": patches}
 
         utheme_output_path = output_path

         with zipfile.ZipFile(utheme_output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
             for bps in bps_files:
                 archive.write(bps, os.path.basename(bps))
 
             metadata_json = json.dumps(data, indent=4)
             archive.writestr("metadata.json", metadata_json)
 
         print(f"Created utheme: {utheme_output_path} successfully!")
         return 0
     else:
         print("Failure to write theme metadata file")
         return error_str


