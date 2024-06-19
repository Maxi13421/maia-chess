import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

max_procs = 10



input_file = r"C:\Users\magle\Desktop\Dateien\Python\maia-chess\lichess_Maxi13421_2024-06-12.pgn"
output_files = r"C:\Users\magle\Desktop\Dateien\Python\maia-chess\output"

os.makedirs(output_files, exist_ok=True)
os.makedirs(os.path.join(output_files, 'blocks'), exist_ok=True)
os.makedirs(os.path.join(output_files, 'training'), exist_ok=True)
os.makedirs(os.path.join(output_files, 'validation'), exist_ok=True)

os.chdir(os.path.join(output_files, 'blocks'))

# Path to pgn-extract.exe
pgn_extract_path = os.path.join(os.getcwd(), r'C:\Users\magle\Desktop\Dateien\Python\maia-chess\pgn-extract.exe')

# Run pgn-extract
# Default war 1000
subprocess.run([pgn_extract_path, '-7', '-C', '-N', '-#100', input_file], check=True)

# Move the first 3000 PGN files to the validation set
# Aktuell 900
for i in range(1, 10):
    src = f"{i}.pgn"
    dst = os.path.join(output_files, 'validation', f"{i}.pgn")
    if os.path.exists(src):
        os.rename(src, dst)

# Move the rest of the PGN files to the training set
for pgn_file in os.listdir('.'):
    if pgn_file.endswith('.pgn'):
        os.rename(pgn_file, os.path.join(output_files, 'training', pgn_file))

os.chdir('..')
#shutil.rmtree(os.path.join(output_files, 'blocks'))


def process_pgn(data_type, p):
    p_num = p.replace('.pgn', '')
    print(f"Starting on {data_type} {p_num}")
    p_dir = os.path.join(output_files, data_type, p_num)
    os.makedirs(p_dir, exist_ok=True)
    subprocess.run([r'C:\Users\magle\Desktop\Dateien\Python\maia-chess\trainingdata-tool.exe', os.path.join(output_files, data_type, p)], cwd=p_dir)


# Process PGN files for training and validation sets
for data_type in ['training', 'validation']:
    data_path = os.path.join(output_files, data_type)
    pgn_files = [f for f in os.listdir(data_path) if f.endswith('.pgn')]

    with ThreadPoolExecutor(max_workers=max_procs) as executor:
        futures = {executor.submit(process_pgn, data_type, p): p for p in pgn_files}
        for future in as_completed(futures):
            p = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {data_type} {p}: {e}")

print("Almost done")
print("Done")