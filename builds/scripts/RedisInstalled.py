from os import chdir
from os.path import dirname, abspath, join
chdir(join(dirname(abspath(__file__)), ".."))

import importlib.util
import sys
from os import getcwd

def is_package_installed(package_name):
    spec = importlib.util.find_spec(package_name)
    return spec is not None

# Example usage
package_name = "redis"  # Change this to the package you want to check
if is_package_installed(package_name):
    print(f"{package_name} is installed.")
    config = join(getcwd(), 'scripts', 'config.txt')
    file = open(config, 'r').read().replace('redis: false', 'redis: true')
    with open(config, 'w') as f:
        f.write(file)
    sys.exit(0)  # Exit with code 0 indicating success
else:
    print(f"{package_name} is not installed.")
    sys.exit(1)  # Exit with code 1 indicating failure
