import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '首页'
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      title: '仪表板'
    }
  },
  {
    path: '/bidding',
    name: 'Bidding',
    component: () => import('@/views/Bidding.vue'),
    meta: {
      title: '投标管理'
    }
  },
  {
    path: '/bidding/create',
    name: 'CreateBid',
    component: () => import('@/views/bidding/CreateBid.vue'),
    meta: {
      title: '创建投标'
    }
  },
  {
    path: '/bidding/:id',
    name: 'BidDetail',
    component: () => import('@/views/bidding/BidDetail.vue'),
    meta: {
      title: '投标详情'
    }
  },
  {
    path: '/templates',
    name: 'Templates',
    component: () => import('@/views/Templates.vue'),
    meta: {
      title: '模板管理'
    }
  },
  {
    path: '/templates/create',
    name: 'CreateTemplate',
    component: () => import('@/views/templates/CreateTemplate.vue'),
    meta: {
      title: '创建模板'
    }
  },
  {
    path: '/templates/:name/edit',
    name: 'EditTemplate',
    component: () => import('@/views/templates/EditTemplate.vue'),
    meta: {
      title: '编辑模板'
    }
  },
  {
    path: '/generate',
    name: 'Generate',
    component: () => import('@/views/Generate.vue'),
    meta: {
      title: '文档生成'
    }
  },
  {
    path: '/analyze',
    name: 'Analyze',
    component: () => import('@/views/Analyze.vue'),
    meta: {
      title: '招标分析'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: {
      title: '系统设置'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '页面不存在'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta?.title) {
    document.title = `${to.meta.title} - AI标书助理系统`
  } else {
    document.title = 'AI标书助理系统'
  }
  next()
})

export default router