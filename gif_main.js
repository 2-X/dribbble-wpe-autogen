let top1 = 0;
let left1 = 0;

let bottom1 = 100;
let left2 = 0;

let bottom2 = 100;
let right1 = 100;

let top2 = 0;
let right2 = 100;

const crop = () => {
    document.getElementById("main-img").style["clip-path"] = `polygon(${left1}% ${top1}%, ${left2}% ${bottom1}%, ${right1}% ${bottom2}%, ${right2}% ${top2}%)`;
}

window.wallpaperPropertyListener = {
    applyUserProperties: (properties) => {
        if (properties.size) {
            document.getElementById("main-img").style.height = properties.size.value + "px";
        }

        if (properties["crop-left"]) {
            let val = properties["crop-left"].value;
            left1 = val;
            left2 = val;
            crop();
        }

        if (properties["crop-right"]) {
            let val = properties["crop-right"].value;
            right1 = 100 - val;
            right2 = 100 - val;
            crop();
        }

        if (properties["crop-top"]) {
            let val = properties["crop-top"].value;
            top1 = val;
            top2 = val;
            crop();
        }

        if (properties["crop-bottom"]) {
            let val = properties["crop-bottom"].value;
            bottom1 = 100 - val;
            bottom2 = 100 - val;
            crop();
        }
    }
};
