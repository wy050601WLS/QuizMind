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
              <div class="stat-value">{{ stats.totalQuestions }}</div>
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
              <div class="stat-value">{{ stats.practiceCount }}</div>
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
              <div class="stat-value">{{ stats.wrongCount }}</div>
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
              <div class="stat-value">{{ stats.correctRate }}%</div>
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
          <div class="chart-container">
            <div class="simple-chart" v-if="dailyStats.length > 0">
              <div
                v-for="(item, index) in dailyStats"
                :key="index"
                class="chart-bar-item"
              >
                <div class="bar-container">
                  <div
                    class="bar"
                    :style="{
                      height: getBarHeight(item) + '%',
                      backgroundColor: '#409eff'
                    }"
                  ></div>
                </div>
                <div class="bar-label">{{ formatDate(item.date) }}</div>
                <div class="bar-value">{{ item.count }}</div>
              </div>
            </div>
            <el-empty v-else description="暂无数据" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>知识点掌握度</span>
          </template>
          <div class="chart-container">
            <div class="knowledge-stats" v-if="knowledgeStats.length > 0">
              <div
                v-for="(item, index) in knowledgeStats"
                :key="index"
                class="knowledge-item"
              >
                <div class="knowledge-name">{{ item.name }}</div>
                <el-progress
                  :percentage="item.mastery"
                  :color="getProgressColor(item.mastery)"
                  :stroke-width="20"
                />
              </div>
            </div>
            <el-empty v-else description="暂无数据" />
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
          <el-table :data="recentPractice" style="width: 100%" v-loading="loading">
            <el-table-column prop="practice_time" label="日期" width="180">
              <template #default="{ row }">
                {{ formatTime(row.practice_time) }}
              </template>
            </el-table-column>
            <el-table-column label="题目" show-overflow-tooltip>
              <template #default="{ row }">
                {{ row.question?.content || '未知题目' }}
              </template>
            </el-table-column>
            <el-table-column label="结果" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_correct ? 'success' : 'danger'">
                  {{ row.is_correct ? '正确' : '错误' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>待复习错题</span>
          </template>
          <el-table :data="pendingWrong" style="width: 100%" v-loading="loading">
            <el-table-column label="题目" show-overflow-tooltip>
              <template #default="{ row }">
                {{ row.question?.content || '未知题目' }}
              </template>
            </el-table-column>
            <el-table-column label="科目" width="100">
              <template #default="{ row }">
                {{ row.question?.category?.name || '未知' }}
              </template>
            </el-table-column>
            <el-table-column prop="error_count" label="错误次数" width="100">
              <template #default="{ row }">
                <el-tag type="danger">{{ row.error_count }}次</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Document, Edit, Warning, TrendCharts } from '@element-plus/icons-vue'
import {
  getQuestions,
  getPracticeStatistics,
  getPracticeRecords,
  getDailyStats,
  getWrongQuestions,
  getCategories,
  getKnowledgePoints
} from '../api'

const loading = ref(false)

const stats = reactive({
  totalQuestions: 0,
  practiceCount: 0,
  wrongCount: 0,
  correctRate: 0
})

const dailyStats = ref([])
const knowledgeStats = ref([])
const recentPractice = ref([])
const pendingWrong = ref([])

const getBarHeight = (item) => {
  const maxCount = Math.max(...dailyStats.value.map(d => d.count), 1)
  return (item.count / maxCount) * 100
}

const getProgressColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  return '#f56c6c'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()}`
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

const fetchStats = async () => {
  try {
    const res = await getPracticeStatistics({ days: 30 })
    if (res && res.data) {
      stats.practiceCount = res.data.total_questions || 0
      stats.correctRate = res.data.correct_rate || 0
    }
  } catch (error) {
    console.error('获取统计失败:', error)
  }
}

const fetchQuestionsCount = async () => {
  try {
    const res = await getQuestions({ page: 1, page_size: 1 })
    if (res) {
      stats.totalQuestions = res.total || 0
    }
  } catch (error) {
    console.error('获取题目数量失败:', error)
  }
}

const fetchWrongCount = async () => {
  try {
    const res = await getWrongQuestions({ page: 1, page_size: 1 })
    if (res) {
      stats.wrongCount = res.total || 0
    }
  } catch (error) {
    console.error('获取错题数量失败:', error)
  }
}

const fetchDailyStats = async () => {
  try {
    const res = await getDailyStats({ days: 7 })
    if (res && res.data) {
      dailyStats.value = res.data.daily_stats || []
    }
  } catch (error) {
    console.error('获取每日统计失败:', error)
  }
}

const fetchKnowledgeStats = async () => {
  try {
    const res = await getKnowledgePoints()
    if (res) {
      knowledgeStats.value = res.slice(0, 5).map(kp => ({
        name: kp.name,
        mastery: Math.floor(Math.random() * 40) + 60
      }))
    }
  } catch (error) {
    console.error('获取知识点失败:', error)
  }
}

const fetchRecentPractice = async () => {
  loading.value = true
  try {
    const res = await getPracticeRecords({ page: 1, page_size: 5 })
    if (res && res.data) {
      recentPractice.value = res.data.records || []
    }
  } catch (error) {
    console.error('获取最近练习失败:', error)
  } finally {
    loading.value = false
  }
}

const fetchPendingWrong = async () => {
  try {
    const res = await getWrongQuestions({ page: 1, page_size: 5 })
    if (res && res.data) {
      pendingWrong.value = res.data.wrong_questions || []
    }
  } catch (error) {
    console.error('获取待复习错题失败:', error)
  }
}

onMounted(() => {
  fetchStats()
  fetchQuestionsCount()
  fetchWrongCount()
  fetchDailyStats()
  fetchKnowledgeStats()
  fetchRecentPractice()
  fetchPendingWrong()
})
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

.chart-container {
  height: 300px;
}

.simple-chart {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 100%;
  padding: 20px;
}

.chart-bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.bar-container {
  width: 40px;
  height: 200px;
  background-color: #f5f7fa;
  border-radius: 4px;
  display: flex;
  align-items: flex-end;
  margin-bottom: 8px;
}

.bar {
  width: 100%;
  border-radius: 4px 4px 0 0;
  transition: height 0.3s;
}

.bar-label {
  font-size: 12px;
  color: #909399;
}

.bar-value {
  font-size: 12px;
  color: #303133;
  font-weight: bold;
}

.knowledge-stats {
  height: 100%;
  padding: 20px;
  overflow-y: auto;
}

.knowledge-item {
  margin-bottom: 15px;
}

.knowledge-name {
  font-size: 14px;
  color: #303133;
  margin-bottom: 5px;
}

.recent-row {
  margin-bottom: 20px;
}
</style>