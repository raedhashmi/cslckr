function verifyPassword() {
    const password = document.querySelector('.password-input').value;

    if (password == 'nexus') {
        window.location.href = "/success";
    } else {
        window.location.href = "/failure";
    }
}

let time = Math.floor(Math.random() * (60 - 20 + 1)) + 20;
const countdown = setInterval(function() {
    time--;
    document.querySelector('.time').textContent = time;
    if (time <= 0) {
        clearInterval(countdown);
        window.location.href = "/failure";
    }
}, 1000);