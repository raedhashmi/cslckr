const flash = document.querySelector('.flash');

function flasher() {
    flash.style.display = 'block';
    setTimeout(() => {
        flash.style.display = 'none'; 
    }, 150);
    setTimeout(flasher, 100);
}
flasher()