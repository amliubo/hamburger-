<template>
  <el-scrollbar height="100vh">
    <p />
    <br>
    <div class="header">
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" :ellipsis="false"
        @select="handleSelect">
        <el-menu-item>
          <img style="width: 170px" src="../assets/logo.png" />
        </el-menu-item>
        <div class="flex-grow" />
        <el-menu-item index="0">😎 关于</el-menu-item>
        <el-menu-item index="1">✌️ 树洞</el-menu-item>
        <el-menu-item index="2">😍 记录</el-menu-item>
        <el-menu-item index="3">🤣 猜数字</el-menu-item>

        <el-sub-menu index="4">
          <template #title>📖 学习</template>
          <el-menu-item index="2-1">Java Script</el-menu-item>
          <el-menu-item index="2-2">Python</el-menu-item>
          <el-menu-item index="2-3">Vue</el-menu-item>
          <el-sub-menu index="2-4">
            <template #title>item four</template>
            <el-menu-item index="2-4-1">item 1</el-menu-item>
            <el-menu-item index="2-4-2">item 2</el-menu-item>
            <el-menu-item index="2-4-3">item 3</el-menu-item>
          </el-sub-menu>
        </el-sub-menu>
      </el-menu>
    </div>
    <div class="container">
      <br />
      <div v-show="activeIndex === '0'" class="profile-container" style="display: flex; align-items: center;">
        <About />
      </div>
      <div v-show="activeIndex === '1'" style="min-height: 680px;">
        <TreeHole />
      </div>
      <div v-show="activeIndex === '2'">
        <Record />
      </div>
      <div v-show="activeIndex === '3'" style="height: 680px;">
        <div style="height: 450px;">
          <NumberGuessingGame />
        </div>
      </div>
      <Footer />
    </div>
  </el-scrollbar>
</template>

<script>
import About from '@/components/About.vue';
import TreeHole from '@/components/TreeHole.vue';
import Record from '@/components/Record.vue';
import Alert from '@/components/Alert.vue';
import Footer from '@/components/Footer.vue';
import NumberGuessingGame from '@/components/GuessNum.vue';
import LoginForm from '@/components/LoginForm.vue';
import { v4 as uuidv4 } from 'uuid';

export default {
  data() {
    return {
      activeIndex: '0',
      // 记录
      password: '',
      correctPassword: 'iamliu',
      isAuthenticated: false,
      activity: {
        author: '',
        email: '',
        description: '',
        time: new Date().toISOString(),
        'like': 0,
        'dislike': 0,
        'comment': []
      },
      // 吐槽
      comact: {
        author: '大帅逼',
        email: '1105729770@qq.com',
        description: '',
        time: new Date().toISOString(),
        like: 0,
        dislike: 0
      },
      activities: [],
      submitting: false,
      emailRules: [
        { type: 'email', message: '输入有效的邮箱', trigger: ['blur'] },
      ],
      message: '',
      msgClass: '',
      releaseMsg: false,
      commentMsg: false,
      msgTime: Date.now(),
      showContent: false,
    };
  },
  watch: {
    password(newValue) {
      this.isAuthenticated = newValue === this.correctPassword;
    }
  },
  components: { About, TreeHole, Record, alert: Alert, Footer, NumberGuessingGame, LoginForm },
  methods: {
    handleSelect(index) {
      this.activeIndex = index;
    }
  }
};
</script>

<style>
.header {
  margin-bottom: 10px;
  margin: 0 auto;
}

.container {
  width: 40%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  padding: 10px;
  /* 边框 */
  /* border: 1px solid #ddd; */
  margin-bottom: 10px;
}

.flex-grow {
  flex-grow: 1;
}

@media (max-width: 768px) {

  .header,
  .container {
    min-width: 100%;
  }
}

@media (min-width: 769px) {

  .header,
  .container {
    width: 50% !important;
  }
}
</style>
