<template>
  <el-form :model="loginData" ref="loginForm" class="login-form">
    <el-form-item prop="username">
      <el-input v-model="loginData.username" placeholder="Username" />
    </el-form-item>
    <el-form-item prop="password">
      <el-input v-model="loginData.password" type="password" placeholder="Password" show-password />
    </el-form-item>
    <el-form-item class="login-button">
      <el-button type="primary" @click="submitLogin" :loading="loading">Login</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    return {
      loginData: {
        username: '',
        password: '',
      },
      loading: false,
    };
  },
  methods: {
    async submitLogin() {
      try {
        this.loading = true;
        await this.$refs.loginForm.validate();
        const response = await this.$store.dispatch('login', this.loginData);
        if (response && response.success) {
          this.$router.push('/index');
        } else {
          this.$message.error('Check username or password');
        }
      } catch (error) {
        this.$message.warning('An error occurred.');
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped></style>
