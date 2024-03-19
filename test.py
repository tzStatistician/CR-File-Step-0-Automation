import os
import time
import re
import cx_Oracle
import sys
import shutil
import fileinput

from utils.models import get_year_month, oracle_sql, create_folder, copy_files, rename_file, replace_text_in_file

################################################
######### Main script execution - Test #########
################################################

if __name__ == "__main__":
    print('===================== CHPA CR PD files pre-processing started... =====================')
    year, month = get_year_month()
    period = year + month
    print('Current period is:', period, '\n')

    # Check SYNC
    oracle_sql(period)

    # For test, all folder will be create in the project directory
    # CHPA CR raw data source (local): \\shasts004p\IA_Hospital\SVNpro\Customized Report\MSD.Regional\RawData\yyyymm 
    # CHPA CR raw data source (server): F:\Shared4SASUsers\IA_Hospital\SVNpro\Customized Report\MSD.Regional\RawData\yyyymm
    # CHPA CR raw data source (network_TZ_end): r'Z:\SVNpro\Customized Report\MSD.Regional\RawData'
    # PD source: \\bejsfps02\Feng Mingzhu\hospital\MSD project\mmMyy
    # PD source (network_TZ_end): r'P:\\'

    print('===================== Working directories Check =====================')
    cr_directory = os.getcwd()
    folder_path = os.path.join(cr_directory, period)
    source_path = os.path.join(cr_directory, f'{month}M{year[2:]}')
    print('Current python source file directory is:', cr_directory)
    print('DS China raw data path is:', folder_path)
    print('PD source path is:', source_path, '\n')
    time.sleep(2)

    # Create folder
    create_folder(folder_path)
    time.sleep(2)   

    # Copy files
    source_path = os.path.join(cr_directory, f'{month}M{year[2:]}')
    copy_files(source_path, folder_path)
    time.sleep(2) 
    
    # Rename file
    rename_file(folder_path)

    # # Replace text in file
    # replace_text_in_file(folder_path, '""', '" "')
    print('===================== CHPA CR PD files pre-processing ended. =====================')