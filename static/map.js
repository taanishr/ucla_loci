const form = document.getElementById("form");
const input = document.getElementById("input");
const num_guesses = document.getElementById("num_guesses")
const game_table = document.getElementById("game_table")

function modifyTextContent(elem, text) {
    elem.textContent = text;
}

fetch('/reset').then((res) => res.json()).then((data) => setPlaceholder(input, data["num_guesses"]));

var arr = []
fetch('/retrive_careers').then((res) => res.json()).then((data) => arr = Object.keys(data))

form.addEventListener("input", (e) => {
    closeLists();

    var a, b; 
    const formData = new FormData(form);
    var val = formData.get("guess")

    a = document.createElement("div");
    a.setAttribute("class", "autocomplete-items")

    e.target.parentNode.appendChild(a);

    for (i = 0; i < arr.length; i++) {
        if (val.length > 0 && (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase())) {
            if (a.childElementCount < 5) {
                b = document.createElement("div");
                b.setAttribute("name", "player")
                b.innerHTML = "<b>" + arr[i] + "</b>";
    
                a.appendChild(b)
            }
        }
    }
})

form.addEventListener("submit", (e) => {
    e.preventDefault();

    var val = "";

    if(document.getElementsByName("player").length > 0) {
        val = document.getElementsByName("player")[0].textContent;

        fetch("/submit_guess", {
            method: 'POST',
            headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify({'guess' : val})
        }).then((res) => res.json()).then((data) => createStatRow(data))

        fetch("/num_guesses", {
            method: 'POST'
        }).then((res) => res.json()).then((data) => setPlaceholder(input, data["num_guesses"]));

        input.value = "";

        closeLists();
    }
})


function closeLists() {
    var lists = document.getElementsByClassName("autocomplete-items")
    for (i = 0; i < lists.length; i++) {
        lists[i].parentNode.removeChild(lists[i])
    }
}

function setPlaceholder(elem, value) {
    elem.setAttribute("placeholder", value + " Guesses Remaining")
}

function createStatRow(data) {
    r = document.createElement("div");
    r.setAttribute("class", "game_table_row");

    ppg = document.createElement("div");
    setCellState(data, ppg, "PPG")

    rpg = document.createElement("div");
    setCellState(data, rpg, "RPG")

    apg = document.createElement("div");
    setCellState(data, apg, "APG")

    fg = document.createElement("div");
    setCellState(data, fg, "FG%") 

    game_table.appendChild(ppg);
    game_table.appendChild(rpg);
    game_table.appendChild(apg);
    game_table.appendChild(fg);

    game_table.appendChild(r);
}

function setCellState(data, cell, stat) {
    cell.setAttribute("class", "game_table_cell");

    if  (data[stat] == true) {
        cell.innerHTML = "<b>↑</b>"
    }else{
        cell.innerHTML = "<b>↓</b>"
    }
}