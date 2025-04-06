import os

if os.name == 'nt':
    print("This is a Windows system")
elif os.name == 'posix':
    print("This is a Unix/Linux/Mac OS system")
else:
    print(f"This is an unknown operating system type: {os.name}")