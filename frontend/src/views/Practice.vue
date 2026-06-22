<template>
  <div class="practice-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>刷题练习</span>
          <div class="header-actions">
            <el-button type="primary" @click="startPractice">
              <el-icon><VideoPlay /></el-icon>
              开始练习
            </el-button>
          </div>
        </div>
      </template>

      <div class="practice-config">
        <el-form :model="configForm" label-width="100px">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="选择科目">
                <el-select v-model="configForm.subject" placeholder="选择科目">
                  <el-option label="数学" value="math" />
                  <el-option label="英语" value="english" />
                  <el-option label="物理" value="physics" />
                  <el-option label="化学" value="chemistry" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="选择知识点">
                <el-select v-model="configForm.knowledgePoint" placeholder="选择知识点" clearable>
                  <el-option label="集合" value="set" />
                  <el-option label="函数" value="function" />
                  <el-option label="三角函数" value="trigonometric" />
                  <el-option label="数列" value="sequence" />
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
                  <el-option label="不限" value="all" />
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
          <el-tag :type="getDifficultyType(currentQuestion.difficulty)">
            {{ currentQuestion.difficulty }}
          </el-tag>
        </div>

        <div class="question-content">
          <p>{{ currentQuestion.content }}</p>
        </div>

        <div class="options-area" v-if="currentQuestion.type === '单选题'">
          <el-radio-group v-model="userAnswer" class="options-group">
            <el-radio
              v-for="(option, index) in currentQuestion.options"
              :key="index"
              :label="option.label"
              class="option-item"
            >
              {{ option.label }}. {{ option.content }}
            </el-radio>
          </el-radio-group>
        </div>

        <div class="answer-area" v-if="currentQuestion.type === '填空题'">
          <el-input v-model="userAnswer" placeholder="请输入答案" />
        </div>

        <div class="action-buttons">
          <el-button @click="prevQuestion" :disabled="currentIndex === 0">上一题</el-button>
          <el-button type="primary" @click="submitAnswer">提交答案</el-button>
          <el-button @click="nextQuestion" :disabled="currentIndex === questions.length - 1">下一题</el-button>
        </div>

        <div class="result-area" v-if="showResult">
          <el-alert
            :title="isCorrect ? '回答正确！' : '回答错误'"
            :type="isCorrect ? 'success' : 'error'"
            :description="currentQuestion.explanation"
            show-icon
            :closable="false"
          />
        </div>
      </div>

      <div class="empty-area" v-else>
        <el-empty description="请配置练习参数后开始练习" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { VideoPlay } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const configForm = reactive({
  subject: '',
  knowledgePoint: '',
  count: 10,
  mode: 'sequential',
  difficulty: 'all'
})

const questions = ref([])
const currentIndex = ref(0)
const userAnswer = ref('')
const showResult = ref(false)
const isCorrect = ref(false)

const currentQuestion = computed(() => questions.value[currentIndex.value])

const getDifficultyType = (difficulty) => {
  const types = {
    '简单': 'success',
    '中等': 'warning',
    '困难': 'danger'
  }
  return types[difficulty] || 'info'
}

const startPractice = () => {
  if (!configForm.subject) {
    ElMessage.warning('请选择科目')
    return
  }
  
  questions.value = [
    {
      id: 1,
      type: '单选题',
      difficulty: '简单',
      content: '已知集合A={1,2,3}，B={2,3,4}，则A∩B=',
      options: [
        { label: 'A', content: '{1,2,3,4}' },
        { label: 'B', content: '{2,3}' },
        { label: 'C', content: '{1,4}' },
        { label: 'D', content: '∅' }
      ],
      answer: 'B',
      explanation: '交集是两个集合共有的元素组成的集合，A和B共有的元素是2和3。'
    },
    {
      id: 2,
      type: '单选题',
      difficulty: '中等',
      content: '函数f(x)=x²-2x+1的最小值为',
      options: [
        { label: 'A', content: '-1' },
        { label: 'B', content: '0' },
        { label: 'C', content: '1' },
        { label: 'D', content: '2' }
      ],
      answer: 'B',
      explanation: 'f(x)=(x-1)²≥0，当x=1时取最小值0。'
    }
  ]
  
  currentIndex.value = 0
  userAnswer.value = ''
  showResult.value = false
  ElMessage.success('开始练习')
}

const submitAnswer = () => {
  if (!userAnswer.value) {
    ElMessage.warning('请先作答')
    return
  }
  
  isCorrect.value = userAnswer.value === currentQuestion.value.answer
  showResult.value = true
  
  if (isCorrect.value) {
    ElMessage.success('回答正确！')
  } else {
    ElMessage.error('回答错误')
  }
}

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    userAnswer.value = ''
    showResult.value = false
  }
}

const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    userAnswer.value = ''
    showResult.value = false
  }
}
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

.empty-area {
  padding: 60px 0;
}
</style>