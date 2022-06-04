// Coundown timer begins

let endDate = document.getElementById("startwork-timer");
const durationNotice = document.getElementById("duration-countdown-timer")

const getDay = document.getElementById("days")
const getHour = document.getElementById("hours")
const getMinute = document.getElementById("minutes")
const getSecond = document.getElementById("seconds")

const durationDate = Date.parse(endDate.textContent)

const countDownMaster = setInterval(() => {
    const dateNow = new Date().getTime()

    const durationDatewDiff = durationDate - dateNow

    const d = Math.floor(durationDate / (1000 * 60 * 60 * 24) - (dateNow / (1000 * 60 * 60 * 24)))
    const h = Math.floor((durationDate / (1000 * 60 * 60) - (dateNow / (1000 * 60 * 60))) % 24)
    const m = Math.floor((durationDate / (1000 * 60) - (dateNow / (1000 * 60))) % 60)
    const s = Math.floor((durationDate / (1000) - (dateNow / (1000))) % 60)

    if (durationDatewDiff > 0) {
        getDay.innerHTML = d 
        getHour.innerHTML = h 
        getMinute.innerHTML = m 
        getSecond.innerHTML = s
    }
    else {
        clearInterval(countDownMaster)
        durationNotice.innerHTML = "Time Expired"
    }
}, 1000)















