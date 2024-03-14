<template>
    <div>
        <input type="password" v-model="password" placeholder="who are you?">
        <div v-if="isAuthenticated">
            <h2>您已成功登录，以下是内容：</h2>
            <p>这里是您需要登录后才能看到的内容。</p>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            password: '',
            correctPassword: 'iamliu',
            isAuthenticated: false
        };
    },
    watch: {
        password(newValue) {
            this.isAuthenticated = newValue === this.correctPassword;
        }
    }
};
</script>