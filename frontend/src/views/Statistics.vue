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
              <div class="stat-value">{{ stats.totalTime }}h</div>
              <div class="stat-label">学习时长</div>
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
              <el-radio-group v-model="trendType" size="small">
                <el-radio-button label="count">题数</el-radio-button>
                <el-radio-button label="accuracy">正确率</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <div class="chart-placeholder">
              <el-icon size="48" color="#c0c4cc"><TrendCharts /></el-icon>
              <p>ECharts趋势图（待集成）</p>
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
            <div class="chart-placeholder">
              <el-icon size="48" color="#c0c4cc"><DataAnalysis /></el-icon>
              <p>ECharts雷达图（待集成）</p>
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
          <el-table :data="subjectStats" style="width: 100%">
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
          <el-table :data="weakPoints" style="width: 100%">
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
import { ref, reactive } from 'vue'
import { Document, CircleCheck, Timer, Warning, TrendCharts, DataAnalysis } from '@element-plus/icons-vue'

const trendType = ref('count')

const stats = reactive({
  totalQuestions: 1256,
  correctRate: 78.5,
  totalTime: 45.2,
  wrongCount: 89
})

const subjectStats = ref([
  { subject: '数学', total: 450, correct: 360, accuracy: 80 },
  { subject: '英语', total: 380, correct: 285, accuracy: 75 },
  { subject: '物理', total: 250, correct: 188, accuracy: 75.2 },
  { subject: '化学', total: 176, correct: 140, accuracy: 79.5 }
])

const weakPoints = ref([
  { knowledgePoint: '三角函数', subject: '数学', errorRate: 45, suggestion: '加强公式记忆和应用练习' },
  { knowledgePoint: '虚拟语气', subject: '英语', errorRate: 62, suggestion: '重点复习虚拟语气的三种情况' },
  { knowledgePoint: '电磁感应', subject: '物理', errorRate: 55, suggestion: '多做综合应用题' },
  { knowledgePoint: '化学平衡', subject: '化学', errorRate: 48, suggestion: '理解勒夏特列原理' }
])

const getProgressColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  return '#f56c6c'
}
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

.detail-row {
  margin-bottom: 20px;
}
</style>