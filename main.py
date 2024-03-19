import os
import time

from utils.models import continue_prompt, get_year_month, oracle_sql, create_folder, check_pd_files, copy_files, rename_file, replace_text_in_file

#########################################
######### Main script execution #########
#########################################

if __name__ == "__main__":
    print('===================== CHPA CR PD files pre-processing started... =====================')
    # Get year and month from user input
    year, month = get_year_month()
    period = year + month

    # Format PD folder month
    if month.startswith('0'):
        month_pd = month[-1]
    else:
        month_pd = month
    month_pd = int(month_pd)
    print('Current period is:', period)
    print('Period for PD directory is:', f'{month_pd}M{year[2:]}', '\n')
    continue_prompt()
    time.sleep(2)

    # Check SYNC
    oracle_sql(period)
    continue_prompt()
    time.sleep(2)

    # CHPA CR raw data source (local): \\shasts004p\IA_Hospital\SVNpro\Customized Report\MSD.Regional\RawData\yyyymm 
    # CHPA CR raw data source (server): F:\Shared4SASUsers\IA_Hospital\SVNpro\Customized Report\MSD.Regional\RawData\yyyymm
    # CHPA CR raw data source (network_TZ_end): r'Z:\SVNpro\Customized Report\MSD.Regional\RawData'
    # PD source: \\bejsfps02\Feng Mingzhu\hospital\MSD project\mmMyy
    # PD source (network_TZ_end): r'P:\\'

    print('===================== Working directories Check =====================')
    cr_directory = os.getcwd()
    DC_root_dir = r'Z:\SVNpro\Customized Report\MSD.Regional\RawData'
    PD_root_dir = r'P:\\'
    folder_path = os.path.join(DC_root_dir, period)
    source_path = os.path.join(PD_root_dir, f'{month_pd}M{year[2:]}')
    print('Current python source file directory is:', cr_directory)
    print('DS China raw data path is:', folder_path)
    print('PD source path is:', source_path, '\n')
    continue_prompt()
    time.sleep(2)

    # Create folder
    create_folder(folder_path)
    continue_prompt()
    time.sleep(2)   

    # Check completeness of the files in PD source folder
    check_pd_files(source_path)
    continue_prompt()
    time.sleep(2)

    # Copy files
    copy_files(source_path, folder_path)
    continue_prompt()
    time.sleep(2) 
    
    # Rename file
    rename_file(folder_path)
    continue_prompt()
    time.sleep(2)

    # # Replace text in file
    # replace_text_in_file(folder_path, '""', '" "')
    print('===================== CHPA CR PD files pre-processing ended... =====================')
    print("===================== Please mannualy replace text in 'pack.csv'! =====================")