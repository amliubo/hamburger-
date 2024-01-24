<template>
    <el-scrollbar height="100vh">
        <p />
        <br>
        <div class="header">
            <el-menu :default-active="activeIndex" class="el-menu-demo" background-color="#333333" text-color="#fff"
                active-text-color="#ffd04b" mode="horizontal" :ellipsis="false" @select="handleSelect">
                <el-menu-item index="1" style="font-size: 16px;">树洞</el-menu-item>
                <el-menu-item index="2" style="font-size: 16px;">猜数字</el-menu-item>
                <div class="flex-grow" />
                <el-menu-item index="9" style="font-size: 16px;">个人中心</el-menu-item>
            </el-menu>
        </div>
        <div class="container">
            <br />
            <div v-show="activeIndex === '1'">
                <el-text tag="b" size="large" style="font-style: italic;">##
                    每个人都需要一个树洞，存放那些不可轻易示人的秘密、引而不发的情绪、难以启齿的柔弱。</el-text>
                <br />
                <el-divider />
                <el-row v-if="activities.length === 0">
                    <el-empty description="暂无发贴信息" />
                </el-row>
                <el-row v-else v-for="activity in activities" :key="activity._id">
                    <el-col :span="24">
                        <div class="activity-container">
                            <div class="left-section">
                                <div class="name">
                                    <el-text :style="{ fontWeight: 'bold' }">{{ activity.author }}</el-text>
                                </div>
                                <div class="time">
                                    <el-text :style="{ fontSize: '12px', color: '#888' }">@{{ formatTime(activity.time)
                                    }}</el-text>
                                </div>
                            </div>
                            <div class="right-section">
                                <el-text style="font-size: 15px;">{{ activity.description }}</el-text>
                                <p />
                                <div class="action-buttons flex justify-space-between flex-wrap gap-2">
                                    <el-link :underline="false" size="small" type="danger" :style="{ fontSize: '12px' }"
                                        @click="handleAction(activity._id, 'like')">
                                        oo👍[ {{ activity.like }} ]
                                    </el-link>
                                    <el-link :underline="false" size="small" type="success" :style="{ fontSize: '12px' }"
                                        @click="handleAction(activity._id, 'dislike')">
                                        xx👎[ {{ activity.dislike }} ]
                                    </el-link>
                                    <el-link :underline="false" size="small" type="info" :style="{ fontSize: '12px' }"
                                        @click="toggleContent(activity._id)">
                                        吐槽 [ {{ activity.comment.length }} ]
                                    </el-link>
                                </div>
                                <el-collapse v-show="showContent === activity._id" class="comment-collapse">
                                    <p />
                                    <el-link :underline="false" size="small" type="info"
                                        :style="{ fontSize: '12px', marginLeft: 'auto' }" @click="toggleContent">
                                        <el-icon>
                                            <Top />
                                        </el-icon>收起吐槽
                                    </el-link>
                                    <div v-for="(com, index) in activity.comment" :key="com._id" class="comment-container">
                                        <div class="comment-info">
                                            <div class="name-and-time">
                                                <div class="name">
                                                    <el-text :style="{ fontWeight: 'bold' }">{{ com.author }}</el-text>
                                                </div>
                                                <span>&nbsp;</span>
                                                <div class="time">
                                                    <el-text style="font-size: 12px; color: '#909399">{{ com.address
                                                    }}</el-text>
                                                </div>
                                                <p :style="{ fontSize: '11px', color: '#909399', marginLeft: 'auto' }">#{{
                                                    index + 1 }}楼</p>
                                            </div>
                                        </div>
                                        <el-text style="font-size: 15px;">{{ com.description }}</el-text>
                                        <p />
                                        <div class="action-buttons flex justify-space-between flex-wrap gap-2">
                                            <el-text :style="{ fontSize: '12px', color: '#888' }">@{{
                                                formatTime(com.time) }}</el-text>
                                            <el-link :underline="false" size="small" type="danger"
                                                :style="{ fontSize: '12px' }"
                                                @click="handleAction(activity._id, 'like', com.comment_id)">
                                                oo [ {{ com.like }} ]
                                            </el-link>
                                            <el-link :underline="false" size="small" type="success"
                                                :style="{ fontSize: '12px' }"
                                                @click="handleAction(activity._id, 'dislike', com.comment_id)">
                                                xx [ {{ com.dislike }} ]
                                            </el-link>
                                            <el-link :underline="false" size="small" type="info"
                                                :style="{ fontSize: '12px' }">
                                                举报
                                            </el-link>
                                        </div>
                                    </div>
                                    <div v-if="!$store.getters['isAuthenticated']">
                                        <alert :message="message" :alertClass="msgClass" :key="msgTime" v-if="commentMsg" />
                                        <el-form :model="comact" ref="comactForm" label-width="auto">
                                            <el-input v-model="comact.description" maxlength="199" show-word-limit
                                                :autosize="{ minRows: 2, maxRows: 2 }" type="textarea" />
                                            <el-button @click="submitActivity(activity._id)" :loading="submitting"
                                                style="width: 100%; background-color: #f7f9fc; height: 24px;">发布</el-button>
                                        </el-form>
                                    </div>
                                    <div v-else>
                                        <el-button @click="handleSelect('9')" :loading="submitting"
                                            style="width: 100%; background-color: #333333; font-weight: bold; color: #fff;">
                                            想吐槽？点击登录
                                        </el-button>
                                    </div>
                                </el-collapse>
                            </div>
                        </div>
                        <el-divider />
                    </el-col>
                </el-row>
                <alert :message="message" :alertClass="msgClass" :key="msgTime" v-if="releaseMsg" />
                <el-form :model="activity" ref="activityForm" label-width="auto">
                    <el-form-item label="昵称:" prop="author">
                        <el-input v-model="activity.author" size="small" style="width: 40%;" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="邮箱:" prop="email" :rules="emailRules">
                        <el-input v-model="activity.email" size="small" style="width: 40%;" clearable></el-input>
                    </el-form-item>
                    <el-input v-model="activity.description" maxlength="1000" show-word-limit
                        :autosize="{ minRows: 3, maxRows: 6 }" type="textarea" />
                    <p />
                    <el-form-item>
                        <el-button @click="submitActivity()" :loading="submitting"
                            style="width: 100%; background-color: #f7f9fc;">点击发布</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <div v-show="activeIndex === '2'">
                <div style="height: 450px;">
                    <NumberGuessingGame />
                </div>
            </div>
            <div v-show="activeIndex === '9'">
                <el-text size="large" style="font-style: italic;">## 个人中心</el-text>
                <el-divider />
                <el-skeleton />
                <br />
                <el-skeleton style="--el-skeleton-circle-size: 100px">
                    <template #template>
                        <el-skeleton-item variant="circle" />
                    </template>
                </el-skeleton>
            </div>
            <Footer />
        </div>
    </el-scrollbar>
</template>  

<script>
import Alert from '@/components/Alert.vue';
import Footer from '@/components/Footer.vue';
import NumberGuessingGame from '@/components/GuessNum.vue'
import { v4 as uuidv4 } from 'uuid';

export default {
    data() {
        return {
            activeIndex: '1',
            activity: { author: '', email: '', description: '', time: new Date().toISOString(), 'like': 0, 'dislike': 0, 'comment': [] },
            // 吐槽
            comact: { author: '大帅逼', email: '1105729770@qq.com', description: '', time: new Date().toISOString(), like: 0, dislike: 0 },
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
    components: { alert: Alert, Footer, NumberGuessingGame },
    methods: {
        handleSelect(index) {
            this.activeIndex = index;
        },
        toggleContent(activityId) {
            this.showContent = this.showContent === activityId ? false : activityId;
        },
        formatTime(time) {
            const now = new Date();
            const activityTime = new Date(time);
            const timeDiff = now - activityTime;
            const seconds = Math.floor(timeDiff / 1000);
            const minutes = Math.floor(seconds / 60);
            const hours = Math.floor(minutes / 60);
            const days = Math.floor(hours / 24);

            if (days > 0) {
                return `${days}天前`;
            } else if (hours > 0) {
                return `${hours}小时前`;
            } else if (minutes > 0) {
                return `${minutes}分钟前`;
            } else {
                return '刚刚';
            }
        },
        async fetchActivities() {
            this.activities = (await this.$axios.get('/post')).data;
        },
        async submitActivity(activity_id) {
            if (activity_id) {
                // this.$refs.comactForm.validate();
                if (this.comact.description.trim()) {
                    this.submitting = true;
                    try {
                        this.comact.comment_id = uuidv4();

                        const response = await fetch('https://ipinfo.io/json');
                        const data = await response.json();
                        this.comact.address = data.city;
                        this.comact.activity_id = activity_id;
                        await this.$axios.post('/post', this.comact);
                        this.fetchActivities();
                        this.clearForm();
                        this.message = '吐槽成功！';
                        this.msgClass = 'alert alert-success';
                        this.commentMsg = true;
                        this.msgTime = Date.now();
                    } finally {
                        this.submitting = false;
                    }
                } else {
                    this.message = '填写吐槽信息！';
                    this.msgClass = 'alert alert-warning'
                    this.commentMsg = true;
                    this.msgTime = Date.now();
                }
            } else {
                this.$refs.activityForm.validate();
                if (this.activity.author.trim() && this.activity.email.trim() && this.activity.description.trim()) {
                    try {
                        this.submitting = true;
                        delete this.activity.activity_id;
                        await this.$axios.post('/post', this.activity);
                        this.fetchActivities();
                        this.clearForm();
                        this.message = '发布成功！';
                        this.msgClass = 'alert alert-success';
                        this.releaseMsg = true;
                        this.msgTime = Date.now();
                    } finally {
                        this.submitting = false;
                    }
                } else {
                    this.message = '填写所有信息！';
                    this.msgClass = 'alert alert-warning'
                    this.releaseMsg = true;
                    this.msgTime = Date.now();
                }
            }
        },
        async handleAction(_id, actionType, comment_id) {
            await this.$axios.post(`/${actionType}`, { _id, comment_id });
            this.fetchActivities();
        },
        clearForm() {
            this.comact.description = '';
            this.activity.description = '';
        },
    },
    mounted() {
        this.fetchActivities();
    },
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
    border: 1px solid #ddd;
    margin-bottom: 10px;
}

.flex-grow {
    flex-grow: 1;
}

.right-section {
    width: 80%;
    margin-bottom: 5px;
}

.activity-container {
    display: flex;
    justify-content: space-between;
    padding: 10px;
}

.el-collapse {
    display: flex;
    flex-direction: column;
}

.action-buttons {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
}

.action-buttons el-link {
    margin-left: 10px;
}

.name-and-time {
    display: flex;
    align-items: center;
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
        width: 40% !important;
    }
}
</style>
