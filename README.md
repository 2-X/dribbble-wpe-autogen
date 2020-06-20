# Dribbble Wallpaper Autogenerator
[Dribble](https://dribbble.com/) has some top-tier animators.

I wrote a script that logs into your Dribbble account, downloads all of your liked animations, 
and turns them into Wallpaper Engine web backgrounds.
Credits for the artists are autogenerated and added to the project's description.
All animations are shown at the center of their wallpaper, regardless of screen dimensions.
All wallpapers have a slider that lets the user adjust the size of the GIF at the center of the wallpaper.

The following wallpapers were made using this script:

- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/all-day-long/index.html" target="_blank">All Day Long</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/a-metaphor-for-being-a-motion-designer/index.html" target="_blank">A Metaphor for Being a Motion Designer</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/animalators/index.html" target="_blank">Animalators</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/arnold-with-his-balloon/index.html" target="_blank">Arnold with his Balloon</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/canned-day/index.html" target="_blank">Canned Day</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/cannibals/index.html" target="_blank">Cannibals</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/cat-things/index.html" target="_blank">Cat Things</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/dog/index.html" target="_blank">Dog</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/dont-talk-to-me-or-my-son-ever-again/index.html" target="_blank">Don't Talk To Me Or My Son Ever Again</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/h-e-l-l-36-days-of-type/index.html" target="_blank">H E L L - 36 Days of Type</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/intelligence-visual-exploration-for-ios-product/index.html" target="_blank">Intelligence Visual Exploration</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/jelly-man/index.html" target="_blank">Jelly Man</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/love-hurts/index.html" target="_blank">Love Hurts</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/l-for-light/index.html" target="_blank">L for Light</a>
- <a href="https://htmlpreview.github.io/?https://github.com/kriispy/dribbble-wpe-autogen/blob/master/examples/morning-mood/index.html" target="_blank">Morning Mood</a>


Also all of my wallpapers published to the [Steam Community](https://steamcommunity.com/id/xkriizpy/myworkshopfiles/?appid=431960&sort=score&browsefilter=myfiles&view=imagewall) were made using this tool.


**Instructions:**
1. Make a [Dribble](https://dribbble.com/) account if you haven't.
2. Find some animations you like and like them.
3. Clone this repo.
4. Install [FFMPEG](https://ffmpeg.org/download.html).
5. Install the python dependencies for this project using `python3 -m pip install selenium Pillow xmltodict`
6. Make sure Chrome or Chromium is installed since it uses Sellenium Chromedriver to scrape your likes.
7. Run `python3 create_backgrounds.py`
8. Wait for it to download all wallpapers to the `downloads` folder.
9. Add your wallpapers to Wallpaper Engine by clicking on Wallpaper Editor, creating a new wallpaper, and selecting the `index.html` file inside each folder in `downloads`.
10. If you want, automatically remove your likes by pasting the contents of [remove_dribble_likes.js](./remove_dribble_likes.js) in your browser's debug console.

**Notes:**

- Sometimes it gets the background color slightly wrong. In that case you can manually edit or (in the usually the more likely scenario that the border color is not the same as the rest of the animation's background) you can just let it.
