<template>
    <el-scrollbar height="98vh">
        <div class="container">
            <el-menu :default-active="0" class="el-menu-demo" background-color="#545c64" text-color="#fff"
                active-text-color="#ffd04b" mode="horizontal" :ellipsis="false">
                <el-menu-item index="0">首页</el-menu-item>
                <el-menu-item index="1">树洞</el-menu-item>
                <div class="flex-grow" />
                <el-menu-item index="2">个人中心</el-menu-item>
            </el-menu>

            <br>
            <el-text tag="mark">每个人都需要一个树洞，存放那些不可轻易示人的秘密、引而不发的情绪、难以启齿的柔弱</el-text>
            <br>
            <el-divider />
            <el-row>
                <el-col v-if="activities.length === 0" :span="24">
                    <el-empty description="暂无发贴信息" />
                </el-col>
                <el-col v-else v-for="activity in activities" :key="activity._id">
                    <!-- 左边区域：用户名和事件 -->
                    <div class="left-section">
                        <el-text class="mx-1">{{ activity.author }} - {{ activity.time }}</el-text>
                    </div>
                    <!-- 右边区域：描述 -->
                    <div class="right-section">
                        <el-text class="mx-1">{{ activity.description }}</el-text>
                    </div>
                    <!-- 右下角区域：赞和踩 -->
                    <div class="bottom-section">
                        <el-divider />
                        <el-button icon="el-icon-thumb-up" size="mini" @click="likeAction(activity._id)">赞</el-button>
                        <el-button icon="el-icon-thumb-down" size="mini" @click="dislikeAction(activity._id)">踩</el-button>
                    </div>

                    <el-divider />
                </el-col>
                <el-pagination layout="prev, pager, next" :total="activities.length" />
                <el-divider />
            </el-row>

            <el-form :model="activity" ref="activityForm" label-width="auto">
                <el-form-item label="称呼:" prop="author">
                    <el-input v-model="activity.author" size="small" style="width: 20%;" clearable></el-input>
                </el-form-item>
                <el-form-item label="邮箱:" prop="email">
                    <el-input v-model="activity.email" size="small" style="width: 20%;" clearable></el-input>
                </el-form-item>
                <el-input v-model="activity.description" :autosize="{ minRows: 2, maxRows: 4 }" type="textarea" />
                <p />
                <el-form-item>
                    <el-button @click="submitActivity" :loading="submitting">添加</el-button>
                </el-form-item>
            </el-form>
        </div>
    </el-scrollbar>
</template>
  
<script>
export default {
    data() {
        return {
            activity: { author: '', email: '', description: '', time: new Date().toISOString() },
            activities: [],
            submitting: false,
        };
    },
    methods: {
        async fetchActivities() {
            this.activities = (await this.$axios.get('/post')).data;
        },
        async submitActivity() {
            if (this.activity.description.length === 0) {
                return;
            }
            try {
                this.submitting = true;
                await this.$axios.post('/post', this.activity);
                this.fetchActivities();
                this.clearForm();
            } finally {
                this.submitting = false;
            }
        },
        clearForm() {
            this.activity.author = '';
            this.activity.description = '';
        },
    },
    mounted() {
        this.fetchActivities();
    },
};
</script>
  
<style>
.container {
    width: 50% !important;
    margin: 0 auto;
}

.flex-grow {
    flex-grow: 1;
}

span {
    color: #333;
}

.mx-1 {
    margin-right: 8px;
}
</style>
  