<template>
  <div class="ai-question-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>AI智能出题</span>
          <el-tag :type="aiStatus === 'healthy' ? 'success' : 'danger'">
            {{ aiStatus === 'healthy' ? 'AI服务正常' : 'AI服务不可用' }}
          </el-tag>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
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
            <el-form-item label="知识点" prop="knowledge_point">
              <el-input v-model="form.knowledge_point" placeholder="请输入知识点" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="题型" prop="question_type">
              <el-select v-model="form.question_type" placeholder="选择题型">
                <el-option label="单选题" value="single" />
                <el-option label="多选题" value="multiple" />
                <el-option label="判断题" value="judge" />
                <el-option label="填空题" value="blank" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="难度" prop="difficulty">
              <el-select v-model="form.difficulty" placeholder="选择难度">
                <el-option label="简单" value="easy" />
                <el-option label="中等" value="medium" />
                <el-option label="困难" value="hard" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="数量" prop="count">
              <el-input-number v-model="form.count" :min="1" :max="10" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item>
              <el-button type="primary" @click="handleGenerate" :loading="loading">
                <el-icon><MagicStick /></el-icon>
                AI生成题目
              </el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <el-card v-if="generatedQuestions.length > 0" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>生成结果</span>
          <el-button type="primary" size="small" @click="handleSaveAll">
            <el-icon><Download /></el-icon>
            全部保存到题库
          </el-button>
        </div>
      </template>

      <div v-for="(question, index) in generatedQuestions" :key="index" class="question-item">
        <div class="question-header">
          <span class="question-index">题目 {{ index + 1 }}</span>
          <el-button type="primary" size="small" @click="handleSaveOne(question)">
            保存到题库
          </el-button>
        </div>
        <div class="question-content">
          <p><strong>题目：</strong>{{ question.content }}</p>
        </div>
        <div class="question-options" v-if="question.options && question.options.length > 0">
          <p><strong>选项：</strong></p>
          <ul>
            <li v-for="(option, optIndex) in question.options" :key="optIndex">
              {{ option }}
            </li>
          </ul>
        </div>
        <div class="question-answer">
          <p><strong>答案：</strong>{{ question.answer }}</p>
        </div>
        <div class="question-explanation" v-if="question.explanation">
          <p><strong>解析：</strong>{{ question.explanation }}</p>
        </div>
        <el-divider v-if="index < generatedQuestions.length - 1" />
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
import { MagicStick, Download } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  aiHealthCheck,
  aiGenerateQuestion,
  getCategories,
  createQuestion
} from '../api'

const loading = ref(false)
const aiStatus = ref('unknown')
const categories = ref([])
const generatedQuestions = ref([])
const rawResponse = ref('')
const formRef = ref(null)

const form = reactive({
  subject: '',
  knowledge_point: '',
  question_type: 'single',
  difficulty: 'medium',
  count: 1
})

const rules = {
  subject: [{ required: true, message: '请选择科目', trigger: 'change' }],
  knowledge_point: [{ required: true, message: '请输入知识点', trigger: 'blur' }],
  question_type: [{ required: true, message: '请选择题型', trigger: 'change' }],
  difficulty: [{ required: true, message: '请选择难度', trigger: 'change' }]
}

const fetchCategories = async () => {
  try {
    const res = await getCategories()
    categories.value = res || []
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

const checkAiStatus = async () => {
  try {
    const res = await aiHealthCheck()
    if (res && res.data) {
      const services = res.data
      const hasHealthy = Object.values(services).some(v => v === true)
      aiStatus.value = hasHealthy ? 'healthy' : 'unhealthy'
    }
  } catch (error) {
    aiStatus.value = 'unhealthy'
  }
}

const handleGenerate = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    generatedQuestions.value = []
    rawResponse.value = ''
    
    try {
      const res = await aiGenerateQuestion(form)
      
      if (res && res.data) {
        if (res.data.questions) {
          generatedQuestions.value = res.data.questions
          ElMessage.success(`成功生成 ${generatedQuestions.value.length} 道题目`)
        } else if (res.data.raw_response) {
          rawResponse.value = res.data.raw_response
          ElMessage.info('AI返回了非结构化响应，请查看原始响应')
        }
      }
    } catch (error) {
      ElMessage.error('AI生成题目失败：' + (error.message || '未知错误'))
    } finally {
      loading.value = false
    }
  })
}

const handleSaveOne = async (question) => {
  try {
    const data = {
      content: question.content,
      question_type: form.question_type,
      difficulty: form.difficulty,
      options: question.options ? JSON.stringify(question.options.map((opt, index) => ({
        label: String.fromCharCode(65 + index),
        content: opt
      }))) : null,
      answer: question.answer,
      explanation: question.explanation || '',
      category_id: categories.value.find(c => c.name === form.subject)?.id || 1,
      knowledge_point_id: 1
    }
    
    await createQuestion(data)
    ElMessage.success('题目已保存到题库')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const handleSaveAll = async () => {
  ElMessageBox.confirm(`确定将 ${generatedQuestions.value.length} 道题目保存到题库吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info'
  }).then(async () => {
    let successCount = 0
    for (const question of generatedQuestions.value) {
      try {
        await handleSaveOne(question)
        successCount++
      } catch (error) {
        console.error('保存题目失败:', error)
      }
    }
    ElMessage.success(`成功保存 ${successCount} 道题目到题库`)
  }).catch(() => {})
}

onMounted(() => {
  fetchCategories()
  checkAiStatus()
})
</script>

<style scoped>
.ai-question-container {
  padding: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question-item {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 15px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.question-index {
  font-weight: bold;
  color: #409eff;
}

.question-content p,
.question-options p,
.question-answer p,
.question-explanation p {
  margin: 8px 0;
  line-height: 1.6;
}

.question-options ul {
  margin: 5px 0 5px 20px;
}

.question-options li {
  margin: 5px 0;
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