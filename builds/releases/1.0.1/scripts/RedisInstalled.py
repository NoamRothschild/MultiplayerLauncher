import importlib.util
import sys

def is_package_installed(package_name):
    spec = importlib.util.find_spec(package_name)
    return spec is not None

# Example usage
package_name = "redis"  # Change this to the package you want to check
if is_package_installed(package_name):
    print(f"{package_name} is installed.")
    sys.exit(0)  # Exit with code 0 indicating success
else:
    print(f"{package_name} is not installed.")
    sys.exit(1)  # Exit with code 1 indicating failure
