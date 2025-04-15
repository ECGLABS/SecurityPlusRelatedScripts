import subprocess

def check_webcam_usage():
    try:
        output = subprocess.check_output(['lsof', '/dev/video0'], stderr=subprocess.DEVNULL).decode()
        if output:
            print("⚠️ Webcam is IN USE!")
            print(output)
        else:
            print("✅ Webcam is NOT in use.")
    except subprocess.CalledProcessError:
        print("✅ Webcam is NOT in use.")
    except FileNotFoundError:
        print("Error: lsof not found. Install with `sudo pacman -S lsof`")

if __name__ == "__main__":
    check_webcam_usage()
