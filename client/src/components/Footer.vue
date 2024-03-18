<template>
    <div class="footer-container">
        <div class="footer-text">
            <a href="https://beian.miit.gov.cn/" class="footer-link">沪ICP备2024041855号-1</a>
            <span class="footer-separator">·</span>
            <span>© Hamburger</span>
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
    width: 100%;
    min-height: 50px;
}

.footer-text {
    background-color: #f5f5f5;
    border-radius: 20px;
    display: inline-block;
    padding: 5px 10px;
}

.footer-link,
.footer-text span {
    color: #555;
    font-size: 12px;
    line-height: 1.6em;
    text-decoration: none;
}

.footer-separator {
    color: #aaa;
    margin: 0 5px;
}
</style>
