import os
from pip._internal.utils.misc import get_installed_distributions

def main():
    total_size = 0
    for package in get_installed_distributions():
        package_size = sum(os.path.getsize(os.path.join(d, f))
                           for d, _, files in os.walk(package.location)
                           for f in files)
        total_size += package_size

    print(f"Total size of installed packages: {total_size} bytes")

if __name__ == "__main__":
    main()

