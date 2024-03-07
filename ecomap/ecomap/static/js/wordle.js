class Wordle {
    constructor(answer) {
        /*stores the answer in upper case as well as the row and column
        index for the next letter to be input on
        Then it sets up the grid by the number of letters in the answer*/
        this.answer = answer.toUpperCase();
        this.row_index = 0;
        this.column_index = 0;
        this.setGrid();
    }

    setGrid() {
        //create six rows of empty boxes each with the length of the answer
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
            //get the users guess input
            var guess_string = ""
            var rows = document.querySelectorAll(`.row-${this.row_index}`);
            for (let i=0; i<rows.length; i++) {
                guess_string += rows[i].textContent;
            }
            var characters = this.answer.split("");
            var remaining_characters = characters;
            var guess = guess_string.split("")
            //check every letter in the users input and compare with the answer and colour respectively
            for (let i = 0; i < characters.length; i++) {
                //if the characters are in the same position colour green
                if (characters[i] == guess[i]) {
                    remaining_characters[i] = "-";
                    rows[i].style.backgroundColor = "#2ADC6B";
                    colourCharacter(guess[i], "#2ADC6B");
                //if the character is in a different position and not been coloured yet, colour this one
                } else if (remaining_characters.includes(guess[i])) {
                    let index = remaining_characters.indexOf(guess[i]);
                    remaining_characters[index] = "-";
                    rows[i].style.backgroundColor = "#F3D510";
                    colourCharacter(guess[i], "#F3D510");
                //if the character is not in the word, colour grey
                } else {
                    rows[i].style.backgroundColor = "#777777";
                    if (!this.answer.includes(guess[i])) {
                        colourCharacter(guess[i], "#777777");
                    }
                }
                rows[i].style.color = "white";
                //disableKey(guess[i]);
            }
            //increment the row and start the column back at 0
            this.row_index += 1;
            this.column_index = 0;
            this.checkWin(guess_string);
        }
    }

    backspace() {
        //check if there are any characters, if so then remove the last one
        if (this.column_index > 0) {
            var rows = document.querySelectorAll(`.row-${this.row_index}`);
            this.column_index -= 1;
            rows[this.column_index].textContent = "";
        }
    }

    addLetter(character) {
        //add letter to the screen if there is enough space on the row
        if (this.column_index < this.answer.length) {
            var rows = document.querySelectorAll(`.row-${this.row_index}`);
            rows[this.column_index].textContent = character;
            this.column_index += 1;
        }
    }

    checkWin(guess) {
        //check if the guess and answer are the same
        if (guess.toUpperCase() == this.answer.toUpperCase()) {
            this.endGame("green")
        } else if (this.row_index > 5) {
            this.endGame("red");
        } else {
            return;
        }

    }

    endGame(colour) {
        //remove the keydown event listener
        document.onkeydown = null;
        //remove keys from webpage and outputs the score
        document.querySelector(".keyboard").innerHTML = "";
        var score = 0;
        var message = "Answer: " + this.answer;
        if (colour.toLowerCase() != "red") {
            message = "Correct!"
            score = Math.floor(100 * this.answer.length / this.row_index);
        }

        //display the score and colour green if win and red if loss
        document.querySelector(".main").innerHTML += `<div class="level-end">${message}
            <div id="level-completed">Score: ${score}pts</div>
        </div>`;
        document.querySelector(".level-end").style.backgroundColor = colour;
        sendScore(score)
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

function colourCharacter(character, colour) {
    //colours the key on the keyboard on screen
    character = character.toUpperCase();
    var keysArray = document.querySelectorAll(".key");
    for (let i=0; i< keysArray.length; i++) {
         if (keysArray[i].outerText == character) {
            keysArray[i].style.backgroundColor = colour;
            return;
         }
    }
}

//receive the answer from django
const data = document.currentScript.dataset;
const answer = data.answer;
wordle = new Wordle(answer)

//allow the user to enter keys on keyboard instead of having to click on the screen
function keyboardType(event) {
    if (event.keyCode >= 65 && event.keyCode <= 90) {
        //character key pressed
        wordle.addLetter(event.key.toUpperCase());
    } else if (event.keyCode == 8) {
        //backspace key pressed
        wordle.backspace()
    } else if (event.keyCode == 13) {
        //enter key pressed
        wordle.wordle_guess()
    }
}
document.onkeydown = keyboardType;

