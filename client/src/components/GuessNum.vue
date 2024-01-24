<template>
    <div>
        <h2>Number guessing game</h2>

        <p>
            We have selected a random number between 1 and 100. See if you can guess it
            in 10 turns or fewer. We'll tell you if your guess was too high or too low.
        </p>

        <div class="form">
            <label for="guessField">Enter a guess: </label>
            <input type="number" min="1" max="100" required v-model="userGuess" @input="updateGuess" class="guessField" />
            <button @click="checkGuess" :disabled="guessFieldDisabled" class="guessButton">Submit</button>
        </div>

        <div class="resultParas">
            <p v-if="guesses.length > 0">Previous guesses: {{ guesses.join(' ') }}</p>
            <p class="lastResult" :style="{ backgroundColor: lastResultColor }">{{ lastResult }}</p>
            <p>{{ lowOrHi }}</p>
        </div>

        <button v-if="gameOver" @click="resetGame" class="resetButton">Start new game</button>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            randomNumber: Math.floor(Math.random() * 100) + 1,
            userGuess: '',
            guesses: [],
            lastResult: '',
            lastResultColor: 'white',
            lowOrHi: '',
            guessCount: 1,
            guessFieldDisabled: false,
            gameOver: false,
        };
    },
    methods: {
        updateGuess() {
            // Optional: Add validation if needed
        },
        checkGuess() {
            const userGuess = Number(this.userGuess);

            if (this.guessCount === 1) {
                this.guesses.push('Previous guesses:');
            }

            this.guesses.push(userGuess);

            if (userGuess === this.randomNumber) {
                this.lastResult = 'Congratulations! You got it right!';
                this.lastResultColor = 'green';
                this.lowOrHi = '';
                this.setGameOver();
            } else if (this.guessCount === 10) {
                this.lastResult = '!!!GAME OVER!!!';
                this.lowOrHi = '';
                this.setGameOver();
            } else {
                this.lastResult = 'Wrong!';
                this.lastResultColor = 'red';
                if (userGuess < this.randomNumber) {
                    this.lowOrHi = 'Last guess was too low!';
                } else if (userGuess > this.randomNumber) {
                    this.lowOrHi = 'Last guess was too high!';
                }
            }

            this.guessCount++;
            this.userGuess = '';
        },
        setGameOver() {
            this.guessFieldDisabled = true;
            this.gameOver = true;
        },
        resetGame() {
            this.guessCount = 1;
            this.guesses = [];
            this.lastResult = '';
            this.lastResultColor = 'white';
            this.lowOrHi = '';
            this.guessFieldDisabled = false;
            this.gameOver = false;
            this.userGuess = '';
            this.randomNumber = Math.floor(Math.random() * 100) + 1;
        },
    },
};
</script>
<style scoped>
.guessField {
    width: 140px;
    height: 25px;
    padding: 5px;
    margin-right: 10px;
}

.guessButton {
    width: 100px;
    height: 30px;
    background-color: #4caf50;
    color: white;
    border: none;
    cursor: pointer;
    font-size: 16px;
}

.guessButton:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.resetButton {
    width: 120px;
    height: 30px;
    background-color: #2196f3;
    color: white;
    border: none;
    cursor: pointer;
    font-size: 16px;
}
</style>
