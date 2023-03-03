function getRandomColor() {
    return "#" + Math.floor(Math.random()*16777215).toString(16);
}

function setColor(id) {
    document.getElementById(id).value = getRandomColor();
}