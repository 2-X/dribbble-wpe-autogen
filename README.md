# Dribbble Wallpaper Autogenerator
[Dribble](https://dribbble.com/) has some top-tier animators.

I wrote a script that logs into your Dribbble account, downloads all of your liked animations, 
and turns them into Wallpaper Engine web backgrounds.
Credits for the artists are autogenerated and added to the project's description.
All animations are shown at the center of their wallpaper, regardless of screen dimensions.
All wallpapers have a slider that lets the user adjust the size of the GIF at the center of the wallpaper.

The following wallpapers were made using this script:
- [All Day Long](./examples/all-day-long/index.html)
- [A Metaphor for Being a Motion Designer](./examples/a-metaphor-for-being-a-motion-designer/index.html)
- [Animalators](./examples/animalators/index.html)
- [Arnold with his Balloon](./examples/arnold-with-his-balloon/index.html)
- [Canned Day](./examples/canned-day/index.html)
- [Cannibals](./examples/cannibals/index.html)
- [Cat Things](./examples/cat-things/index.html)
- [Dog](./examples/dog/index.html)
- [Don't Talk To Me Or My Son Ever Again](./examples/dont-talk-to-me-or-my-son-ever-again/index.html)
- [H E L L - 36 Days of Type](./examples/h-e-l-l-36-days-of-type/index.html)
- [Intelligence Visual Exploration](./examples/intelligence-visual-exploration-for-ios-product/index.html)
- [Jelly Man](./examples/jelly-man/index.html)
- [Love Hurts](./examples/love-hurts/index.html)
- [L for Light](./examples/l-for-light/index.html)
- [Morning Mood](./examples/morning-mood/index.html)


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
