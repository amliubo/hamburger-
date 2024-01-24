<template>
    <div :class="alertClass" role="alert" v-if="visible">
        {{ message }}
    </div>
</template>
  
<script>
export default {
    props: {
        message: String,
        alertClass: String,
    },
    data() {
        return {
            visible: true,
        };
    },
    methods: {
        hideAlert() {
            this.visible = false;
        },
    },
    mounted() {
        setTimeout(() => {
            this.hideAlert();
        }, 2000);
    },
};
</script>
