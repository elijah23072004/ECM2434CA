class Hangman {
    /*hangman class to start a game of hangman
    requires the answer to the hangman to start*/
    constructor(answer) {
        /*stores the answer to hangman, the number of wrong guesses,
        the remaining letters not input by user, the guesses made by the user
        (may remove this or add feature to show the guesses)*/
        this.answer = answer;
        this.wrongGuesses = 0;
        this.remainingLetters = this.getUniqueLetters();
        this.guesses = [];
        this.setHiddenAnswer();
    }

    setHiddenAnswer() {
        /*this sets the text on screen to show the underscores for missing letters*/
        var charArray = this.answer.split("");
        var hiddenString = "";
        var character;
        /*checks if the user has already entered each letter
        if yes: display the letter
        else: display an underscore
        uses thinspace character for easier viewing*/
        for (let i=0; i< charArray.length; i++) {
            character = charArray[i];
            if (character == " ") {
                hiddenString += "   ";
            } else if (this.guesses.includes(character) || character.toLowerCase() == character.toUpperCase() || this.guesses.includes(removeWhitespace(this.answer))) {
                hiddenString += character;
            } else {
                hiddenString += "_";
            }
            hiddenString += " ";
        }
        document.querySelector(".hiddenAnswer").textContent = hiddenString;
    }


    getUniqueLetters() {
        //gets the unique letters in the answer
        //make array, turn into a set then back to array
        var answer = removeWhitespace(this.answer)
        var letters = answer.split("")
        letters = new Set(letters);
        return [...letters]
    }

    checkGuess(guess) {
        //first check if it has already been guessed, if so do nothing
        guess = guess.toUpperCase();
        if (this.guesses.includes(removeWhitespace(guess))) {
            return false;
        }

        //if the user just input a single letter go to guessLetter
        if (removeWhitespace(guess).length == 1) {
            return this.guessLetter(removeWhitespace(guess))
        }

        //add this guess to the guesses for the game
        this.guesses.push(removeWhitespace(guess));
        //if the user input the full answer, they win
        if (removeWhitespace(guess) == removeWhitespace(this.answer)) {
            this.setHiddenAnswer();
            win();
            return true;
        } else if (removePunctuation(this.answer.toUpperCase()).split(" ").includes(removePunctuation(guess.toUpperCase()))) {
            //check if the word is one of the words for the hangman game,
            //if so add every letter in the word to the guesses
            var word = removeWhitespace(guess);
            for(let i=0; i < word.length; i++) {
                this.guessLetter(word[i]);
            }
            this.checkWin()
            return true;
        }
        this.setHangmanImage()
        return false;
    }

    guessLetter(letter) {
        //add the letter to guesses
        var letter = letter.toUpperCase();
        this.guesses.push(letter);
        disableKey(letter);
        const index = this.remainingLetters.indexOf(letter);
        //if the letter is missing, add it and check for a win
        if (index > -1) {
            this.remainingLetters.splice(index, 1);
            this.setHiddenAnswer();
            this.checkWin();
            return true;
        }
        //if the user has not already guessed this letter, the guess is wrong
        if (!this.getUniqueLetters().includes(letter)) {
            this.setHangmanImage()
            return false
        }
        return true;
    }

    setHangmanImage() {
        //increases the number of wrong guesses and sets the hangman image accordingly
        this.wrongGuesses += 1;
        var imageLink = `../static/images/hangman_images/hangman${this.wrongGuesses}.png`
        document.querySelector(".hangman-image").src = imageLink;
        this.setWrongGuesses()
        if (this.wrongGuesses >= 7) {
            fail(this.answer, this.remainingLetters, this.wrongGuesses);
        }
    }

    checkWin() {
        //checks if all letters have been guessed, if so the user wins
        if (this.remainingLetters.length <= 0) {
            win(this.answer, this.wrongGuesses);
        }
    }

    setWrongGuesses() {
        //sets the wrong guesses message to the number of wrong guesses
        document.querySelector(".guesses-count").textContent = `Wrong Guesses: ${this.wrongGuesses}/7`;
    }
}

function searchFunction(e) {
    //if the user hits the enter key in the input bar, check the guess (what is in the input bar)
    if (e.keyCode == 13) {
        var guess = document.querySelector(".inputGuess").value;
        guessNoWhite = removeWhitespace(guess);
        if (guessNoWhite) {
            if (guessNoWhite.length == 1) {
                disableKey(guessNoWhite);
            }
            hangman.checkGuess(guess);
        document.querySelector(".inputGuess").value = "";
        }
    }
}

function disableKey(character) {
    //disable the key so it cannot be clicked and is greyed out
    character = character.toUpperCase();
    var keysArray = document.querySelectorAll(".key");
    for (let i=0; i< keysArray.length; i++) {
         if (keysArray[i].outerText == character) {
            keysArray[i].classList.remove("key");
            keysArray[i].classList.add("keyPressed");
            return;
         }
    }
}

function clickKey(e) {
    //if the user clicks a key, get the letter clicked and check the guess for this letter
    var keyPressed = e.srcElement;
    if (keyPressed.classList.contains("keyPressed")) {
        return;
    }
    var character = keyPressed.outerText;
    keyPressed.classList.remove("key");
    keyPressed.classList.add("keyPressed");
    keyPressed.removeEventListener("click", clickKey);
    hangman.checkGuess(character);
}

function removeWhitespace(string) {
    //remove whitespace and punctuation from a string
    string = string.replace(/\s+/g, '');
    return removePunctuation(string);
}

function removePunctuation(string) {
    //remove the punctuation from a string
    return string.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()\'\"]/g, "");
}


function fail(answer, remainingLetters, wrong_guesses) {
    //display the hidden word with letters not picked in red as the user has lost
    var html_code = "";
    console.log(answer);
    for (let i=0; i<answer.length; i++) {
        if (remainingLetters.includes(answer[i])) {
            html_code += `<font color="red" class="underline">${answer[i]}</font>\n`;
        } else if (answer[i] == " ") {
            html_code += "   ";
        } else {
            html_code += `<font color="black">${answer[i]}</font>\n`;
        }
    }
    document.querySelector(".hiddenAnswer").innerHTML = html_code;
    endGame("red", answer, wrong_guesses);
}

function win(answer, wrong_guesses) {
    //winning screen as the user has won
    endGame("green", answer, wrong_guesses);
    document.querySelector(".hiddenAnswer").style.color = "green";

}

function endGame(colour, answer, wrong_guesses) {
    //remove the input box
    document.querySelector(".hangman-input-bar").innerHTML = "";
    //remove keys from webpage and outputs the score
    document.querySelector(".keyboard").innerHTML = "";
    var score = 0;
    var message = "Answer: " + answer;
    if (colour.toLowerCase() != "red") {
        message = "Correct!"
        score = Math.floor(100 * answer.length / (wrong_guesses+1));
    }

    //display the score and colour green if win and red if loss
    document.querySelector(".main").innerHTML += `<div class="level-end">${message}
        <div id="level-completed">Score: ${score}pts</div>
    </div>`;
    document.querySelector(".level-end").style.backgroundColor = colour;

}

//input the answer here and start the game of hangman
const data = document.currentScript.dataset;
const answer = data.answer;
const hangman = new Hangman(answer.toUpperCase());