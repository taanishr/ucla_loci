// TODO: make styling better, add win condition, change csv system to database, add favicon

const form = document.getElementById("form");
const input = document.getElementById("input");
const num_guesses = document.getElementById("num_guesses")
const game_table = document.getElementById("game_table")

reset();

loadGuesses();

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

        storeGuess(val);
        
        submitGuess(val).then((data) => createStatRow(data));

        fetch("/num_guesses", {
            method: "POST"
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

function storeGuess(name) {
    fetch("num_guesses").then((res) => res.json()).then((data) => {
        const id = 5 - data["num_guesses"];
        localStorage.setItem(id, name);
    });
}

function loadGuesses() {
    var arr = [];
    for (i = 0; i < localStorage.length; i++) {
        player = localStorage.getItem(i);
        arr.push(submitGuess(player));
    }
    
    Promise.all(arr).then((values) => {
        for (value of values) {
            createStatRow(value);
        }
    });
}

function submitGuess(player) {
    return fetch("/submit_guess", {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify({'guess' : player})
    }).then((res) => res.json())
}

function createStatRow(data) {
    var r = document.createElement("div");
    r.setAttribute("class", "game_table_row");

    player = document.createElement("div");
    player.setAttribute("class", "game_table_cell");
    player.innerHTML = data["player"];
    r.appendChild(player)

    // if (data["answer"]) {
    //     input.setAttribute("disabled", "");
    //     // alert("congratulations");
    // }

    fetch('/retrieve_categories').then((res) => res.json()).then((categories) => {
        for (category of categories) {
            e = document.createElement("div");
            setCellState(data, e, category);
            r.appendChild(e);
        }
    })

    game_table.appendChild(r);

}

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

function reset() {
    localStorage.clear();
    fetch('/reset').then((res) => res.json()).then((data) => setPlaceholder(input, data["num_guesses"]));
}

