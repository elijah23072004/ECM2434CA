class Wordle {
    constructor(answer) {
        /*stores the answer to hangman, the number of wrong guesses,
        the remaining letters not input by user, the guesses made by the user
        (may remove this or add feature to show the guesses)*/
        this.answer = answer.toUpperCase();
        this.row_index = 0;
        this.column_index = 0;
        this.setGrid();
    }

    setGrid() {
        document.querySelector(".wordle-table").style.gridTemplateColumns  = `repeat(${this.answer.length}, 1fr)`;
        for (let i = 0; i < 6; i++) {
            for (let j = 0; j < this.answer.length; j++) {
                document.querySelector(".wordle-table").innerHTML += `<div class="row-${i} column-${j} square"></div>`;
            }
        }
    }

    wordle_guess() {
        //check all letters have been used
        if (this.column_index == this.answer.length) {
            var guess_string = ""
            var rows = document.querySelectorAll(`.row-${this.row_index}`);
            for (let i=0; i<rows.length; i++) {
                guess_string += rows[i].textContent;
            }
            var characters = this.answer.split("");
            var guess = guess_string.split("")
            for (let i = 0; i < characters.length; i++) {
                if (characters[i] == guess[i]) {
                    rows[i].style.backgroundColor = "#2ADC6B";
                } else if (characters.includes(guess[i])) {
                    rows[i].style.backgroundColor = "#F3D510";
                } else {
                    rows[i].style.backgroundColor = "#777777";
                }
                rows[i].style.color = "white";
                //disableKey(guess[i]);
            }
            this.checkWin(guess_string);
            this.row_index += 1;
            this.column_index = 0;
        }
    }

    backspace() {
        if (this.column_index > 0) {
            var rows = document.querySelectorAll(`.row-${this.row_index}`);
            this.column_index -= 1;
            rows[this.column_index].textContent = "";
        }
    }

    addLetter(character) {
        if (this.column_index < this.answer.length) {
            var rows = document.querySelectorAll(`.row-${this.row_index}`);
            rows[this.column_index].textContent = character;
            this.column_index += 1;
        }
    }

    checkWin(guess) {
        if (guess.toUpperCase() == this.answer.toUpperCase()) {
            this.endGame("green")
        } else if (this.row_index > 5) {
            this.endGame("red");
        } else {
            return;
        }

    }

    endGame(colour) {
        //remove keys from webpage
        document.querySelector(".keyboard").innerHTML = "";
        var score = 0;
        if (colour.toLowerCase() != "red") {
            score = 100 * this.answer.length / this.row_index;
        }

        document.querySelector(".main").innerHTML += `<div class="level-end">Level Completed
            <div id="level-completed">Score: 100pts</div>
        </div>`;
        document.querySelector(".level-end").backgroundColor = colour;
    }
}


function clickKey(e) {
    //if the user clicks a key, get the letter clicked and check the guess for this letter
    var keyPressed = e.srcElement;
    var character = keyPressed.outerText;
    if (character == "Enter") {
        wordle.wordle_guess();
    } else if (character == "<-") {
        wordle.backspace();
    } else {
        wordle.addLetter(character);
    }
}

function disableKey(character) {
    //disable the key so it cannot be clicked and is greyed out
    character = character.toUpperCase();
    var keysArray = document.querySelectorAll(".key");
    for (let i=0; i< keysArray.length; i++) {
         if (keysArray[i].outerText == character) {
            if (keysArray[i].classList.contains("key")) {
                keysArray[i].classList.remove("key");
                keysArray[i].classList.add("keyPressed");
            }
            return;
         }
    }
}

const data = document.currentScript.dataset;
const answer = data.answer;
wordle = new Wordle(answer)