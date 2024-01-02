import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';
import login from '@/components/login.vue';
import index from '@/components/index.vue';

const routes = [
    {
        path: '/',
        name: 'index',
        component: index,
        meta: { title: 'Index -TreeHole' }
    },
    {
        path: '/login',
        name: 'login',
        component: login,
        meta: { title: 'Login -TreeHole', requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {

    // 设置页面标题
    document.title = to.meta.title || 'Default Title';
    const isAuthenticated = store.getters['isAuthenticated'];

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/');
    } else {
        next();
    }
});

export default router;
