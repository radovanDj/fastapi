import pip
import subprocess
import sys
import os

# check for required packages
putanja_paketa = os.path.dirname(__file__)+"requirements.txt"
try:
    subprocess.run(
        ["pip", "install", "-r ", putanja_paketa], shell=True)
    print("instalira svaki put za svaki slucaj requirements.txt")

except Exception as e:
    print(e)
