<template>
  <div class="practice-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>刷题练习</span>
          <div class="header-actions">
            <el-button type="primary" @click="startPractice" :loading="loading">
              <el-icon><VideoPlay /></el-icon>
              开始练习
            </el-button>
            <el-button @click="resetPractice" v-if="questions.length > 0">
              <el-icon><RefreshRight /></el-icon>
              重新开始
            </el-button>
          </div>
        </div>
      </template>

      <div class="practice-config">
        <el-form :model="configForm" label-width="100px">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="选择科目">
                <el-select v-model="configForm.category_id" placeholder="选择科目">
                  <el-option
                    v-for="cat in categories"
                    :key="cat.id"
                    :label="cat.name"
                    :value="cat.id"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="选择知识点">
                <el-select v-model="configForm.knowledge_point_id" placeholder="选择知识点" clearable>
                  <el-option
                    v-for="kp in filteredKnowledgePoints"
                    :key="kp.id"
                    :label="kp.name"
                    :value="kp.id"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="题目数量">
                <el-input-number v-model="configForm.count" :min="1" :max="50" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="练习模式">
                <el-radio-group v-model="configForm.mode">
                  <el-radio label="sequential">顺序练习</el-radio>
                  <el-radio label="random">随机练习</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="难度要求">
                <el-select v-model="configForm.difficulty" placeholder="选择难度" clearable>
                  <el-option label="简单" value="easy" />
                  <el-option label="中等" value="medium" />
                  <el-option label="困难" value="hard" />
                  <el-option label="不限" value="" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>

      <el-divider />

      <div class="question-area" v-if="currentQuestion">
        <div class="question-header">
          <span class="question-index">第 {{ currentIndex + 1 }} 题 / 共 {{ questions.length }} 题</span>
          <div>
            <el-tag :type="getDifficultyType(currentQuestion.difficulty)" style="margin-right: 10px">
              {{ getDifficultyLabel(currentQuestion.difficulty) }}
            </el-tag>
            <el-tag type="info">{{ getQuestionTypeLabel(currentQuestion.question_type) }}</el-tag>
          </div>
        </div>

        <div class="question-content">
          <p>{{ currentQuestion.content }}</p>
        </div>

        <div class="options-area" v-if="currentQuestion.question_type === 'single' || currentQuestion.question_type === 'multiple'">
          <el-checkbox-group v-model="userAnswer" v-if="currentQuestion.question_type === 'multiple'" class="options-group">
            <el-checkbox
              v-for="(option, index) in parsedOptions"
              :key="index"
              :label="option.label"
              class="option-item"
            >
              {{ option.label }}. {{ option.content }}
            </el-checkbox>
          </el-checkbox-group>
          <el-radio-group v-model="userAnswer" v-else class="options-group">
            <el-radio
              v-for="(option, index) in parsedOptions"
              :key="index"
              :label="option.label"
              class="option-item"
            >
              {{ option.label }}. {{ option.content }}
            </el-radio>
          </el-radio-group>
        </div>

        <div class="answer-area" v-else-if="currentQuestion.question_type === 'judge'">
          <el-radio-group v-model="userAnswer" class="options-group">
            <el-radio label="正确" class="option-item">正确</el-radio>
            <el-radio label="错误" class="option-item">错误</el-radio>
          </el-radio-group>
        </div>

        <div class="answer-area" v-else>
          <el-input v-model="userAnswer" placeholder="请输入答案" />
        </div>

        <div class="action-buttons">
          <el-button @click="prevQuestion" :disabled="currentIndex === 0">上一题</el-button>
          <el-button type="primary" @click="handleSubmitAnswer" :loading="submitLoading">
            {{ showResult ? '已提交' : '提交答案' }}
          </el-button>
          <el-button @click="nextQuestion" :disabled="currentIndex === questions.length - 1">下一题</el-button>
        </div>

        <div class="result-area" v-if="showResult">
          <el-alert
            :title="isCorrect ? '回答正确！' : '回答错误'"
            :type="isCorrect ? 'success' : 'error'"
            :closable="false"
            show-icon
          >
            <template #default>
              <p v-if="currentQuestion.explanation"><strong>解析：</strong>{{ currentQuestion.explanation }}</p>
              <p v-if="!isCorrect"><strong>正确答案：</strong>{{ currentQuestion.answer }}</p>
            </template>
          </el-alert>
        </div>

        <div class="progress-area">
          <el-progress
            :percentage="progressPercentage"
            :format="progressFormat"
            :color="progressColors"
          />
        </div>
      </div>

      <div class="empty-area" v-else>
        <el-empty description="请配置练习参数后开始练习" />
      </div>
    </el-card>

    <!-- 练习完成对话框 -->
    <el-dialog v-model="completeDialogVisible" title="练习完成" width="400px">
      <div class="complete-content">
        <el-statistic title="总题数" :value="questions.length" />
        <el-statistic title="正确数" :value="correctCount" />
        <el-statistic title="正确率" :value="correctRate" suffix="%" />
      </div>
      <template #footer>
        <el-button @click="completeDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="resetPractice">再来一次</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { VideoPlay, RefreshRight } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import {
  getQuestions,
  getCategories,
  getKnowledgePoints,
  submitAnswer
} from '../api'

const loading = ref(false)
const submitLoading = ref(false)
const completeDialogVisible = ref(false)

const configForm = reactive({
  category_id: null,
  knowledge_point_id: null,
  count: 10,
  mode: 'sequential',
  difficulty: ''
})

const categories = ref([])
const knowledgePoints = ref([])
const questions = ref([])
const currentIndex = ref(0)
const userAnswer = ref(null)
const showResult = ref(false)
const isCorrect = ref(false)
const correctCount = ref(0)
const answeredQuestions = ref(new Set())

const currentQuestion = computed(() => questions.value[currentIndex.value])

const filteredKnowledgePoints = computed(() => {
  if (!configForm.category_id) return knowledgePoints.value
  return knowledgePoints.value.filter(kp => kp.category_id === configForm.category_id)
})

const parsedOptions = computed(() => {
  if (!currentQuestion.value || !currentQuestion.value.options) return []
  try {
    return typeof currentQuestion.value.options === 'string'
      ? JSON.parse(currentQuestion.value.options)
      : currentQuestion.value.options
  } catch {
    return []
  }
})

const progressPercentage = computed(() => {
  if (questions.value.length === 0) return 0
  return Math.round((answeredQuestions.value.size / questions.value.length) * 100)
})

const correctRate = computed(() => {
  if (answeredQuestions.value.size === 0) return 0
  return Math.round((correctCount.value / answeredQuestions.value.size) * 100)
})

const progressFormat = (percentage) => {
  return `${answeredQuestions.value.size}/${questions.value.length}`
}

const progressColors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#409eff', percentage: 60 },
  { color: '#67c23a', percentage: 80 },
  { color: '#67c23a', percentage: 100 }
]

const getDifficultyType = (difficulty) => {
  const types = { easy: 'success', medium: 'warning', hard: 'danger' }
  return types[difficulty] || 'info'
}

const getDifficultyLabel = (difficulty) => {
  const labels = { easy: '简单', medium: '中等', hard: '困难' }
  return labels[difficulty] || difficulty
}

const getQuestionTypeLabel = (type) => {
  const types = { single: '单选题', multiple: '多选题', judge: '判断题', blank: '填空题' }
  return types[type] || type
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
  } catch (error) {
    console.error('获取知识点失败:', error)
  }
}

const startPractice = async () => {
  if (!configForm.category_id) {
    ElMessage.warning('请选择科目')
    return
  }

  loading.value = true
  try {
    const params = {
      page: 1,
      page_size: configForm.count
    }
    
    const cat = categories.value.find(c => c.id === configForm.category_id)
    if (cat) params.subject = cat.name
    if (configForm.knowledge_point_id) params.knowledge_point_id = configForm.knowledge_point_id
    if (configForm.difficulty) params.difficulty = configForm.difficulty

    const res = await getQuestions(params)
    questions.value = res.data.questions || []
    
    if (questions.value.length === 0) {
      ElMessage.warning('没有找到符合条件的题目')
      return
    }

    if (configForm.mode === 'random') {
      questions.value = shuffleArray(questions.value)
    }

    currentIndex.value = 0
    userAnswer.value = ''
    showResult.value = false
    correctCount.value = 0
    answeredQuestions.value = new Set()
    ElMessage.success(`已加载 ${questions.value.length} 道题目`)
  } catch (error) {
    ElMessage.error('获取题目失败')
  } finally {
    loading.value = false
  }
}

const shuffleArray = (array) => {
  const newArray = [...array]
  for (let i = newArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [newArray[i], newArray[j]] = [newArray[j], newArray[i]]
  }
  return newArray
}

const handleSubmitAnswer = async () => {
  if (!userAnswer.value) {
    ElMessage.warning('请先作答')
    return
  }

  if (answeredQuestions.value.has(currentIndex.value)) {
    ElMessage.info('该题已提交过答案')
    return
  }

  submitLoading.value = true
  try {
    const answerStr = Array.isArray(userAnswer.value) ? userAnswer.value.join(',') : userAnswer.value
    const res = await submitAnswer({
      question_id: currentQuestion.value.id,
      my_answer: answerStr
    })

    isCorrect.value = res.data.is_correct === 1
    showResult.value = true
    answeredQuestions.value.add(currentIndex.value)

    if (isCorrect.value) {
      correctCount.value++
      ElMessage.success('回答正确！')
    } else {
      ElMessage.error('回答错误')
    }

    if (answeredQuestions.value.size === questions.value.length) {
      setTimeout(() => {
        completeDialogVisible.value = true
      }, 1000)
    }
  } catch (error) {
    ElMessage.error('提交答案失败')
  } finally {
    submitLoading.value = false
  }
}

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    resetQuestionState()
  }
}

const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    resetQuestionState()
  }
}

const resetQuestionState = () => {
  if (answeredQuestions.value.has(currentIndex.value)) {
    showResult.value = true
  } else {
    showResult.value = false
  }
  // 根据题型设置 userAnswer 的类型
  if (currentQuestion.value?.question_type === 'multiple') {
    userAnswer.value = []
  } else {
    userAnswer.value = ''
  }
}

const resetPractice = () => {
  questions.value = []
  currentIndex.value = 0
  userAnswer.value = null
  showResult.value = false
  correctCount.value = 0
  answeredQuestions.value = new Set()
  completeDialogVisible.value = false
}

onMounted(() => {
  fetchCategories()
  fetchKnowledgePoints()
})
</script>

<style scoped>
.practice-container {
  padding: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.practice-config {
  margin-bottom: 20px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.question-index {
  font-size: 14px;
  color: #909399;
}

.question-content {
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.options-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-item {
  padding: 10px 15px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  transition: all 0.3s;
}

.option-item:hover {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.result-area {
  margin-top: 20px;
}

.progress-area {
  margin-top: 20px;
}

.empty-area {
  padding: 60px 0;
}

.complete-content {
  display: flex;
  justify-content: space-around;
  text-align: center;
}
</style>