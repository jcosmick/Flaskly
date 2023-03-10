//Ricerca gli elementi con il titolo cercato dall'utente tramite l'apposita barra di ricerca
function search(toFind){
    const grafDivButtons = document.getElementById('grafici').getElementsByClassName('graf-div')
    console.log(grafDivButtons)
    elements = grafDivButtons.length ? grafDivButtons : [grafDivButtons];
    for(el of elements){
        if(el.querySelectorAll(".graf-button-title")[0].innerText.toLowerCase().includes(toFind.toLowerCase()))
            showElementFlex(el)
        else
            hideElement(el)
    }
}

