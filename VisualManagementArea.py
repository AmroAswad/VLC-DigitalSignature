import os
import glob
import subprocess
import time

ROOT = "C:\\Users\\Admin\\Documents\\Visual Management\\"
SAFETY = "H&S\\"
QUALITY = "QA\\"
PROJECTS = "Projects\\"
OE = "OpEx\\"
MP4 = '*.mp4'
PNG = '*.png'

DISPLAYS = ['\\\\.\\DISPLAY10', '\\\\.\\DISPLAY11', '\\\\.\\DISPLAY4', '\\\\.\\DISPLAY9', \
            '\\\\.\\DISPLAY5', '\\\\.\\DISPLAY6', '\\\\.\\DISPLAY7', '\\\\.\\DISPLAY8']

def safety_files(n=3):
    files = glob.glob(ROOT+SAFETY+MP4)
    files.extend(glob.glob(ROOT+SAFETY+PNG))
    return sorted(files, key=os.path.getmtime)[-1*n:]


def quality_files(n=1):
    files = glob.glob(ROOT+QUALITY+MP4)
    return sorted(files, key=os.path.getmtime)[-1*n:]


def oe_files(n=1):
    files = glob.glob(ROOT+OE+PNG)
    return sorted(files, key=os.path.getmtime)[-1*n:]


def projects_files(n=3):
    files = glob.glob(ROOT+PROJECTS+MP4)
    return sorted(files, key=os.path.getmtime)[-1*n:]

def sync_files(script_location):
    subprocess.run([script_location], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pass

def turnoff_screens():
    subprocess.run(["VLC Screens Off.bat"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pass


def turnon_screen(file, display):
    '''
    directx-draw
    ____________________________________
 	|DISPLAY |DISPLAY |DISPLAY |DISPLAY |
	|___10___|___11___|___8____|___9____|
	|DISPLAY |DISPLAY |DISPLAY |DISPLAY |
	|___5____|____6___|___7____|___4____|

    
    Direct3D11 - qt
    ____________________________________
 	|DISPLAY |DISPLAY |DISPLAY |DISPLAY |
	|___5____|___7____|___0____|___1____|
	|DISPLAY |DISPLAY |DISPLAY |DISPLAY |
	|___3____|___6____|___4____|___2____|
    
    '''

    subprocess.run(['VLC Screen Arrangement.bat', file, str(display)])
    pass


def turnon_screens(mode = 'normal'):

    #Safety screens 5, 6, 10
    files = safety_files()
    if len(files)!=3:
        print(f"Only {len(files)} files were found. Make sure files are mp4 format!")

    for item in zip(files, [DISPLAYS[0], DISPLAYS[4], DISPLAYS[5]]):
        file, display = item
        turnon_screen(file, display)
        print(f'{file} is displayed on {display}')
        if mode=='debug':
            input('Press any key to continue to next file...')


    #Quality screen 11
    files = quality_files()
    turnon_screen(files, DISPLAYS[1])
    print(f'{files} is displayed on {DISPLAYS[1]}')
    if mode=='debug':
        input('Press any key to continue to next file...')

    #Projects screen 9
    files = projects_files()
    turnon_screen(files, DISPLAYS[3])
    print(f'{files} is displayed on {DISPLAYS[3]}')
    if mode=='debug':
        input('Press any key to continue to next file...')

    #OE screens 4, 7, 8
    files = oe_files()
    if len(files)!=3:
        print(f"Only {len(files)} files were found. Make sure files are mp4 format!")

    for item in zip(files, [DISPLAYS[2], DISPLAYS[6], DISPLAYS[7]]):
        file, display = item
        turnon_screen(file, display)
        print(f'{file} is displayed on {display}')
        if mode=='debug':
            input('Press any key to continue to next file...')
    pass


def screens_on_time() -> bool:
    if int(time.strftime("%H" ,time.localtime()))>23 or int(time.strftime("%H" ,time.localtime()))<6:
        return False
    
    return True


def list_files() -> None:
    print(*oe_files(), sep='\n')
    print(*safety_files(), sep='\n')
    print(quality_files())
    print(projects_files())
    pass


def main():

    midnight_screens = False
    while True:
        if int(time.strftime("%H" ,time.localtime()))>7 and midnight_screens:
            turnon_screens()
            midnight_screens = False
            print(f"DISPLAYS RESTORED AT {time.ctime()}")

        if screens_on_time() and midnight_screens==False:
            user_input = input("Available options: l_files, debug, exit, turn_off. Reset Screens? [y/n] ")
            if user_input == 'y':
                turnoff_screens()

                turnon_screens()
                
                print(f"DISPLAYS RESTORED AT {time.ctime()}")

            elif user_input == 'l_files':
                list_files()

            elif user_input == 'exit':
                quit()

            elif user_input == 'turn_off':
                turnoff_screens()

            elif user_input == 'debug':
                turnoff_screens()

                turnon_screens(mode='debug')
                        
        if not screens_on_time() and midnight_screens==False:
            turnoff_screens()
            midnight_screens=True
            print(f"Screens turned off at {time.ctime()}")

        print("Press ctrl+c to exit program")


if __name__ == '__main__':
    main()