// Coundown timer begins for project, quiz and packages Expiry
const durationTimer = document.getElementById("duration-timer")
const durationCountdownTimer = document.getElementById("duration-countdown-timer")

const durationDate = Date.parse(durationTimer.textContent)

const countDownMaster = setInterval(() => {
    const dateNow = new Date().getTime()

    const durationDatewDiff = durationDate - dateNow

    const d = Math.floor(durationDate / (1000 * 60 * 60 * 24) - (dateNow / (1000 * 60 * 60 * 24)))
    const h = Math.floor((durationDate / (1000 * 60 * 60) - (dateNow / (1000 * 60 * 60))) % 24)
    const m = Math.floor((durationDate / (1000 * 60) - (dateNow / (1000 * 60))) % 60)
    const s = Math.floor((durationDate / (1000) - (dateNow / (1000))) % 60)

    if (durationDatewDiff > 0) {
        durationCountdownTimer.innerHTML = d + " D: " + h + " H: " + m + " M: " + s + " S"
    }
    else {
        clearInterval(countDownMaster)
        durationCountdownTimer.innerHTML = "Time Expired"
    }
}, 1000)
// Coundown timer ends for project Expiry















