"""
Script for evaluating the configuration of a Raspberry Pi 800 in a student lab.

The script connects to a Raspberry Pi with a fixed IP address (10.42.0.2),
evaluates the SSH connection, retrieves content from students.txt, and performs
checks on the MySQL database structure and content.

Author: NRZ
Date: 07-dec-2023
"""
import subprocess
import shlex
import mysql.connector


def compare_table_structure(table_name, actual_structure):
    """
    Compare the structure of a table with the desired structure.

    Args:
    - table_name (str): The name of the table.
    - actual_structure (list): The actual structure of the table.

    Returns:
    - bool: True if the table structure matches the desired structure, False otherwise.
    """
    desired_columns = set(desired_structure[table_name])
    actual_columns = set(column[0] for column in actual_structure)
    if desired_columns != actual_columns:
        print("Attendu :", desired_columns)
        print("Fait :", actual_columns)
    return desired_columns == actual_columns


def print_table_content(cursor, table_name):
    """
    Print the content of a table.

    Args:
    - cursor: The MySQL cursor.
    - table_name (str): The name of the table.
    """
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    print(f"\nTable {table_name} content:")
    for row in rows:
        print(row)


def evaluate_ping(ip):
    """
    Evaluate the response to a ping command.

    Args:
    - ip (str): The IP address to ping.

    Returns:
    - bool: True if the ping is successful, False otherwise.
    """
    ping_command = ["ping", "-c", "1", ip]
    try:
        subprocess.run(ping_command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def evaluate_ssh(ip):
    """
    Evaluate SSH connection to a Raspberry Pi and retrieve content from ~/students.txt of the user student.

    Args:
    - ip (str): The IP address of the Raspberry Pi.

    Returns:
    - Tuple[bool, Optional[str]]: A tuple containing a boolean indicating SSH success and the content of students.txt (if available).
    """
    password = 'pwdstudent'
    ssh_command = f"sshpass -p {shlex.quote(password)} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null student@{ip} 'cat ~/students.txt'"
    
    try:
        ssh_output = subprocess.check_output(ssh_command, shell=True, text=True)
        
        # Check if the file is empty
        if not ssh_output.strip():
            return True, ""  # Return True with an empty string for empty file
        else:
            return True, ssh_output.strip()
    except subprocess.CalledProcessError as e:
        # Check if the error message indicates file not found
        if "No such file or directory" in e.output:
            return True, ""  # Return True with an empty string for missing file
        else:
            return False, None

# Configuration
db_config = {
    'user': 'prof',
    'password': 'pwdprof',
    'host': '10.42.0.2',
    'database': 'CAMPING',
}

# Desired structure of tables
desired_structure = {
    'ACTICAMPING': ['NumCamping', 'NumActivité', 'PrixActivité'],
    'ACTIVITE': ['NumActivité', 'NomActivité', 'TypeActivité'],
    'CAMPING': ['NumCamping', 'NomCamping', 'AddrCamping', 'TelCamping', 'DateOuv', 'DateFerm', 'NbEtoiles', 'QualitéFrance'],
}

print(db_config)

try:
    # Ping the IP
    ping_success = evaluate_ping(db_config['host'])

    if not ping_success:
        print(f"\nRaspberry at {db_config['host']}: Ping failed. Exiting and giving 0 points.")
        exit(0)
    else:
        # SSH Connection and evaluation
        ssh_success, ssh_content = evaluate_ssh(db_config['host'])
        if ssh_success:
            if ssh_content:
                print(f"\nRaspberry at {db_config['host']}: SSH connection successful. Content of students.txt:\n{ssh_content}")
            else:
                print(f"\nRaspberry at {db_config['host']}: students.txt not found or empty. Exiting and giving 7 points.")
                exit(7)
        else:
            print(f"\nRaspberry at {db_config['host']}: SSH connection failed. Exiting and giving 5 points.")
            exit(5)

        # Connect to the Raspberry Pi
        with mysql.connector.connect(**db_config) as conn, conn.cursor() as cursor:
            # Try to connect to the database
            cursor.execute("SELECT 1")

            # Evaluate database connection
            db_success = cursor.fetchone()

            if not db_success:
                print(f"\nRaspberry at {db_config['host']}: Database connection failed. Exiting and giving 11 points.")
                exit(11)
            else:
                # Loop through tables and compare structure
                tables_correct = True
                for table_name in desired_structure:
                    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                    actual_structure = cursor.fetchall()
                    print_table_content(cursor, table_name)
                    if not compare_table_structure(table_name, actual_structure):
                        tables_correct = False
                        print(f"\nRaspberry at {db_config['host']}: Attention - Table {table_name} structure does not match!")

                if not tables_correct:
                    print(f"\nRaspberry at {db_config['host']}: Database tables are not correct. Exiting and giving 16 points.")
                    exit(16)
                else:
                    # If everything is fine
                    print(f"\nRaspberry at {db_config['host']}: All checks passed. Giving 20 points.")
                    exit(20)
                    # print_table_content(cursor, 'ACTICAMPING')  # Change table name as needed

except subprocess.CalledProcessError:
    print(f"\nRaspberry at {db_config['host']}: Ping failed. Exiting and giving 0 points.")
except mysql.connector.Error as err:
    print(f"\nError connecting to Raspberry at {db_config['host']}: {err}, exiting and giving 9 points!")
    exit(9)
except Exception as e:
    print(f"An unexpected error occurred: {e}")