<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #409eff">
              <el-icon size="24"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">1,234</div>
              <div class="stat-label">题目总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #67c23a">
              <el-icon size="24"><Edit /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">567</div>
              <div class="stat-label">已刷题目</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #e6a23c">
              <el-icon size="24"><Warning /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">89</div>
              <div class="stat-label">错题数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #f56c6c">
              <el-icon size="24"><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">78.5%</div>
              <div class="stat-label">正确率</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>最近7天刷题趋势</span>
          </template>
          <div class="chart-placeholder">
            <el-empty description="图表区域（待集成ECharts）" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>知识点掌握度</span>
          </template>
          <div class="chart-placeholder">
            <el-empty description="雷达图区域（待集成ECharts）" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="recent-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>最近练习记录</span>
          </template>
          <el-table :data="recentPractice" style="width: 100%">
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="subject" label="科目" width="100" />
            <el-table-column prop="count" label="题数" width="80" />
            <el-table-column prop="accuracy" label="正确率" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>待复习错题</span>
          </template>
          <el-table :data="pendingWrong" style="width: 100%">
            <el-table-column prop="question" label="题目" show-overflow-tooltip />
            <el-table-column prop="subject" label="科目" width="100" />
            <el-table-column prop="errorCount" label="错误次数" width="100" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Document, Edit, Warning, TrendCharts } from '@element-plus/icons-vue'

const recentPractice = ref([
  { date: '2026-06-22', subject: '数学', count: 20, accuracy: '85%' },
  { date: '2026-06-21', subject: '英语', count: 15, accuracy: '73%' },
  { date: '2026-06-20', subject: '数学', count: 25, accuracy: '80%' },
  { date: '2026-06-19', subject: '物理', count: 10, accuracy: '70%' },
  { date: '2026-06-18', subject: '英语', count: 18, accuracy: '78%' }
])

const pendingWrong = ref([
  { question: '关于二次函数的最值问题', subject: '数学', errorCount: 3 },
  { question: '虚拟语气的用法', subject: '英语', errorCount: 2 },
  { question: '牛顿第二定律应用', subject: '物理', errorCount: 2 },
  { question: '化学平衡常数计算', subject: '化学', errorCount: 1 }
])
</script>

<style scoped>
.dashboard-container {
  padding: 10px;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-right: 12px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.chart-row {
  margin-bottom: 20px;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.recent-row {
  margin-bottom: 20px;
}
</style>