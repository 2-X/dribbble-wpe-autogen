// paste this into the chrome console and it will remove all your likes without hitting the rate limit
Array.from(document.getElementsByClassName("form-btn stats-action like-shot")).forEach((e, i) => {
    setTimeout(() => { e.click() }, 400 * i)
})