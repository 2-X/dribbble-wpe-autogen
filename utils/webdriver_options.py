import platform
from selenium import webdriver


def get_chrome_options(
    headless=True, sandbox=False,
    dev_shm_usage=False, notifications=False,
    spoof_user_agent=True, user_agent=None,
    user_profile_dir=None, start_maximized=True,
    ignore_errors=False,
):
    # define chromium options
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')
    if not sandbox:
        chrome_options.add_argument('--no-sandbox')
    if not dev_shm_usage:
        chrome_options.add_argument('--disable-dev-shm-usage')
    if not notifications:
        chrome_options.add_argument("--disable-notifications")
    if user_profile_dir:
        chrome_options.add_argument(f"--user-data-dir={user_profile_dir}")
    
    system_version = platform.system()
    if system_version == "Linux":
        if start_maximized:
            chrome_options.add_argument(f"--kiosk")
    elif system_version == "Darwin":
        if start_maximized:
            chrome_options.add_argument(f"--kiosk")
    elif system_version == "Windows":
        if start_maximized:
            chrome_options.add_argument(f"--start-maximized")
    else:
        raise Exception(f"Invalid operating system: {system_version}!")

    # trick websites into not knowing that we are running headless
    if spoof_user_agent:
        if not user_agent:
            user_agent = (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/60.0.3112.50 Safari/537.36"
            )
        chrome_options.add_argument(f"user-agent={user_agent}")
    
    if ignore_errors:
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")

    return chrome_options
