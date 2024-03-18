<template>
    <div>
        <el-alert :title="`-- 我们已经一起度过了 ${formattedElapsedTime}啦！🎈💕`" type="error" effect="dark" :closable="false" />
        <br>
        <div v-if="!isAuthenticated" class="password-container">
            <div class="input-container">
                <input type="password" v-model="password" placeholder="🔒PIN码" class="password-input">
            </div>
            <div class="message">
                <br>
                <p><b>亲爱的访客：👋</b></p>
                <br>
                <p>非常抱歉给您添麻烦，但我希望能够向您解释一下密码保护的原因。</p>
                <p>这个密码是用来保护我们的隐私内容的，里面包含了一些我们的日常分享和个人生活的内容。</p>
                <p>如果您对内容感兴趣，但是没有获得密码，我希望您能够理解并再多等待一些时间。</p>
                <p>可能会有一天我会考虑去掉密码限制，但目前我们仍然希望保持这种私密性。</p>
                <br>
                <p>感谢您的理解和支持。🙏🌟</p>
            </div>
        </div>
        <div v-if="isAuthenticated">
            <el-button type="primary" @click="showFormDialog" size="large"><el-icon>
                    <Plus />
                </el-icon>新增事件</el-button>
            <br>
            <el-dialog v-model="formDialogVisible" title="Add" :width="awidthVariable">
                <el-form :model="activity" ref="activityForm" label-width="auto">
                    <el-form-item label="活动:" prop="action"
                        :rules="[{ required: true, message: '请输入活动', trigger: 'blur' }]">
                        <el-input v-model="activity.action" placeholder="Enter action" clearable></el-input>
                    </el-form-item>

                    <el-form-item label="描述:" prop="description">
                        <el-input v-model="activity.description" placeholder="Enter description" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="图片:" prop="description">
                        <el-upload @change="handleFileChange" ref="upload" action="/activities" list-type="picture-card"
                            :auto-upload="false" :file-list="selectedFiles" @remove="handleRemove">
                            <el-icon>
                                <Plus />
                            </el-icon>
                            <template #file="{ file }">
                                <div>
                                    <img class="el-upload-list__item-thumbnail" :src="file.url" alt="" />
                                    <span class="el-upload-list__item-actions">
                                        <span class="el-upload-list__item-preview"
                                            @click="handlePictureCardPreview(file)">
                                            <el-icon><zoom-in /></el-icon>
                                        </span>
                                        <span v-if="!disabled" class="el-upload-list__item-delete"
                                            @click="handleRemove(file)">
                                            <el-icon>
                                                <Delete />
                                            </el-icon>
                                        </span>
                                    </span>
                                </div>
                            </template>
                        </el-upload>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="submitActivity" :loading="submitting"><el-icon>
                                <Plus />
                            </el-icon>添加</el-button>
                    </el-form-item>
                </el-form>
            </el-dialog>

            <el-dialog v-model="dialogVisible">
                <img w-full :src="dialogImageUrl" alt="Preview Image" />
            </el-dialog>

            <el-dialog v-model="dialogFormVisible" title="Details" :width="dwidthVariable">
                <div>
                    <el-carousel :interval="5000" arrow="always">
                        <el-carousel-item v-for="imageData in selectedActivity.image" :key="imageData">
                            <el-image :src="getImageUrl(imageData)" alt="" style="width: 100%; height: 100%"
                                fit="contain"></el-image>
                        </el-carousel-item>
                    </el-carousel>

                    <div class="info">
                        <p><b>{{ selectedActivity.action }}</b></p>
                        <p><b>{{ selectedActivity.description }}</b></p>
                        <el-tag class="ml-2" type="success">{{ formattedCurrentDate(selectedActivity.time) }}</el-tag>
                    </div>
                </div>
            </el-dialog>

            <el-row>
                <el-col v-for="activity in activities" :key="activity._id" :span="6">
                    <el-card :body-style="{ padding: '0px' }" class="activity-card">
                        <img :src="activity.author === 'hanbao' ? hanbaoUrl : baoUrl" class="image" />
                        <div style="padding: 14px">
                            <span>{{ activity.action }}</span>
                            <div class="bottom">
                                <time class="time">{{ formattedCurrentDate(activity.time) }}</time>
                                <div class="button-container">
                                    <el-button class="button" @click="showActivityDetails(activity)">详情</el-button>
                                </div>
                            </div>
                        </div>
                    </el-card>
                </el-col>
                <el-col v-if="activities.length === 0" :span="24">
                    <el-alert title="No activities found" type="info" show-icon :closable="false"></el-alert>
                </el-col>
            </el-row>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            password: '',
            correctPassword: 'iamliu',
            isAuthenticated: false,
            awidthVariable: '33%',
            dwidthVariable: '30%',
            activity: { action: '', description: '', time: new Date().toISOString(), image: [] },
            activities: [],
            startTime: new Date('2023-11-01T00:00:00').getTime(),
            elapsedTime: 0,
            disabled: false,
            dialogVisible: false,
            formDialogVisible: false,
            dialogImageUrl: '',
            selectedFiles: [],
            submitting: false,
            selectedActivity: null,
            dialogFormVisible: false,
        };
    },
    computed: {
        formattedElapsedTime() {
            const days = Math.floor(this.elapsedTime / (3600 * 24));
            const hours = Math.floor((this.elapsedTime % (3600 * 24)) / 3600);
            const minutes = Math.floor((this.elapsedTime % 3600) / 60);
            const seconds = this.elapsedTime % 60;
            return `${days} 天 ${hours} 时 ${minutes} 分 ${seconds} 秒`;
        },
    },
    watch: {
        password(newValue) {
            this.isAuthenticated = newValue === this.correctPassword;
        }
    },
    methods: {
        async fetchActivities() {
            this.activities = (await this.$axios.get('/activities')).data;
        },
        async submitActivity() {
            if (this.activity.action.length === 0) {
                return;
            }
            try {
                this.submitting = true;
                this.activity.author = this.$store.getters.currentUser;
                this.activity.image = await Promise.all(this.selectedFiles.map(async file => {
                    const base64Data = await this.convertFileToBase64(file.raw);
                    return base64Data
                }));
                await this.$axios.post('/activities', this.activity);
                this.fetchActivities();
                this.clearForm();
            } finally {
                this.submitting = false;
            }
        },
        convertFileToBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => resolve(reader.result.split(',')[1]);
                reader.onerror = error => reject(error);
            });
        },
        clearForm() {
            this.activity.action = '';
            this.activity.description = '';
            this.activity.image = [];
            this.formDialogVisible = false;
            this.selectedFiles = [];

        },
        updateElapsedTime() {
            setInterval(() => {
                this.elapsedTime = Math.floor((Date.now() - this.startTime) / 1000);
            }, 1000);
        },
        handleFileChange(file, fileList) {
            this.selectedFiles = fileList;
        },
        handleRemove(file) {
            const index = this.selectedFiles.findIndex(selectedFile => selectedFile.uid === file.uid);
            if (index !== -1) {
                this.selectedFiles.splice(index, 1);
            }
        },
        handlePictureCardPreview(file) {
            if (file.url) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            }
        },
        showFormDialog() {
            this.formDialogVisible = true;
        },
        formattedCurrentDate(time) {
            const date = new Date(time);
            return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(
                date.getHours()
            ).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
        },
        showActivityDetails(activity) {
            this.selectedActivity = activity;
            this.dialogFormVisible = true;
        },
        getImageUrl(imageData) {
            return `data:image/jpeg;base64,${imageData}`;
        },
    },
    mounted() {
        this.fetchActivities();
        this.updateElapsedTime();
    },
};
</script>

<style>
.password-container {
    text-align: left;
    margin-top: 20px;
}

.input-container {
    display: flex;
    justify-content: center;
}

.password-input {
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.message p {
    margin-bottom: 10px;
    font-size: 16px;
}

.message p:first-child {
    font-weight: bold;
}

.message p:last-child {
    margin-bottom: 0;
}


/* 内容显示区域样式 */
.content {
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #f9f9f9;
}

/* 标题样式 */
.content h2 {
    font-size: 20px;
    color: #333;
}

/* 内容样式 */
.content p {
    font-size: 16px;
    color: #666;
}
</style>
