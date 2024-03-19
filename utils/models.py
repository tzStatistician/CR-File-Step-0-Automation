import os
import time
import re
import cx_Oracle
import sys
import shutil
import fileinput

# Ask user to continue program or not
def continue_prompt():
    while True:
        user_input = input("Do you want to continue? (Y/N): ").strip().upper()
        if user_input == 'Y':
            break  # Exit the prompt loop and continue the program
        elif user_input == 'N':
            print("===================== Exiting the program by user ... =====================")
            sys.exit()  # Exit the program immediately
        else:
            print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")

# Get current year and month by user input
def get_year_month():
    # Define year and month pattern
    year_pattern = r"^\d{4}$"  # Pattern for four digits
    month_pattern = r"^(0[1-9]|1[0-2])$"  # Pattern for months 01-12

    while True:
        year = input("Enter the current year (yyyy): ")
        if re.match(year_pattern, year):
            break  # Exit loop if year is valid
        else:
            print("Invalid year format. Please enter the year again in 'yyyy' format.")

    while True:
        month = input("Enter the current month (mm): ")
        if re.match(month_pattern, month):
            break  # Exit loop if month is valid
        else:
            print("Invalid month format. Please enter the month again in 'mm' format (01-12).")

    return year, month

# Execute sql in python to check whether SYNC is updated 
def oracle_sql(period):
    print('===================== SYNC database check operation starting... =====================')
    # configure the Oracle client. Solution reference: https://stackoverflow.com/questions/56119490/cx-oracle-error-dpi-1047-cannot-locate-a-64-bit-oracle-client-library
    lib_dir = r"C:\Users\u1158100\Desktop\oracleinstantclient_21_13\instantclient-basic-windows.x64-21.13.0.0.0dbru\instantclient_21_13"
    
    try:
    # Get the Oracle client version
        version = cx_Oracle.clientversion()
        print("Oracle is connected. Oracle client version:", version)
    except cx_Oracle.DatabaseError as e:
        print("Oracle is not connected. Error message shows:", e, ". Will try to initialize Oracle client.")
        try:
        # Initialize the Oracle client with the specified library directory
            cx_Oracle.init_oracle_client(lib_dir=lib_dir)
            print("Oracle client initialized successfully. Oracle client version:", cx_Oracle.clientversion())
        except cx_Oracle.DatabaseError as e:
            print("Failed to initialize Oracle client. Error message shows", e)
            sys.exit("Exiting program due to Oracle client initialization failure.")

    # Configure the Oracle connection
    conf="IMS_DATA_SHARE/IMS_DATA_SHARE@shauorl001p.internal.imsglobal.com:1521/IMSORA.internal.imsglobal.com"
    sql = f"""
    SELECT COUNT(1)
    FROM IMS_APPLI.SYNC_FACT_ALL_INFO
    WHERE SALE_DATE = TO_DATE(:period, 'YYYYMM')
    ORDER BY TO_CHAR(SALE_DATE, 'YYYYMM')
    """
    try:
        conn = cx_Oracle.connect(conf) 
        cur = conn.cursor()
        cur.execute(sql, [period])
        count = cur.fetchone()[0]
        print("IMS_APPLI.SYNC_FACT_ALL_INFO databesed successfully updated.")
        print(f"Count of data for {period} is: {count}")
    except cx_Oracle.DatabaseError as e:
        print("SQL fails. Please check IMS_APPLI.SYNC_FACT_ALL_INFO. Error message shows:", e)
        sys.exit()

    finally:
    # Close the cursor and connection to release resources
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    print('===================== SYNC database check operation ending... =====================\n')

# Create folder if it doesn't exist
def create_folder(path):
    print('===================== Folder creation operation starting... =====================')
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Folder '{path}' created.")
    else:
        print(f"Folder '{path}' already exists.")
    print('===================== Folder creation operation ending... =====================\n')

# Check completeness of the files in PD source folder
def check_pd_files(path):
    print('===================== PD files check operation starting... =====================')
    files = ['cudu.csv', 'CUQ_vertical_simple.csv', 'lab.csv', 'manuflg.csv', 'ndf.CSV', 'pack.csv', 'product.csv', 'product_molecule.csv', 'product_molecule_updated.csv']

    # Check if the files exist
    for file in files:
        if os.path.exists(os.path.join(path, file)):
            print(f"'{file}' exists.")
        else:
            print(f"'{file}' does not exist.")
            print('===================== PD files are not completely uploaded. Exiting program... =====================')
            sys.exit()
    print('All PD files are uploaded. Program will continue.')
    print('===================== PD files check operation ending... =====================\n')

# Copy files excluding 'product_molecule.csv'; src: source, dst: destination
def copy_files(src, dst):
    print('===================== Copy and paste operation starting... =====================')

    # List to hold the names of duplicated files
    duplicated_files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(dst, f)) and f != 'product_molecule.csv']
    
    if not duplicated_files:
        print("No duplicated files found.")

    # If there are duplicated files, ask the user what to do
    while duplicated_files:
        print("===================== The following files already exist in the destination directory: =====================")
        for filename in duplicated_files:
            print(filename)
        print("===================== Duplicate Files List End. =====================")

        user_input = input("Files above already exist. Do you want to remove the existing files? (Y/N): ").strip().upper()
        if user_input == 'Y':
            print("===================== Start removing existing files... =====================")
            for filename in duplicated_files:
                os.remove(os.path.join(dst, filename))
                print(f"'{filename}' Removed.")
            print("===================== All existing files removed. =====================")
            break  # Exit the loop and proceed with copying files
        
        elif user_input == 'N':
            user_input = input("Do you want to continue to the RENAME operation? (Y/N): ").strip().upper()
            if user_input == 'Y':
                print("===================== Existing files will be overwitten. =====================")
                break

            elif user_input == 'N':
                print("===================== Rufused to continue program. Exiting program... =====================")
                sys.exit()  # Exit the program
            else:
                print("Input format wrong. Please try again.")
                continue  # Ask the question again
        else:
            print("Input format wrong. Please try again.")

    time.sleep(2)
    print("===================== Start copying files... =====================")
    # Copy the files
    for filename in os.listdir(src):
        if filename != 'product_molecule.csv':
            src_file = os.path.join(src, filename)
            dst_file = os.path.join(dst, filename)
            print(f"Copying '{filename}'...")
            shutil.copy2(src_file, dst_file)
            print(f"'{filename}' copied.")
    print("===================== All files copied. =====================")
    print('===================== Copy and paste operation ending... =====================\n')

# Function to rename 'product_molecule_updated.csv' to 'product_molecule.csv'
def rename_file(path):
    print('===================== File renaming operation started... =====================')
    original = os.path.join(path, 'product_molecule_updated.csv')
    changed = os.path.join(path, 'product_molecule.csv')
    if os.path.exists(changed):
        user_input = input("The file 'product_molecule.csv' already exists. Do you want to remove it? (Y/N): ").strip().upper()
        if user_input == 'Y':
            print(f"Removing '{changed}'...")
            os.remove(changed)
            print(f"'{changed}' Removed.")
        elif user_input == 'N':
            print("Renaming cannot be done if 'product_molecule.csv' exists. Exiting program...")
            sys.exit()
        else:
            print("Input format wrong. Please try again.")

    if os.path.exists(original):
        print(f"'{original}' detected.")
        print(f"Renaming '{original}' to '{changed}'...")
        os.rename(original, changed)
        print(f"'{original}' renamed to '{changed}'.")
    else:
        print(f"'{original}' does not exist.")
        print('===================== Exiting program... =====================\n')
    print('===================== File renaming operation ending... =====================\n')

# Function to replace "" with " " in 'pack.csv'
def replace_text_in_file(path, search_text, replace_text):
    file_path = os.path.join(path, 'pack.csv')
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            print(line.replace(search_text, replace_text), end='')