window.wallpaperPropertyListener = {
    applyUserProperties: (properties) => {
        if (properties.size) {
            document.getElementById("main-img").style.height = properties.size.value + "px";
        }
    }
};
