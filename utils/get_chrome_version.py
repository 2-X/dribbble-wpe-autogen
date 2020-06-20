import platform
import re
import requests
from subprocess import check_output, Popen, PIPE


def chrome_version_linux(full_version=False):
    """Get the installed version of Chrome on Linux.

    Args:
        full_version (bool, optional): Whether to return
            the full string (e.g. 78.0.3904.97) instead
            of just the main verions (e.g. 78).
            Defaults to False.

    Returns:
        str: The installed version of chrome.

    Examples:
        >>> chrome_version_linux()
        78
        >>> chrome_version_linux(full_version=False)
        78
        >>> chrome_version_linux(full_version=True)
        78.0.3904.97
    """
    # retrieve chrome version number from installation location
    linux_chrome_version_cmd = [
        "chromium-browser",
        "--version"
    ]

    # execute command and capture output
    output_bytes, _ = Popen(linux_chrome_version_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()

    # convert bytes to string
    output = "".join(map(chr, output_bytes))

    # 'output' is in the form 'blah blah NUM.NUM.NUM.NUM blah'
    # so we are going to match for NUM.NUM.NUM.NUM and return the first NUM
    full_version_string = output and re.search(r"(\d+.\d+.\d+.\d+)", output).groups()[0]

    # return the full NUM.NUM.NUM.NUM if requested
    if full_version:
        return full_version_string

    # else just return the main version number
    return re.search(r"(\d+).\d+.\d+.\d+", full_version_string).groups()[0]

def chrome_version_mac(full_version):
    """Get the installed version of Chrome on Mac OS X.

    Args:
        full_version (bool, optional): Whether to return
            the full string (e.g. 78.0.3904.97) instead
            of just the main verions (e.g. 78).
            Defaults to False.

    Returns:
        str: The installed version of chrome.

    Examples:
        >>> chrome_version_mac()
        78
        >>> chrome_version_mac(full_version=False)
        78
        >>> chrome_version_mac(full_version=True)
        78.0.3904.97
    """
    # retrieve chrome version number from installation location
    mac_chrome_version_cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--version"
    ]

    # execute command and capture output
    output_bytes, _ = Popen(mac_chrome_version_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()

    # convert bytes to string
    output = "".join(map(chr, output_bytes))

    # 'output' is in the form 'blah blah NUM.NUM.NUM.NUM blah'
    # so we are going to match for NUM.NUM.NUM.NUM and return the first NUM
    full_version_string = output and re.search(r"(\d+.\d+.\d+.\d+)", output).groups()[0]

    # return the full NUM.NUM.NUM.NUM if requested
    if full_version:
        return full_version_string

    # else just return the main version number
    return re.search(r"(\d+).\d+.\d+.\d+", full_version_string).groups()[0]


def chrome_version_windows(full_version):
    """Get the installed version of Chrome on Windows.

    Args:
        full_version (bool, optional): Whether to return
            the full string (e.g. 78.0.3904.97) instead
            of just the main verions (e.g. 78).
            Defaults to False.

    Returns:
        str: The installed version of chrome.

    Examples:
        >>> chrome_version_windows()
        78
        >>> chrome_version_windows(full_version=False)
        78
        >>> chrome_version_windows(full_version=True)
        78.0.3904.97
    """
    # get chrome version regardless of its installation location
    windows_chrome_version_cmd = 'reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version'

    # execute command and capture output
    output_bytes = check_output(windows_chrome_version_cmd, shell=True)

    # convert bytes to string
    output_string = "".join(map(chr, output_bytes))

    # 'full_version' is in the form 'blah blah NUM.NUM.NUM.NUM blah'
    # so we are going to match for NUM.NUM.NUM.NUM and return the first NUM
    full_version_string = output_string and re.search(r"(\d+.\d+.\d+.\d+)", output_string).groups()[0]

    # return the full NUM.NUM.NUM.NUM if requested
    if full_version:
        return full_version_string

    # else just return the main version number
    return re.search(r"(\d+).\d+.\d+.\d+", full_version_string).groups()[0]


def chrome_version(full_version=False):
    """Get the installed version of Chrome on this machine.

    Args:
        full_version (bool, optional): Whether to return
            the full string (e.g. 78.0.3904.97) instead
            of just the main verions (e.g. 78).
            Defaults to False.

    Returns:
        str: The installed version of chrome.

    Raises:
        Exception: If you're not running Windows, Mac, or Linux.

    Examples:
        >>> chrome_version()
        78
        >>> chrome_version(full_version=False)
        78
        >>> chrome_version(full_version=True)
        78.0.3904.97
    """
    system_verison = platform.system()
    if system_verison == "Linux":
        return chrome_version_linux(full_version=full_version)
    elif system_verison == "Darwin":
        return chrome_version_mac(full_version=full_version)
    elif system_verison == "Windows":
        return chrome_version_windows(full_version=full_version)
    else:
        raise Exception(f"Invalid operating system: {system_verison}!")


def get_matching_chromedriver_version(version):
    """Retrieves the matching chromedriver version from Google.

    Args:
        version (str): The version of Chrome.

    Returns:
        str: The latest chromedriver version associated
            with the given version of Chrome.

    Examples:
        >>> get_matching_chromedriver_version(72)
        72.0.3626.69
        >>> get_matching_chromedriver_version(78.0.3904.20)
        78.0.3904.105
    """
    version_split = version.split(".")

    # need to remove the last part of a full version number
    # because that's how Google wants it
    if len(version_split) == 4:
        version_to_send = ".".join(version_split[:3])
    else:
        version_to_send = version

    URL = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version_to_send}"
    r = requests.get(URL)
    matching_version = r.content.decode("utf-8")

    if "<Error>" in matching_version:
        raise ValueError(f"No chromedriver version found for Chrome {version}.")

    return matching_version


def required_chromedriver_version():
    """Gets the require chromedriver version number.

    Each version of Chrome has a compatible chromedriver.
    This function determines which version that is
    for your currently installed Chrome.

    Returns:
        str: The required chromedriver version.

    Raises:
        ValueError: If your installed version of Chrome is
            not yet supported in the `chromedriver_version_dict`
            defined at the top of the file. If you get this error,
            you should go to http://chromedriver.chromium.org/downloads
            and find the matching chromedriver version and update
            this dictionary.

    Examples:
        >>> required_chromedriver_version()
        78.0.3904.11
    """
    installed_chrome_version = chrome_version(full_version=True)
    version_requirement = get_matching_chromedriver_version(installed_chrome_version)

    if version_requirement is None:
        raise ValueError((
            f"The installed Chrome version '{installed_chrome_version}' "
            "does not have a matching chromedriver."
        ))

    return version_requirement
