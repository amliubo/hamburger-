<template>
    <el-scrollbar height="100vh">
        <div class="container">
            <el-menu :default-active="'0'" class="el-menu-demo" background-color="#545c64" text-color="#fff"
                active-text-color="#ffd04b" mode="horizontal" :ellipsis="false">
                <el-menu-item index="0">树洞</el-menu-item>
                <div class="flex-grow" />
                <el-menu-item index="2">个人中心</el-menu-item>
            </el-menu>
            <br />
            <el-text tag="mark">每个人都需要一个树洞，存放那些不可轻易示人的秘密、引而不发的情绪、难以启齿的柔弱。</el-text>
            <br />
            <el-divider />

            <el-row v-if="activities.length === 0">
                <el-empty description="暂无发贴信息" />
            </el-row>
            <el-row v-else v-for="activity in activities" :key="activity._id">
                <el-col :span="24">
                    <div class="activity-container">
                        <div class="left-section">
                            <el-text class="name">{{ activity.author }}</el-text>
                            <el-text class="time">{{ activity.time }}</el-text>
                        </div>
                        <div class="right-section">
                            <el-text class="description">{{ activity.description }}</el-text>
                            <div class="action-buttons flex justify-space-between flex-wrap gap-4">
                                <el-button type="danger" text @click="handleAction(activity._id, 'like')">
                                    oo [ {{ activity.like }} ]
                                </el-button>
                                <el-button type="danger" text @click="handleAction(activity._id, 'dislike')">
                                    xx [ {{ activity.dislike }} ]
                                </el-button>
                            </div>
                        </div>
                    </div>
                    <el-divider />
                </el-col>
            </el-row>
            <alert :message="message" v-if="showMessage" />
            <el-form :model="activity" ref="activityForm" label-width="auto">
                <el-form-item label="昵称:" prop="author">
                    <el-input v-model="activity.author" size="small" style="width: 20%;" clearable></el-input>
                </el-form-item>
                <el-form-item label="邮箱:" prop="email" :rules="emailRules">
                    <el-input v-model="activity.email" size="small" style="width: 20%;" clearable></el-input>
                </el-form-item>
                <el-input v-model="activity.description" maxlength="1000" show-word-limit
                    :autosize="{ minRows: 3, maxRows: 6 }" type="textarea" />
                <p />
                <el-form-item>
                    <el-button @click="submitActivity" :loading="submitting" style="width: 100%;">点击发布</el-button>
                </el-form-item>
            </el-form>
        </div>
    </el-scrollbar>
</template>  
  
<script>
import Alert from './Alert.vue';

export default {
    data() {
        return {
            activity: { author: '', email: '', description: '', time: new Date().toISOString(), 'like': 0, 'dislike': 0 },
            activities: [],
            submitting: false,
            emailRules: [
                { type: 'email', message: '输入有效的邮箱', trigger: ['blur', 'change'] },
            ],
            message: '',
            showMessage: false,
        };
    },
    components: { alert: Alert, },
    methods: {
        async fetchActivities() {
            this.activities = (await this.$axios.get('/post')).data;
        },
        async submitActivity() {
            this.$refs.activityForm.validate();
            if (!this.$refs.activityForm.validate()) {
                this.message = '检查输入内容！';
                this.showMessage = true;
                return;
            }
            if (this.activity.author || this.activity.email || this.activity.description) {
                this.message = '发布成功！';
                this.showMessage = true;
            } else {
                this.message = '检查输入内容！';
                this.showMessage = true;
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
        async handleAction(_id, actionType) {
            try {
                await this.$axios.post(`/${actionType}`, { _id });
                this.fetchActivities();
            } catch (error) {
                this.showMessage = true;
            }
        },
        clearForm() {
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
    width: 40% !important;
    margin: 0 auto;

    display: flex;
    flex-direction: column;
    padding: 10px;
    border: 1px solid #ddd;
    margin-bottom: 10px;
}

.flex-grow {
    flex-grow: 1;
}

.left-section {
    display: flex;
    flex-direction: column;
    width: 20%;
    margin-bottom: 5px;
}

.right-section {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-bottom: 5px;
}

.name {
    font-size: 16px;
    font-weight: bold;
    color: #333;
}

.time {
    font-size: 14px;
    color: #666;
}

.description {
    font-size: 14px;
    color: #333;
}

.action-buttons {
    display: flex;
    justify-content: flex-end;
}

.action-buttons el-button {
    margin-left: 10px;
}

.activity-container {
    display: flex;
    justify-content: space-between;
    padding: 10px;
}
</style>
  