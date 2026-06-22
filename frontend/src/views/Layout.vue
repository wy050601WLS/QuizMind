<template>
  <div class="layout-container">
    <el-container>
      <el-aside width="220px" class="aside">
        <div class="logo">
          <h2>AI刷题助手</h2>
        </div>
        <el-menu
          :default-active="activeMenu"
          router
          class="el-menu-vertical"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409eff"
        >
          <el-menu-item index="/dashboard">
            <el-icon><HomeFilled /></el-icon>
            <span>首页仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/questions">
            <el-icon><Document /></el-icon>
            <span>题库管理</span>
          </el-menu-item>
          <el-menu-item index="/practice">
            <el-icon><Edit /></el-icon>
            <span>刷题练习</span>
          </el-menu-item>
          <el-menu-item index="/wrong">
            <el-icon><Warning /></el-icon>
            <span>错题本</span>
          </el-menu-item>
          <el-menu-item index="/statistics">
            <el-icon><DataAnalysis /></el-icon>
            <span>学习统计</span>
          </el-menu-item>
          <el-menu-item index="/api-test">
            <el-icon><Connection /></el-icon>
            <span>API测试</span>
          </el-menu-item>
          <el-menu-item index="/ai-question">
            <el-icon><MagicStick /></el-icon>
            <span>AI智能出题</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
          <div class="header-left">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item>{{ currentRoute.meta.title }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="header-right">
            <el-dropdown>
              <span class="el-dropdown-link">
                用户
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>个人中心</el-dropdown-item>
                  <el-dropdown-item>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main class="main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeFilled,
  Document,
  Edit,
  Warning,
  DataAnalysis,
  ArrowDown,
  Connection,
  MagicStick
} from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
const currentRoute = computed(() => route)
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.aside {
  background-color: #304156;
  overflow: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #263445;
}

.logo h2 {
  color: #fff;
  margin: 0;
  font-size: 18px;
}

.el-menu-vertical {
  border-right: none;
}

.header {
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>