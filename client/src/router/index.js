import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';
import index from '@/components/index.vue';

const routes = [
    {
        path: '/',
        name: 'index',
        component: index,
        meta: { title: 'Humburger' }
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
