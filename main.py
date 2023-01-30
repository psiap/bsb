import subprocess
import time


def main():
    proc = subprocess.Popen(['python', "app.py"],shell=False)
    time.sleep(43200)
    proc.kill()
    time.sleep(1)

if __name__ == '__main__':
    while True:
        main()