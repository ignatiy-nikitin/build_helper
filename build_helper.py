import os
import configparser


def check_config_file_existence():
    if not os.path.isfile(CONFIG_FILE):
        return False
    return True


def set_config_file():
    CONFIG.add_section('SETTINGS')
    CONFIG.set('SETTINGS', 'project_folder', '')
    CONFIG.set('SETTINGS', 'dist_folder', '')
    with open(CONFIG_FILE, 'w') as file_:
        CONFIG.write(file_)


def check_config_params():
    for param in CONFIG_PARAMS:
        if not CONFIG_SETTINGS[param]:
            return False, param
    return True, None 


CONFIG_FILE = 'config.ini'
CONFIG_PARAMS = ('project_folder', 'dist_folder')

CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_FILE)

print('Checking config file...')
if not check_config_file_existence():
    print('Config file not found. Create config file...')
    set_config_file()
    print('Could not start main program. Set config params and restart program.')
    exit()
print('Config file exists')

CONFIG_SETTINGS = CONFIG['SETTINGS']
result_of_checking_config_params, param = check_config_params()

if not result_of_checking_config_params:
    print(f'Seems like "{param}" in config is empty...')
    print('Could not start main program. Set config params and restart program.')
    exit()
print('Config params are ok')

PROJECT_FOLDER_PATH = CONFIG_SETTINGS['project_folder']
DIST_FOLDER_PATH = CONFIG_SETTINGS['dist_folder']


LIBRARIES_PATH = PROJECT_FOLDER_PATH + '\\venv\\Lib\\site-packages'
TEMP_DIST_MANAGE_PATH = PROJECT_FOLDER_PATH + '\\dist\\manage'

TEMP_DIST_LOCAL_SERVER_PATH = PROJECT_FOLDER_PATH + '\\dist\\LocalServer'
TEMP_DIST_RUNSERVER_WAITRESS_PATH = PROJECT_FOLDER_PATH + '\\dist\\runserver_waitress'


def go_to_project_folder():
    os.chdir(PROJECT_FOLDER_PATH)


def build_manage_with_pyinstaller():
    os.system('venv\\Scripts\\activate & pyinstaller manage.py --noconfirm')


def build_runserver_waitress_with_pyinstaller():
    os.system('venv\\Scripts\\activate & pyinstaller manage.py --noconfirm')


def build_local_server_with_pyinstaller():
    os.system('venv\\Scripts\\activate & pyinstaller LocalServer.py --noconfirm')


def collecting_libraries():
    os.system(f'robocopy "{LIBRARIES_PATH}" "{TEMP_DIST_MANAGE_PATH}" /E')


def collecting_templates():
    for i in os.listdir(PROJECT_FOLDER_PATH):
        if os.path.isdir(PROJECT_FOLDER_PATH + '\\' + i):
            for sub_i in os.listdir(PROJECT_FOLDER_PATH + '\\' + i):
                if os.path.isdir(PROJECT_FOLDER_PATH + '\\' + i + '\\' + sub_i) and sub_i == 'templates':
                    os.system(f'robocopy "{PROJECT_FOLDER_PATH}\\{i}" "{TEMP_DIST_MANAGE_PATH}\\{i}" /E')


def move_local_server_to_dist_folder():
    os.system(f'robocopy "{TEMP_DIST_LOCAL_SERVER_PATH}" "{DIST_FOLDER_PATH}" /E')


def move_manage_to_dist_folder():
    os.system(f'robocopy "{TEMP_DIST_MANAGE_PATH}" "{DIST_FOLDER_PATH}\\manage" /E')


def move_runserver_waitress_to_dist_folder():
    os.system(f'xcopy "{TEMP_DIST_RUNSERVER_WAITRESS_PATH}\\runserver_waitress.exe" "{DIST_FOLDER_PATH}\\manage"')


def move_bat_files():
    for f in ('run.bat', 'stop.bat', 'install.bat', 'access.bat'):
        os.system(f'xcopy "{PROJECT_FOLDER_PATH}\\{f}" "{DIST_FOLDER_PATH}"')


if __name__ == '__main__':
    go_to_project_folder()
    build_manage_with_pyinstaller()
    build_runserver_waitress_with_pyinstaller()
    build_local_server_with_pyinstaller()
    collecting_libraries()
    collecting_templates()
    move_local_server_to_dist_folder()
    move_manage_to_dist_folder()
    move_runserver_waitress_to_dist_folder()
    move_bat_files()
