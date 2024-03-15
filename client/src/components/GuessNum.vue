<template>
    <div>
        <div class="profile-container">
            <div class="profile-description" style="flex: 1;">
                <div>
                    <p class="profile-title" style="font-size: 20px; font-weight: bold; margin-bottom: 10px;">
                        Welcome！</p>
                    <p style="font-size: 16px;">欢迎来到这个有趣的 JavaScript 教程游戏！</p>
                    <p style="font-size: 16px;">看看你能否在 10 圈内猜中它，我们会告诉你你的猜测是否太高或太低。享受刺激，体验 JavaScript
                        的魔力吧！😄🎉
                    </p>
                    <p style="font-size: 16px;">这个游戏的目标是在最少的猜测次数内猜到正确的数字。你可以通过输入数字并点击提交按钮来进行猜测，系统会告诉你你的猜测是否正确，或者是否太高或太低。
                        加油吧！💪🔥
                    </p>
                </div>
            </div>
            <img src="../assets/js.png" style="margin-right: 20px;">
        </div>

        <div class="form">
            <br>
            <el-form :model="formData" :rules="formRules" ref="form">
                <el-form-item prop="userGuess">
                    <el-input v-model.number="formData.userGuess" min="1" max="100" required clearable></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button @click="checkGuess" :disabled="guessFieldDisabled" type="primary">提交</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div class="resultParas">
            <p v-if="guesses.length > 0">上次猜测: {{ guesses.join(' ') }}</p>
            <p class="lastResult" :style="{ backgroundColor: lastResultColor }">{{ lastResult }}</p>
            <p>{{ lowOrHi }}</p>
        </div>

        <el-button v-if="gameOver" @click="resetGame" type="primary">开始新游戏 😊</el-button>
    </div>
</template>


<script>
export default {
    data() {
        return {
            randomNumber: Math.floor(Math.random() * 100) + 1,
            formData: {
                userGuess: ''
            },
            formRules: {
                userGuess: [
                    { required: true, message: '输入你的猜测', trigger: 'blur' },
                    { type: 'number', message: '输入有效号码', trigger: 'blur' },
                    { min: 1, max: 100, message: '数字必须介于 1 到 100 之间', trigger: 'blur' }
                ]
            },
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
        checkGuess() {
            const userGuess = Number(this.formData.userGuess);

            if (this.guessCount === 1) {
                this.guesses.push('之前的猜测:');
            }

            this.guesses.push(userGuess);

            if (userGuess === this.randomNumber) {
                this.lastResult = '恭喜！ 你做对了！';
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
                    this.lowOrHi = '最后的猜测太低了！';
                } else if (userGuess > this.randomNumber) {
                    this.lowOrHi = '最后的猜测太高了！';
                }
            }

            this.guessCount++;
            this.formData.userGuess = '';
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
            this.formData.userGuess = '';
            this.randomNumber = Math.floor(Math.random() * 100) + 1;
        },
    },
};
</script>

<style scoped>
.profile-container {
    display: flex;
    align-items: center;
}

.profile-description {
    flex: 1;
    margin-right: 20px;
}

.resultParas p {
    margin: 5px 0;
}

.lastResult {
    padding: 10px;
    border-radius: 5px;
}

.form {
    margin-bottom: 20px;
}
</style>