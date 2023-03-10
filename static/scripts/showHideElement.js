function hideElement(el){
    el.style.display = "none"
}

function showElement(el){
    el.style.display = "block"
}

function showElementFlex(el)
{
    el.style.display = "flex"
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