import os
from sigmageek_nv3 import appPalindrome
import argparse
# Download Pi file from (initial index)*100,000,000,000 to 100GB and save to STORAGE FOLDER
# Process file
# Delete file
# Increment index by number of terminals processing (5) ==> 500GB available
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--storage",
                            required=True,
                            default=None,
                            help="Folder to store 100GB of Pi")
        parser.add_argument("-i", "--index",
                            required=True,
                            default=1,
                            help="Start Index: 1 == first 100B digits")
        parser.add_argument("-m","--mod",
                            default=1,
                            required=False,
                            help="How many terminals will be processing? So it will increment Index by mod terminals")
        
        args = parser.parse_args()
        
        storage = args.storage
        index = int(args.index)
        incremental_mod = int(args.mod)
        download = 256 # Error code.
        slice_size = 750_000
        number_of_digits = 100_000_000_000
        for i in range(index, 1000, incremental_mod):
            pi_file_output = storage + f"/pi_dec_1t_{i}.txt"
            print("Checking if file already exists")
            must_download = True
            if os.path.exists(pi_file_output):
                if os.stat(pi_file_output).st_size == number_of_digits: # ToDo: Keep download from where stoped. 
                    print(f"File already downloaded and size ok.")
                    download = 0
                    must_download = False
            if must_download:              
                print(f"Downloading file: {pi_file_output}")
                download = os.system(f"cd /Volumes/SSD/pi-delivery; go run ./cmd/extract -s {i*100_000_000_000} -n {number_of_digits} > { pi_file_output }")
            
            if download == 0:
                file_out = f"out_pi_dec_1t_{i}.txt"
                print(f"Processing file. Output: {file_out}")
                try: 
                    appPalindrome(size=21, file_input=pi_file_output, slice_size=slice_size, file_output=file_out, offset=0)
                    print(f"Removing file:{pi_file_output}")
                    rm = os.system(f"rm {pi_file_output}")
                except Exception as e:
                    print(f"Error precessing file. {e}")
                    input("Press ENTER to continue.")        
            else:
                print("Error downloading file.")
                input("Press ENTER to continue.")
    except Exception as e:
        print(f"ERROR: {e}")