// TODO: finish setCellState, make styling better, tie number of guesses + answers to cookies, add favicon

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
        }).then((res) => res.json()).then((data) => createStatRow(data) /*console.log(data)*/);

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
    var r = document.createElement("div");
    r.setAttribute("class", "game_table_row");

    console.log(data);
    if (data["answer"]) {
        input.setAttribute("disabled", "");
        alert("congratulations");
    }
    fetch('/retrieve_categories').then((res) => res.json()).then((categories) => {
        for (category of categories) {
            e = document.createElement("div");
            setCellState(data, e, category);
            r.appendChild(e);
        }
    });

    game_table.appendChild(r);

}

// Finish setCellState function
function setCellState(data, cell, stat) {
    if(data[stat]["equality"] == 2) {
        cell.setAttribute("class", "game_table_cell_high");
    }else if (data[stat]["equality"] == 1) {
        cell.setAttribute("class", "game_table_cell_equal");
    }else {
        cell.setAttribute("class", "game_table_cell_low");
    }
    cell.innerHTML = data[stat]["value"];
}