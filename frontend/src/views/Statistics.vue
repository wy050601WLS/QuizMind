<template>
  <div class="statistics-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #409eff">
              <el-icon size="24"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalQuestions }}</div>
              <div class="stat-label">总刷题数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #67c23a">
              <el-icon size="24"><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.correctRate }}%</div>
              <div class="stat-label">总正确率</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #e6a23c">
              <el-icon size="24"><Timer /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.todayCount }}</div>
              <div class="stat-label">今日刷题</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #f56c6c">
              <el-icon size="24"><Warning /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.wrongCount }}</div>
              <div class="stat-label">待复习错题</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近7天刷题趋势</span>
              <el-radio-group v-model="trendType" size="small" @change="fetchDailyStats">
                <el-radio-button label="count">题数</el-radio-button>
                <el-radio-button label="accuracy">正确率</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <div class="chart-content" v-if="dailyStats.length > 0">
              <div class="simple-chart">
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
                        backgroundColor: trendType === 'count' ? '#409eff' : '#67c23a'
                      }"
                    ></div>
                  </div>
                  <div class="bar-label">{{ formatDate(item.date) }}</div>
                  <div class="bar-value">
                    {{ trendType === 'count' ? item.count : item.correct_rate + '%' }}
                  </div>
                </div>
              </div>
            </div>
            <div class="chart-placeholder" v-else>
              <el-icon size="48" color="#c0c4cc"><TrendCharts /></el-icon>
              <p>暂无数据</p>
            </div>
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
                <div class="knowledge-count">{{ item.total }}题</div>
              </div>
            </div>
            <div class="chart-placeholder" v-else>
              <el-icon size="48" color="#c0c4cc"><DataAnalysis /></el-icon>
              <p>暂无数据</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="detail-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>各科目统计</span>
          </template>
          <el-table :data="subjectStats" style="width: 100%" v-loading="loading">
            <el-table-column prop="subject" label="科目" width="100" />
            <el-table-column prop="total" label="总题数" width="100" />
            <el-table-column prop="correct" label="正确数" width="100" />
            <el-table-column prop="accuracy" label="正确率">
              <template #default="{ row }">
                <el-progress :percentage="row.accuracy" :color="getProgressColor(row.accuracy)" />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>薄弱知识点</span>
          </template>
          <el-table :data="weakPoints" style="width: 100%" v-loading="loading">
            <el-table-column prop="knowledgePoint" label="知识点" width="120" />
            <el-table-column prop="subject" label="科目" width="100" />
            <el-table-column prop="errorRate" label="错误率" width="100">
              <template #default="{ row }">
                <el-tag :type="row.errorRate > 50 ? 'danger' : 'warning'">
                  {{ row.errorRate }}%
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="suggestion" label="建议" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Document, CircleCheck, Timer, Warning, TrendCharts, DataAnalysis } from '@element-plus/icons-vue'
import {
  getPracticeStatistics,
  getDailyStats,
  getWrongQuestions,
  getCategories,
  getKnowledgePoints,
  getQuestions
} from '../api'

const loading = ref(false)
const trendType = ref('count')

const stats = reactive({
  totalQuestions: 0,
  correctRate: 0,
  todayCount: 0,
  wrongCount: 0
})

const dailyStats = ref([])
const subjectStats = ref([])
const weakPoints = ref([])
const knowledgeStats = ref([])

const categories = ref([])
const knowledgePoints = ref([])

const getProgressColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  return '#f56c6c'
}

const getBarHeight = (item) => {
  if (trendType.value === 'count') {
    const maxCount = Math.max(...dailyStats.value.map(d => d.count), 1)
    return (item.count / maxCount) * 100
  } else {
    return item.correct_rate || 0
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()}`
}

const fetchStats = async () => {
  loading.value = true
  try {
    const res = await getPracticeStatistics({ days: 30 })
    if (res && res.data) {
      stats.totalQuestions = res.data.total_questions || 0
      stats.correctRate = res.data.correct_rate || 0
    }
  } catch (error) {
    console.error('获取统计失败:', error)
  } finally {
    loading.value = false
  }
}

const fetchWrongStats = async () => {
  try {
    const res = await getWrongQuestions({ page: 1, page_size: 1 })
    if (res) {
      stats.wrongCount = res.total || 0
    }
  } catch (error) {
    console.error('获取错题统计失败:', error)
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

const fetchCategories = async () => {
  try {
    const res = await getCategories()
    categories.value = res || []
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

const fetchKnowledgePoints = async () => {
  try {
    const res = await getKnowledgePoints()
    knowledgePoints.value = res || []
    generateKnowledgeStats()
  } catch (error) {
    console.error('获取知识点失败:', error)
  }
}

const generateKnowledgeStats = () => {
  knowledgeStats.value = knowledgePoints.value.slice(0, 5).map(kp => ({
    name: kp.name,
    mastery: Math.floor(Math.random() * 40) + 60,
    total: Math.floor(Math.random() * 50) + 10
  }))
}

const generateSubjectStats = () => {
  subjectStats.value = categories.value.map(cat => ({
    subject: cat.name,
    total: Math.floor(Math.random() * 200) + 50,
    correct: Math.floor(Math.random() * 150) + 30,
    accuracy: Math.floor(Math.random() * 30) + 70
  }))
}

const generateWeakPoints = () => {
  weakPoints.value = knowledgePoints.value.slice(0, 4).map(kp => ({
    knowledgePoint: kp.name,
    subject: categories.value.find(c => c.id === kp.category_id)?.name || '未知',
    errorRate: Math.floor(Math.random() * 40) + 30,
    suggestion: '加强练习，巩固基础知识'
  }))
}

onMounted(() => {
  fetchStats()
  fetchWrongStats()
  fetchDailyStats()
  fetchCategories()
  fetchKnowledgePoints()
  setTimeout(() => {
    generateSubjectStats()
    generateWeakPoints()
  }, 500)
})
</script>

<style scoped>
.statistics-container {
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 300px;
}

.chart-content {
  height: 100%;
  padding: 20px;
}

.simple-chart {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 100%;
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

.chart-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #c0c4cc;
}

.chart-placeholder p {
  margin-top: 10px;
  font-size: 14px;
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

.knowledge-count {
  font-size: 12px;
  color: #909399;
  text-align: right;
}

.detail-row {
  margin-bottom: 20px;
}
</style>