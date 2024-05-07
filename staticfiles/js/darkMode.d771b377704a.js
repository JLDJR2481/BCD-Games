
const toLightIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="white" class="bi bi-brightness-low" viewBox="0 0 16 16"> <path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6m0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8m.5-9.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0m0 11a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0m5-5a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1m-11 0a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1m9.743-4.036a.5.5 0 1 1-.707-.707.5.5 0 0 1 .707.707m-7.779 7.779a.5.5 0 1 1-.707-.707.5.5 0 0 1 .707.707m7.072 0a.5.5 0 1 1 .707-.707.5.5 0 0 1-.707.707M3.757 4.464a.5.5 0 1 1 .707-.707.5.5 0 0 1-.707.707" /></svg>';


const toDarkIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-moon" viewBox="0 0 16 16"><path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278M4.858 1.311A7.27 7.27 0 0 0 1.025 7.71c0 4.02 3.279 7.276 7.319 7.276a7.32 7.32 0 0 0 5.205-2.162q-.506.063-1.029.063c-4.61 0-8.343-3.714-8.343-8.29 0-1.167.242-2.278.681-3.286"/></svg>';

function setDarkMode() {
    var parser = new DOMParser();
    var modeButton = document.getElementById("darkModeToggle");
    var logoImage = document.querySelector('#logo');

    document.body.id = "dark";
    var svgNode = parser.parseFromString(toLightIcon, "image/svg+xml").documentElement;
    localStorage.setItem('mode', 'dark');

    logoImage.src = "/static/images/logotipo-without-background-darkmode.png";

    modeButton.removeChild(modeButton.firstElementChild);
    modeButton.appendChild(svgNode);

}

function setLightMode() {
    var parser = new DOMParser();
    var modeButton = document.getElementById("darkModeToggle");
    var logoImage = document.querySelector('#logo');

    document.body.id = "light";
    var svgNode = parser.parseFromString(toDarkIcon, "image/svg+xml").documentElement;
    localStorage.setItem('mode', 'light');

    logoImage.src = "/static/images/logotipo-without-background.png";

    modeButton.removeChild(modeButton.firstElementChild);
    modeButton.appendChild(svgNode);
}

function darkModeToggle() {
    var bodyMode = document.body.id;

    if (bodyMode == "light") {
        setDarkMode();
    }
    else if (bodyMode == "dark") {
        setLightMode();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var savedMode = localStorage.getItem('mode');
    if (savedMode) {
        document.body.id = savedMode;
        if (savedMode === 'dark') {
            setDarkMode();
        } else {
            setLightMode();
        }
    }
});
