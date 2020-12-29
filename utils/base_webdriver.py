import time
import random
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities# Do not wait for full page load

from .download_utils import download_chromedriver
from .webdriver_options import get_chrome_options


class BaseWebDriver:
    def __init__(self, page_load_strategy="normal", **kwargs):

        # download the chromedriver
        self.download()

        # set up desired capabilities
        desired_capabilities = DesiredCapabilities().CHROME

        # valid values for 'page_load_strategy' are "none" and "normal"
        # "normal" means that the webdriver waits for the page to laod before executing script
        # "none" means that it doesn't wait at all
        desired_capabilities["pageLoadStrategy"] = page_load_strategy

        self.driver = webdriver.Chrome(
            executable_path=self.chromedriver_filepath,
            options=get_chrome_options(**kwargs),
            desired_capabilities=desired_capabilities
        )

        # change default loading timeout because sometimes it takes a while
        self.driver.set_page_load_timeout(120)

    def download(self):
        self.chromedriver_filepath = download_chromedriver()

    def quit(self):
        self.driver.quit()

    def get(self, url, force=False):
        """ go to the given URL if we aren't currently there
        if we are there, then just stay there
        """
        if (self.get_url() != url) or force:
            try:
                self.driver.get(url)
            except Exception:
                print(f"Error when going to the URL '{url}'!")
                raise
    
    def reload(self):
        self.get(self.get_url(), force=True)

    def inject_react_internal(self):
        self.js("""
            ReactInternal = (elem) => {
                // Object.keys() doesn't like null and undefined
                if (elem == null || elem == undefined) {
                    return;
                }
            
                // find it's react internal instance key
                let key = Object.keys(elem).find(key => key.startsWith("__reactInternalInstance$"));
            
                // get the react internal instance
                return elem[key];
            }
        """)

    def get_url(self):
        """ Get the current URL of the webpage. """
        return self.js("return window.location.href")

    def js(self, code, *args):
        """ Execute javascript code in the webdriver. """
        return self.driver.execute_script(code, *args)

    def send_keys(self, element, text, speed=0.08):
        """ Send keys at a determined rate. """
        # focus the element
        self.js("arguments[0].click();", element)
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(speed, speed+0.2))

        # wait a little between typing in elements
        time.sleep(0.5)

    def get_in_new_tab(self, url):
        """ Open given URL in a new tab. """
        if not url.startswith("https://"):
            url = f"https://{url}"
        self.js(f"""win = window.open({url});""")

    def switch_to_tab(self, tab_number):
        """ NOTE: tabs are 0-indexed """
        self.driver.switch_to.window(self.driver.window_handles[tab_number])
    
    def num_tabs(self):
        return len(self.driver.window_handles)
    
    def close_current_tab(self):
        self.driver.close()

    def switch_iframe(self, iframe_selector):
        self.driver.switch_to.frame(self.js(f"""return {iframe_selector}"""))

    def default_iframe(self):
        self.driver.switch_to.default_content()

    def get_elem(self, js_code, *args, interval=0.25, timeout=10):
        """ wait until the given xpath returns an element, or until we reach the timeout

        @js_code:   code to retrieve element (e.g. "document.getElementById('password')")
        @interval:  number of seconds to wait in between checks
        @timeout:   give up after this number of seconds has elapsed"""

        elem = None
        total_time_elapsed = 0

        # add return statement if it isn't there
        if not js_code.startswith("return"):
            js_code = f"return {js_code}"
        print(f"fetching element from {js_code}")

        # quit loop if we have found the element or reached the timeout
        while (not elem) and (total_time_elapsed < timeout):
            try:
                elem = self.js(js_code, *args)
            # BUG ignores invalid javascript code errors
            except Exception:
                pass
            if not elem:
                print(f"didn't find element, sleeping {interval} second(s)")
                total_time_elapsed += interval
                time.sleep(interval)

        # raise exception if timed out
        if (total_time_elapsed >= timeout):
            raise Exception(f"Could not find web element at '{js_code}'")
        else:
            return elem

    def scroll_by(self, pixels):
        self.driver.execute_script(f'window.scrollBy({{top: {pixels}, behavior: "smooth"}});')

    def scroll_to_end(self):
        # LOGGER.info("Scrolling to end of page")
        self.driver.execute_script('window.scrollTo({top: document.body.scrollHeight, behavior: "smooth"});')

    def scroll_to_top(self):
        # LOGGER.info("Scrolling to top of page")
        self.driver.execute_script('window.scrollTo({top: 0, behavior: "smooth"});')

    def scroll_into_view(self, element):
        self.driver.execute_script('return arguments[0].scrollIntoView({behavior: "smooth", inline: "nearest"});', element)
        # self.driver.execute_script('window.scrollBy(0, -window.innerHeight/2);')

    def page_down(self):
        # LOGGER.info("Scrolling down")
        self.driver.execute_script('window.scrollBy({top: window.innerHeight, behavior: "smooth"});')

    def page_up(self):
        # LOGGER.info("Scrolling up")
        self.driver.execute_script('window.scrollBy({top: -window.innerHeight, behavior: "smooth"});')

    def simulate_hover(self, element):
        self.js("""
            var hover_event = new MouseEvent('mouseover', {
                'view': window,
                'bubbles': true,
                'cancelable': true
            });

            arguments[0].dispatchEvent(hover_event);""",
            element
        )

    def wait_random(self, max, min=None):
        if min is None:
            time.sleep(int(max))
        else:
            time.sleep(random.randrange(int(min), int(max)))

    def random_scroll(self, seconds):
        for _ in range(seconds):
            choice = random.choice(["up", "down", "wait"])
            if choice == "up":
                self.page_up()
                self.wait_random(1)
            elif choice == "down":
                self.page_down()
                self.wait_random(1)
            else:
                self.wait_random(1)