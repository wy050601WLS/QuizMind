import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '首页仪表盘' }
      },
      {
        path: 'questions',
        name: 'Questions',
        component: () => import('../views/Questions.vue'),
        meta: { title: '题库管理' }
      },
      {
        path: 'practice',
        name: 'Practice',
        component: () => import('../views/Practice.vue'),
        meta: { title: '刷题练习' }
      },
      {
        path: 'wrong',
        name: 'WrongQuestions',
        component: () => import('../views/WrongQuestions.vue'),
        meta: { title: '错题本' }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('../views/Statistics.vue'),
        meta: { title: '学习统计' }
      },
      {
        path: 'api-test',
        name: 'ApiTest',
        component: () => import('../views/ApiTest.vue'),
        meta: { title: 'API测试' }
      },
      {
        path: 'ai-question',
        name: 'AiQuestion',
        component: () => import('../views/AiQuestion.vue'),
        meta: { title: 'AI智能出题' }
      },
      {
        path: 'weak-points',
        name: 'WeakPoints',
        component: () => import('../views/WeakPoints.vue'),
        meta: { title: '薄弱点分析' }
      },
      {
        path: 'exam-paper',
        name: 'ExamPaper',
        component: () => import('../views/ExamPaper.vue'),
        meta: { title: 'AI模拟组卷' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - AI刷题助手` : 'AI刷题助手'
  next()
})

export default router