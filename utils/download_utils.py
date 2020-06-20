import os
import platform
import requests
import zipfile
import subprocess

from .get_chrome_version import required_chromedriver_version

def download_ngrok(force_download=False):
    """Downloads ngrok.

    Downloads ngrok to the './bin' folder.

    Args:
        force_download (bool, optional): Download and overwrite any existing ngrok.
            Defaults to False.

    Returns:
        str: The path to the executable.

    Examples:
        # on windows
        >>> download_chromedriver(force_download)
        ./bin/ngrok.exe
        # on mac/linux
        >>> download_chromedriver(force_download)
        ./bin/ngrok
    """
    # URLs for ngrok downloads
    base_url = "https://bin.equinox.io/c/4VmDzA7iaHb/"
    linux_suffix = "ngrok-stable-linux-amd64.zip"
    mac_suffix = "ngrok-stable-darwin-amd64.zip"
    windows_suffix = "ngrok-stable-windows-amd64.zip"

    # download the executable and return the path to the executable
    return download_executable(
        base_url,
        "ngrok",
        linux_suffix,
        mac_suffix,
        windows_suffix,
        force_download=force_download
    )


def download_chromedriver(force_download=False):
    """Downloads the necessary chromedriver.

    Downloads chromedriver version for the required chromedriver version
    for the matching operating system to the './bin' folder.

    Args:
        force_download (bool, optional): Download and overwrite any existing chromedrivers.
            Defaults to False.

    Returns:
        str: The path to the executable.

    Examples:
        # on windows
        >>> download_chromedriver(force_download)
        ./bin/chromedriver.exe
        # on mac/linux
        >>> download_chromedriver(force_download)
        ./bin/chromedriver

    Notes:
        This downloads from http://chromedriver.chromium.org/downloads.
        Go there if this breaks because a new version of Chrome came out,
        and update the `required_chromedriver_version()` function.
    """
    # URLs for chromedriver Downloads
    base_url = f"https://chromedriver.storage.googleapis.com/{required_chromedriver_version()}/"
    linux_suffix = "chromedriver_linux64.zip"
    mac_suffix = "chromedriver_mac64.zip"
    windows_suffix = "chromedriver_win32.zip"

    # download the executable and return the path to the executable
    return download_executable(
        base_url,
        "chromedriver",
        linux_suffix,
        mac_suffix,
        windows_suffix,
        force_download=force_download
    )


def download_executable(
    base_url, name,
    linux_url_suffix, mac_url_suffix, windows_url_suffix,
    force_download=False,
    to_folder="bin"
):
    """Downloads an executable from the given URL.

    First determines what system you are running on,
    then uses that info to get download the correct
    version of the executable.

    Args:
        base_url (str): The base url to download from.
        name (str): The filename to save
        linux_url_suffix (str): The suffix for the linux download.
        mac_url_suffix (str): The suffix for the mac download.
        windows_url_suffix (str): The suffix for the windows download.
        force_download (bool, optional): Download and overwrite any existing
            executables with the same name. Defaults to False.
        to_folder (str, optional): The folder to download to. Defaults to "bin".

    Returns:
        str: The path to the executable.

    Raises:
        Exception: If you're not running on Windows, Linux, or Mac OS.

    Examples:
        >>> download_executable(
        ...     "https://chromedriver.storage.googleapis.com/76.0.3809.25",
        ...     "chromedriver",
        ...     "chromedriver_linux64.zip",
        ...     "chromedriver_mac64.zip",
        ...     "chromedriver_win32.zip"
        ... )
        ./bin/chromedriver
    """
    # get current working directory and system version
    system_version = platform.system()

    # path to binaries download folder
    path_to_bin = f"{os.getcwd()}/{to_folder}/"

    # create bin if it doesn't exist
    if not os.path.exists(path_to_bin):
        os.makedirs(path_to_bin)

    # match chromedriver to the right version based on the OS
    # set the filepaths to the zip file and the extracted chromedriver executable
    if system_version == "Linux":
        path_to_executable_zip = path_to_bin + linux_url_suffix
        path_to_executable = path_to_bin + name
        download_url = base_url + linux_url_suffix
    elif system_version == "Darwin":
        path_to_executable_zip = path_to_bin + mac_url_suffix
        path_to_executable = path_to_bin + name
        download_url = base_url + mac_url_suffix
    elif system_version == "Windows":
        path_to_executable_zip = path_to_bin + windows_url_suffix
        path_to_executable = path_to_bin + f"{name}.exe"
        download_url = base_url + windows_url_suffix
    else:
        raise Exception(f"Invalid operating system: {system_version}!")

    # download executable if it doesn't exist
    if not os.path.isfile(path_to_executable) or force_download:

        # remove previous version of executable
        if os.path.isfile(path_to_executable):
            os.remove(path_to_executable)

        # download zip file
        r = requests.get(download_url)

        # write zip file to folder
        with open(path_to_executable_zip, 'wb') as f:
            f.write(r.content)

        # extract zip file
        zip_ref = zipfile.ZipFile(path_to_executable_zip, 'r')
        zip_ref.extractall(path_to_bin)
        zip_ref.close()

        # delete zip file - we don't need it anymore
        os.remove(path_to_executable_zip)

        # format plaintext executable as a unix executable for Linux and MacOS
        if system_version != "Windows":
            subprocess.Popen(["chmod", "+x", path_to_executable])

    # return the path to the executable
    return path_to_executable
