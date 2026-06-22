<template>
  <div class="exam-paper-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>AI模拟组卷</span>
          <el-button type="primary" @click="handleGenerate" :loading="loading">
            <el-icon><Document /></el-icon>
            生成试卷
          </el-button>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="科目" prop="subject">
              <el-select v-model="form.subject" placeholder="选择科目">
                <el-option
                  v-for="cat in categories"
                  :key="cat.id"
                  :label="cat.name"
                  :value="cat.name"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="考试范围" prop="scope">
              <el-input v-model="form.scope" placeholder="请输入考试范围" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="总分" prop="total_score">
              <el-input-number v-model="form.total_score" :min="50" :max="200" :step="10" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="题型分布">
              <div class="distribution-item">
                <span>单选题：</span>
                <el-input-number v-model="form.question_types.single" :min="0" :max="100" size="small" />
                <span>%</span>
              </div>
              <div class="distribution-item">
                <span>多选题：</span>
                <el-input-number v-model="form.question_types.multiple" :min="0" :max="100" size="small" />
                <span>%</span>
              </div>
              <div class="distribution-item">
                <span>判断题：</span>
                <el-input-number v-model="form.question_types.judge" :min="0" :max="100" size="small" />
                <span>%</span>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="难度分布">
              <div class="distribution-item">
                <span>简单：</span>
                <el-input-number v-model="form.difficulty_distribution.easy" :min="0" :max="100" size="small" />
                <span>%</span>
              </div>
              <div class="distribution-item">
                <span>中等：</span>
                <el-input-number v-model="form.difficulty_distribution.medium" :min="0" :max="100" size="small" />
                <span>%</span>
              </div>
              <div class="distribution-item">
                <span>困难：</span>
                <el-input-number v-model="form.difficulty_distribution.hard" :min="0" :max="100" size="small" />
                <span>%</span>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <el-card v-if="examPaper" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>{{ examPaper.title || 'AI生成试卷' }}</span>
          <div>
            <el-tag type="info">总分：{{ examPaper.total_score || form.total_score }}分</el-tag>
          </div>
        </div>
      </template>

      <div class="exam-content">
        <div v-for="(question, index) in examPaper.questions" :key="index" class="exam-question">
          <div class="question-header">
            <span class="question-index">{{ index + 1 }}.</span>
            <span class="question-type">[{{ getQuestionTypeLabel(question.type) }}]</span>
            <span class="question-score">（{{ question.score || 0 }}分）</span>
          </div>
          <div class="question-content">
            <p>{{ question.content }}</p>
          </div>
          <div class="question-options" v-if="question.options && question.options.length > 0">
            <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option-item">
              {{ String.fromCharCode(65 + optIndex) }}. {{ option }}
            </div>
          </div>
          <div class="question-answer" v-if="showAnswer">
            <p><strong>答案：</strong>{{ question.answer }}</p>
            <p v-if="question.explanation"><strong>解析：</strong>{{ question.explanation }}</p>
          </div>
          <el-divider v-if="index < examPaper.questions.length - 1" />
        </div>
      </div>

      <div class="exam-footer">
        <el-button @click="showAnswer = !showAnswer">
          {{ showAnswer ? '隐藏答案' : '显示答案' }}
        </el-button>
        <el-button type="primary" @click="handleSaveExam">
          <el-icon><Download /></el-icon>
          保存试卷
        </el-button>
      </div>
    </el-card>

    <el-card v-if="rawResponse" style="margin-top: 20px">
      <template #header>
        <span>AI原始响应</span>
      </template>
      <pre class="raw-response">{{ rawResponse }}</pre>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Document, Download } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { aiGenerateExam, getCategories } from '../api'

const loading = ref(false)
const showAnswer = ref(false)
const categories = ref([])
const examPaper = ref(null)
const rawResponse = ref('')
const formRef = ref(null)

const form = reactive({
  subject: '',
  scope: '',
  total_score: 100,
  question_types: {
    single: 60,
    multiple: 20,
    judge: 20
  },
  difficulty_distribution: {
    easy: 30,
    medium: 50,
    hard: 20
  }
})

const rules = {
  subject: [{ required: true, message: '请选择科目', trigger: 'change' }],
  scope: [{ required: true, message: '请输入考试范围', trigger: 'blur' }]
}

const getQuestionTypeLabel = (type) => {
  const types = {
    single: '单选题',
    multiple: '多选题',
    judge: '判断题',
    blank: '填空题'
  }
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

const handleGenerate = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    examPaper.value = null
    rawResponse.value = ''
    
    try {
      const res = await aiGenerateExam(form)
      
      if (res && res.data) {
        if (res.data.questions) {
          examPaper.value = res.data
          ElMessage.success('试卷生成成功')
        } else if (res.data.raw_response) {
          rawResponse.value = res.data.raw_response
          ElMessage.info('AI返回了非结构化响应，请查看原始响应')
        }
      }
    } catch (error) {
      ElMessage.error('生成试卷失败：' + (error.message || '未知错误'))
    } finally {
      loading.value = false
    }
  })
}

const handleSaveExam = () => {
  ElMessage.success('试卷保存功能开发中...')
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.exam-paper-container {
  padding: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.distribution-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.exam-content {
  padding: 20px;
}

.exam-question {
  margin-bottom: 20px;
}

.question-header {
  margin-bottom: 10px;
}

.question-index {
  font-weight: bold;
  margin-right: 5px;
}

.question-type {
  color: #409eff;
  margin-right: 5px;
}

.question-score {
  color: #909399;
}

.question-content p {
  line-height: 1.8;
  margin: 10px 0;
}

.question-options {
  margin: 10px 0 10px 20px;
}

.option-item {
  margin: 5px 0;
  line-height: 1.6;
}

.question-answer {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.question-answer p {
  margin: 5px 0;
  line-height: 1.6;
}

.exam-footer {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.raw-response {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: monospace;
  font-size: 14px;
  line-height: 1.6;
}
</style>