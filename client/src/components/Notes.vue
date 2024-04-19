<template>
    <div>
        <el-carousel height="70px" direction="vertical" :autoplay="true">
            <el-carousel-item v-for="(item, index) in items" :key="index">
                <el-alert :title="item.title" :type="item.type" :effect="item.effect" :closable="item.closable" />
            </el-carousel-item>
        </el-carousel>

        <div class="jumbotron jumbotron-fluid">
            <div>
                <el-divider content-position="left">
                    <el-tag class="mx-1" type="success" round>
                        <h5 class="display-7">✍️创建笔记</h5>
                    </el-tag>
                </el-divider>
                <p class="lead">记录笔记的好处在于它可以帮助我们更好地组织和管理思维，记录下重要的想法、观点、任务和经验。通过记录笔记，我们可以提高记忆力和思维能力和记录成长历程等。</p>
            </div>

            <el-input v-model="noteContent" show-word-limit maxlength="999" :autosize="{ minRows: 3, maxRows: 8 }"
                type="textarea"></el-input>
            <p />
            <el-button type="primary" @click="createNote" text><el-icon>
                    <Promotion />
                </el-icon> POST</el-button>
        </div>
        <br>
        <template v-if="notes.length > 0">
            <ul>
                <li v-for="(note, index) in notes" :key="index">{{ note.content }}</li>
            </ul>
        </template>
        <template v-else>
            <p class="lead">当前没有笔记信息，赶快记录一篇吧。</p>
        </template>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus';

export default {
    data() {
        return {
            items: [
                { title: "📣📣📣 2024 -03 -16 第1次线下课 四平路校区2202教室 💻", type: "info", effect: "dark", closable: false },
                { title: "📣📣📣 2024 -04 -20 第2次线下课 💻", type: "success", effect: "dark", closable: false },
                { title: "📣📣📣 2024 -05 -25 第3次线下课 💻", type: "success", effect: "dark", closable: false },
            ],
            noteContent: '',
            notes: []
        };
    },
    mounted() {
        this.getNotes();
    },
    methods: {
        async createNote() {
            if (this.noteContent.length == 0) {
                ElMessage.info('笔记内容不能为空！');
                return;
            }
            const response = await this.$axios.post('/notes', {
                content: this.noteContent
            });
            console.log(response)
            if (response.status === 200) {
                ElMessage.success('笔记创建成功！');
                this.noteContent = '';
                this.getNotes();
            }
        },
        async getNotes() {
            const response = await this.$axios.get('/notes');
            this.notes = response.data;
        }
    }
};
</script>
