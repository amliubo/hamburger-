<template>
  <el-scrollbar height="100vh">
    <div class="header">
      <el-menu :default-active="activeIndex" mode="horizontal" @select="handleSelect">
        <el-menu-item>
          <img style="width: 220px" src="@/assets/logo.png" />
        </el-menu-item>
        <div class="flex-grow" />
        <el-menu-item index="0">😎 关于</el-menu-item>
        <el-menu-item index="1">✌️ 树洞</el-menu-item>
        <el-menu-item index="2">💕 记录</el-menu-item>
        <el-menu-item index="3">👀 数据</el-menu-item>
        <el-menu-item index="4">📒 笔记</el-menu-item>
        <el-menu-item index="5">🎮 游戏</el-menu-item>

        <!-- <el-sub-menu index="5">
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
</el-sub-menu> -->

      </el-menu>
    </div>
    <div class="container">
      <br />
      <div v-show="activeIndex === '0'">
        <About />
        <Footer />
      </div>
      <div v-show="activeIndex === '1'">
        <TreeHole />
      </div>
      <div v-show="activeIndex === '2'">
        <Record />
      </div>
      <div v-show="activeIndex === '3'">
        <Data />
      </div>
      <div v-show="activeIndex === '4'">
        <Notes />
      </div>
      <div v-show="activeIndex === '5'">
        <NumberGuessingGame />
      </div>
    </div>
  </el-scrollbar>
</template>

<script>
import About from '@/components/About.vue';
import TreeHole from '@/components/TreeHole.vue';
import Record from '@/components/Record.vue';
import Data from '@/components/Data.vue';
import NumberGuessingGame from '@/components/GuessNum.vue';
import Footer from '@/components/Footer.vue';
import Notes from '@/components/Notes.vue';

export default {
  data() {
    return {
      activeIndex: '0',
    };
  },
  methods: {
    handleSelect(index) {
      this.activeIndex = index;
    }
  },
  components: { About, TreeHole, Record, Data, Footer, Notes, NumberGuessingGame }
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
    width: 60% !important;
  }
}
</style>
