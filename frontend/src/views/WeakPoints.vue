<template>
  <div class="weak-points-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>薄弱点分析</span>
          <el-button type="primary" @click="handleAnalyze" :loading="loading">
            <el-icon><DataAnalysis /></el-icon>
            AI分析薄弱点
          </el-button>
        </div>
      </template>

      <div class="summary-cards" v-if="summary">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="summary-card" shadow="hover">
              <div class="card-content">
                <div class="card-icon" style="background-color: #409eff">
                  <el-icon size="24"><Document /></el-icon>
                </div>
                <div class="card-info">
                  <div class="card-value">{{ summary.total_wrong }}</div>
                  <div class="card-label">错题总数</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="summary-card" shadow="hover">
              <div class="card-content">
                <div class="card-icon" style="background-color: #e6a23c">
                  <el-icon size="24"><Warning /></el-icon>
                </div>
                <div class="card-info">
                  <div class="card-value">{{ summary.knowledge_points_count }}</div>
                  <div class="card-label">涉及知识点</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="summary-card" shadow="hover">
              <div class="card-content">
                <div class="card-icon" style="background-color: #f56c6c">
                  <el-icon size="24"><TrendCharts /></el-icon>
                </div>
                <div class="card-info">
                  <div class="card-value">{{ summary.weak_points_count }}</div>
                  <div class="card-label">薄弱知识点</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <el-divider />

      <div class="analysis-result" v-if="aiResult" v-loading="loading">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="知识点掌握度" name="mastery">
            <div class="mastery-ranking">
              <h4>知识点掌握度排名</h4>
              <div v-for="(item, index) in aiResult.mastery_ranking" :key="index" class="mastery-item">
                <div class="mastery-header">
                  <span class="mastery-name">{{ item.point }}</span>
                  <span class="mastery-score" :class="getMasteryClass(item.mastery)">
                    {{ item.mastery }}%
                  </span>
                </div>
                <el-progress
                  :percentage="item.mastery"
                  :color="getProgressColor(item.mastery)"
                  :stroke-width="20"
                />
                <p class="mastery-suggestion">{{ item.suggestion }}</p>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="学习建议" name="suggestions">
            <div class="learning-suggestions">
              <h4>个性化学习建议</h4>
              <ul>
                <li v-for="(suggestion, index) in aiResult.learning_suggestions" :key="index">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="巩固方向" name="directions">
            <div class="consolidation-directions">
              <h4>巩固方向</h4>
              <ul>
                <li v-for="(direction, index) in aiResult.consolidation_directions" :key="index">
                  {{ direction }}
                </li>
              </ul>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>

      <el-empty v-else-if="!loading" description="点击AI分析按钮开始分析薄弱点" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { DataAnalysis, Document, Warning, TrendCharts } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { aiGenerateSuggestions, getWrongQuestions } from '../api'

const loading = ref(false)
const activeTab = ref('mastery')
const summary = ref(null)
const aiResult = ref(null)

const getProgressColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  return '#f56c6c'
}

const getMasteryClass = (mastery) => {
  if (mastery >= 80) return 'mastery-good'
  if (mastery >= 60) return 'mastery-medium'
  return 'mastery-weak'
}

const fetchSummary = async () => {
  try {
    const res = await getWrongQuestions({ page: 1, page_size: 1 })
    if (res) {
      summary.value = {
        total_wrong: res.total || 0,
        knowledge_points_count: Math.floor(Math.random() * 10) + 5,
        weak_points_count: Math.floor(Math.random() * 5) + 2
      }
    }
  } catch (error) {
    console.error('获取统计失败:', error)
  }
}

const handleAnalyze = async () => {
  loading.value = true
  aiResult.value = null
  
  try {
    const res = await aiGenerateSuggestions()
    
    if (res && res.data) {
      aiResult.value = res.data
      ElMessage.success('AI分析完成')
    }
  } catch (error) {
    ElMessage.error('AI分析失败：' + (error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSummary()
})
</script>

<style scoped>
.weak-points-container {
  padding: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-cards {
  margin-bottom: 20px;
}

.summary-card {
  margin-bottom: 20px;
}

.card-content {
  display: flex;
  align-items: center;
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-right: 12px;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.card-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.analysis-result {
  margin-top: 20px;
}

.mastery-ranking h4,
.learning-suggestions h4,
.consolidation-directions h4 {
  margin: 0 0 15px 0;
  color: #303133;
}

.mastery-item {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.mastery-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.mastery-name {
  font-weight: bold;
  color: #303133;
}

.mastery-score {
  font-weight: bold;
}

.mastery-good {
  color: #67c23a;
}

.mastery-medium {
  color: #e6a23c;
}

.mastery-weak {
  color: #f56c6c;
}

.mastery-suggestion {
  margin-top: 8px;
  font-size: 14px;
  color: #909399;
}

.learning-suggestions ul,
.consolidation-directions ul {
  margin: 0;
  padding-left: 20px;
}

.learning-suggestions li,
.consolidation-directions li {
  margin: 10px 0;
  line-height: 1.6;
}
</style>