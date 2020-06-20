import cv2
import os
import time
import re
import subprocess
import shutil
import urllib.request

# pip install image
from PIL import Image, ImageFilter

from utils.base_webdriver import BaseWebDriver
from utils.json_utils import save_json_file, load_json_file

def download_dribbble_likes(username, password, output_folder=None, bwd=None):
    """ log into Dribbble and fetch all of your likes using Selenium"""
    # make a new webdriver by default
    should_clean_webdriver = False
    if bwd is None:
        bwd = BaseWebDriver()
        should_clean_webdriver = True
    
    # save to the current folder by default
    if output_folder is None:
        output_folder = os.getcwd()

    # load the sign-in page
    bwd.get("https://dribbble.com/session/new")
    
    # log in
    print("Logging in.")
    username_input = bwd.get_elem("""document.getElementById("login")""")
    password_input = bwd.get_elem("""document.getElementById("password")""")
    bwd.send_keys(username_input, username, speed=0.01)
    bwd.send_keys(password_input, password, speed=0.01)
    bwd.js("""document.querySelector("input[value='Sign In']").click()""")

    # load the likes page
    print("Loading the likes page.")
    bwd.get(f"https://dribbble.com/{username}/likes")

    # scroll to the bottom of the page
    bottom_of_page = False
    while not bottom_of_page:
        print("Scrolling to bottom of page.")
        bottom_of_page = bwd.js("""
            const reachedBottomOfPage = document.getElementsByClassName("null-message")[0];
            if (!reachedBottomOfPage) {
                document.getElementsByClassName("form-btn load-more")[0].click()
                window.scrollTo(0, document.body.scrollHeight)
                return false;
            } else {
                return true;
            }
        """)
        time.sleep(0.1)

    # scrape all info and links
    print("Scraping info for all likes from page.")
    sources = bwd.js("""
        sources = []
        Array.from(document.getElementsByClassName("shot-thumbnail")).forEach(e => {
            const nameNode = e.getElementsByClassName("shot-title")[0];
            const name = nameNode && nameNode.innerText;
            const authorURLNode = e.querySelector("a[rel='contact']");
            const authorURL = authorURLNode && authorURLNode.getAttribute("href");
            const authorNode = e.getElementsByClassName("display-name")[0];
            const author = authorNode && authorNode.innerText;

            // is it a GIF or an MP4?
            let mediaSource;
            let imageSource = e.querySelector("img").getAttribute("src").replace("_1x", "");
            if (imageSource.includes(".png")) { // mp4
                mediaSource = e.children[0].getAttribute("data-video-teaser-large").replace("_large_preview", "");
            } else { // gif
                mediaSource = imageSource;
            }

            // add to sources
            sources.push({
                "src": mediaSource,
                "name": name,
                "author_url": "https://dribbble.com" + authorURL,
                "author": author,
            })
        });
        return sources;
    """)

    # destroy webdriver if we created it just for this instance
    print("Closing webdriver.")
    if should_clean_webdriver:
        bwd.quit()

    print(f"Starting download of {len(sources)} liked files.")

    # create downloads folder
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # download all GIF and MP4 files
    i = 0
    for source in sources:
        # increment
        i += 1

        # build output name
        file_type = source["src"].split(".")[-1]
        cleaned_name = slugify(source['name'])

        # 
        if cleaned_name is None:
            continue


        output_filename = cleaned_name + "." + file_type
        output_folder = os.path.join("downloads", cleaned_name)

        # make folder if it doesn"t exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # if it does exist, skip it
        else:
            continue

        # print debug info
        print(f"{i}/{len(sources)} - Downloading {source['name']} by {source['author']}")

        # download it!
        filepath = f"{output_folder}/{output_filename}"
        urllib.request.urlretrieve(source["src"], filepath)

        # save credits.json
        save_json_file(source, os.path.join(output_folder, "credits.json"))
    
    print("Finished downloading.")


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    if value is None:
        return None
    value = unicodedata.normalize("NFKD", value)
    value = str(re.sub("[^\\w\\s-]", "", value).strip().lower())
    value = str(re.sub("[-\\s]+", "-", value))
    return value


def make_backgrounds():
    # get all files to convert (in subfolders of the downloads folder)
    files_to_convert = []
    for subdir, dirs, _ in os.walk("downloads"):
        for d in dirs:
                for subsubdir, _, files in os.walk(os.path.join(subdir, d)):
                        for file in files:
                                files_to_convert.append(os.path.join(subsubdir, file).replace("\\", "/"))
    
    for filepath in files_to_convert:
        # get some required things
        file_type = filepath.split(".")[-1]
        media_folder = os.path.join(os.getcwd(), "/".join(filepath.split("/")[:-1]))
        media_filename = filepath.split("/")[-1]

        # skip non-gif and non-mp4 files
        if file_type not in ["gif", "mp4"]:
            continue

        def escape(str):
            return str.replace('"', '\\"').replace("\\", "\\\\")

        # get the credits.json info
        metadata = load_json_file(os.path.join(media_folder, "credits.json"))
        metadata_name = escape(metadata.get("name"))
        metadata_author = escape(metadata.get("author"))

        # turn into a Wallpaper Engine web wallpaper
        if file_type == "mp4":
            # convert MP4 to WEBM
            # (because Wallpaper Engine requires .webm)
            print("Converting MP4 to GIF")
            full_input_filename = os.path.join(media_folder, media_filename)
            media_filename = media_filename.replace(".mp4", ".gif")
            filepath = filepath.replace(".mp4", ".gif")
            full_output_filename = os.path.join(media_folder, media_filename)

            # use FFMPEG to convert
            # the "-n" flag auto-skips converting if the output already exists
            # the "-y" flag auto-converts if the output already exists (no prompt)
            os.system(f'ffmpeg -y -i {full_input_filename} -vf "fps=30,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 {full_output_filename}')

            # remove mp4 file
            try:
                os.remove(full_input_filename)
            except OSError:
                pass

        # create preview.png
        save_first_frame_of_gif(filepath, os.path.join(media_folder, "preview"))

        # find color for background
        background_color = get_image_background_color(filepath)

        # load HTML template
        with open("gif_template.html", "r", encoding="utf-8") as f:
            gif_template = f.read()
        
        # format HTML template
        gif_template = gif_template.replace("$FILENAME", media_filename)
        gif_template = gif_template.replace("$COLOR", background_color)
        gif_template = gif_template.replace("$TITLE", metadata_name)

        # write HTML to file
        with open(f"{media_folder}/index.html", "w", encoding="utf-8") as f:
            f.write(gif_template)

        # copy main.js into folder
        shutil.copy(os.path.join(os.getcwd(), "gif_main.js"), media_folder)

        # load project.json template
        with open("project_template.json", "r", encoding="utf-8") as f:
            project_template = f.read()

        # format project.json template
        project_template = project_template.replace("$DESCRIPTION", (
            f"{metadata_name} was made by {metadata_author} on Dribbble. "
            f"Check them out at {metadata['author_url']}"
        ))
        project_template = project_template.replace("$COLOR", background_color)
        project_template = project_template.replace("$PREVIEW", "preview.png")
        project_template = project_template.replace("$TITLE", metadata_name)

        # write project.json to file
        with open(f"{media_folder}/project.json", "w", encoding="utf-8") as f:
            f.write(project_template)

def save_first_frame_of_gif(filepath, output_filename):
    # open image
    im = Image.open(filepath)

    # transfer palette from GIF to image
    palette = im.getpalette()
    im.putpalette(palette)

    # save first frame
    new_im = Image.new("RGBA", im.size)
    new_im.paste(im)
    new_im.save(output_filename + ".png")

def get_image_background_color(filepath):
    # open GIF
    im = Image.open(filepath)
    rgb_im = im.convert("RGB")
    
    # get RGB values of top-left pixel
    r, g, b = rgb_im.getpixel((0, 0))

    return rgb_to_hex(r, g, b)

def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

if __name__ == "__main__":
    credentials_filename = "creds.json"
    creds = load_json_file(credentials_filename)
    username = creds.get("username")
    password = creds.get("password")

    if not username:
        raise ValueError(f"You need to add your username to {credentials_filename}!")

    if not password:
        raise ValueError(f"You need to add your password to {credentials_filename}!")

    download_dribbble_likes(username, password)
    make_backgrounds()
