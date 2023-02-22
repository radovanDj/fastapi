import subprocess


# check for required packages
try:
    subprocess.call(f"pip3 install --ignore-installed -r requirements.txt")
    print("instalira requirements.txt ako nesto fali")

except Exception as e:
    print(e)
