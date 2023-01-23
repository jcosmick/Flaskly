function hideElement(el){
    el.style.display = "none"
}

function showElementBlock(el){
    el.style.display = "block"
}

function showElementInline(el){
    el.style.display = "inline"
}

function toggleDisplay(el){
    if(el.style.display === 'none')
        showElement(el)
    else
        hideElement(el)
}

function isChecked(el){
    return el.checked
}