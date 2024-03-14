<template>
    <div class="footer-container">
        <div class="footer">
            <a href="https://beian.miit.gov.cn/" rel="external nofollow">
                沪ICP备2024041855号-1
            </a>
            · © 2024 hamburger
        </div>
    </div>
</template>

<style>
.footer-container {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    width: 100%; /* 让底部组件占据整个宽度 */
    min-height: 50px; /* 设置底部组件的最小高度 */
}

.footer {
    color: #aaa;
    font-size: 12px;
    line-height: 1.6em;
    padding: 10px;
}

.footer a {
    text-decoration: none;
    color: #aaa;
}
</style>
