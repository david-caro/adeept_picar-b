#!/usr/bin/python3
# File name   : setup.py
# Author      : Adeept
# Date        : 2020/3/14

import argparse
import os
import subprocess
import sys
import time

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)


def replace_line(path, match, replacement):
    newline = ""
    str_num = str(replacement)
    with open(path, "r") as f:
        for line in f.readlines():
            if line.find(match) == 0:
                line = str_num + "\n"
            newline += line
    with open(path, "w") as f:
        f.writelines(newline)


def install_pocketsphinx():
    run = subprocess.check_call
    run(
        [
            "wget",
            "https://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz/download",
            "-O",
            "sphinxbase.tar.gz",
        ]
    )

    run(
        [
            "wget",
            "https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz/download",
            "-O",
            "pocketsphinx.tar.gz",
        ]
    )

    run(
        [
            "tar",
            "-xzvf",
            "sphinxbase.tar.gz",
        ]
    )

    run(
        [
            "tar",
            "-xzvf",
            "pocketsphinx.tar.gz",
        ]
    )

    os.chdir("sphinxbase-5prealpha")
    try:
        run(["./configure", "-enable-fixed"])
        run(["make"])
        # run(["make", "install"])
    finally:
        os.chdir("..")


def install_create_ap():
    subprocess.check_output(
        [
            "git",
            "clone",
            "ssh://git@github.com/oblique/create_ap",
        ]
    )
    os.chdir("create_ap")
    try:
        subprocess.check_output(["/create_ap"])
        # subprocess.check_output(["make", "install"])
    finally:
        os.chdir("..")


def install_pip():
    subprocess.check_output(["pip", "install", "-r", "requirements.txt"])


def install_apt_packages():
    subprocess.check_output(["./install_apt_requirements.sh"])


def create_startup_script():
    with open(os.path.expanduser("~/startup.sh"), "w") as startup_fd:
        startup_fd.write("#!/bin/sh\nsudo python3 ~/server/webServer.py")
    # startup_fd.write(
    #     "#!/bin/sh\nsudo python3 ~/server/server.py"
    # )

    suprocess.check_output(["chmod", "777", os.path.userexpand("~/startup.sh")])

    replace_line(
        path="/etc/rc.local",
        match="fi",
        replacement="fi\n" + os.path.expanduser("~/startup.sh") + " start",
    )


def fix_conflict_with_onboard_audio():
    try:  # fix conflict with onboard Raspberry Pi audio
        os.system("sudo touch /etc/modprobe.d/snd-blacklist.conf")
        with open("/etc/modprobe.d/snd-blacklist.conf", "w") as file_to_write:
            file_to_write.write("blacklist snd_bcm2835")
    except:
        pass


def fix_i2c():
    replace_line(
        path="/boot/config.txt",
        match="#dtparam=i2c_arm=on",
        replacement="dtparam=i2c_arm=on\nstart_x=1\n",
    )


def require_sudo():
    if not os.getuid() == 0:
        raise Exception("This option should be run as root, try again adding sudo.")


def main(args: argparse.Namespace) -> int:
    if args.install_packages:
        print("Installing packages...")
        install_apt_packages()
        print("Installing packages... Done")

    if args.install_create_ap:
        print("Installing create_ap...")
        install_create_ap()
        print("Installing create_ap... Done")

    if args.install_pip:
        print("Installing pip packages...")
        install_pip()
        print("Installing pip packages... Done")

    if args.fix_i2c:
        require_sudo()
        print("Fixing i2c...")
        fix_i2c()
        print("Fixing i2c... Done")

    if args.create_startup_script:
        require_sudo()
        print("Adding startup script...")
        create_startup_script()
        print("Adding startup script... Done")

    if args.fix_audio_conflict:
        require_sudo()
        print("Fixing audio conflict...")
        fix_conflict_with_onboard_audio()
        print("Fixing audio conflict... Done")

    print(
        "The program in Raspberry Pi has been installed, disconnected and "
        "restarted. \n"
        "You can now power off the Raspberry Pi to install the camera and "
        "driver board (Robot HAT). \n"
        "After turning on again, the Raspberry Pi will automatically run the "
        "program to set the servos port signal to turn the servos to the "
        "middle position, which is convenient for mechanical assembly."
    )
    print("You migt need to restart for some changes to take effect: sudo reboot")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--install-packages", action="store_true")
    parser.add_argument("--install-pip", action="store_true")
    parser.add_argument("--install-create-ap", action="store_true")
    parser.add_argument("--fix-i2c", action="store_true")
    parser.add_argument("--fix-audio-conflict", action="store_true")
    parser.add_argument("--create-startup-script", action="store_true")
    args = parser.parse_args()
    sys.exit(main(args))
