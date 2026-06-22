<template>
  <div class="questions-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>题库管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新增题目
            </el-button>
            <el-button @click="handleImport">
              <el-icon><Upload /></el-icon>
              批量导入
            </el-button>
          </div>
        </div>
      </template>

      <div class="filter-container">
        <el-form :inline="true" :model="filterForm">
          <el-form-item label="科目">
            <el-select v-model="filterForm.subject" placeholder="选择科目" clearable>
              <el-option
                v-for="cat in categories"
                :key="cat.id"
                :label="cat.name"
                :value="cat.name"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="题型">
            <el-select v-model="filterForm.question_type" placeholder="选择题型" clearable>
              <el-option label="单选题" value="single" />
              <el-option label="多选题" value="multiple" />
              <el-option label="判断题" value="judge" />
              <el-option label="填空题" value="blank" />
            </el-select>
          </el-form-item>
          <el-form-item label="难度">
            <el-select v-model="filterForm.difficulty" placeholder="选择难度" clearable>
              <el-option label="简单" value="easy" />
              <el-option label="中等" value="medium" />
              <el-option label="困难" value="hard" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table :data="questions" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="科目" width="100">
          <template #default="{ row }">
            {{ getCategoryName(row.category_id) }}
          </template>
        </el-table-column>
        <el-table-column label="题型" width="100">
          <template #default="{ row }">
            {{ getQuestionTypeLabel(row.question_type) }}
          </template>
        </el-table-column>
        <el-table-column label="难度" width="80">
          <template #default="{ row }">
            <el-tag :type="getDifficultyType(row.difficulty)">
              {{ getDifficultyLabel(row.difficulty) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="题目内容" show-overflow-tooltip />
        <el-table-column label="知识点" width="120">
          <template #default="{ row }">
            {{ getKnowledgePointName(row.knowledge_point_id) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑题目对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="questionFormRef"
        :model="questionForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="科目" prop="category_id">
          <el-select v-model="questionForm.category_id" placeholder="选择科目">
            <el-option
              v-for="cat in categories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="知识点" prop="knowledge_point_id">
          <el-select v-model="questionForm.knowledge_point_id" placeholder="选择知识点">
            <el-option
              v-for="kp in filteredKnowledgePoints"
              :key="kp.id"
              :label="kp.name"
              :value="kp.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="题型" prop="question_type">
          <el-select v-model="questionForm.question_type" placeholder="选择题型">
            <el-option label="单选题" value="single" />
            <el-option label="多选题" value="multiple" />
            <el-option label="判断题" value="judge" />
            <el-option label="填空题" value="blank" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度" prop="difficulty">
          <el-select v-model="questionForm.difficulty" placeholder="选择难度">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
        </el-form-item>
        <el-form-item label="题目内容" prop="content">
          <el-input
            v-model="questionForm.content"
            type="textarea"
            :rows="3"
            placeholder="请输入题目内容"
          />
        </el-form-item>
        <el-form-item label="选项" v-if="questionForm.question_type === 'single' || questionForm.question_type === 'multiple'">
          <div v-for="(option, index) in questionForm.options" :key="index" class="option-item">
            <el-input v-model="option.label" placeholder="标签" style="width: 60px" />
            <el-input v-model="option.content" placeholder="选项内容" style="flex: 1; margin: 0 10px" />
            <el-button type="danger" size="small" @click="removeOption(index)">删除</el-button>
          </div>
          <el-button type="primary" size="small" @click="addOption">添加选项</el-button>
        </el-form-item>
        <el-form-item label="正确答案" prop="answer">
          <el-input v-model="questionForm.answer" placeholder="请输入正确答案" />
        </el-form-item>
        <el-form-item label="解析">
          <el-input
            v-model="questionForm.explanation"
            type="textarea"
            :rows="2"
            placeholder="请输入解析"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { Plus, Upload } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getQuestions,
  createQuestion,
  updateQuestion,
  deleteQuestion,
  getCategories,
  getKnowledgePoints
} from '../api'

const loading = ref(false)
const submitLoading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('新增题目')
const questionFormRef = ref(null)
const editingId = ref(null)

const filterForm = reactive({
  subject: '',
  question_type: '',
  difficulty: ''
})

const questions = ref([])
const categories = ref([])
const knowledgePoints = ref([])

const questionForm = reactive({
  category_id: null,
  knowledge_point_id: null,
  question_type: 'single',
  difficulty: 'easy',
  content: '',
  options: [
    { label: 'A', content: '' },
    { label: 'B', content: '' },
    { label: 'C', content: '' },
    { label: 'D', content: '' }
  ],
  answer: '',
  explanation: ''
})

const rules = {
  category_id: [{ required: true, message: '请选择科目', trigger: 'change' }],
  knowledge_point_id: [{ required: true, message: '请选择知识点', trigger: 'change' }],
  question_type: [{ required: true, message: '请选择题型', trigger: 'change' }],
  difficulty: [{ required: true, message: '请选择难度', trigger: 'change' }],
  content: [{ required: true, message: '请输入题目内容', trigger: 'blur' }],
  answer: [{ required: true, message: '请输入正确答案', trigger: 'blur' }]
}

const filteredKnowledgePoints = computed(() => {
  if (!questionForm.category_id) return knowledgePoints.value
  return knowledgePoints.value.filter(kp => kp.category_id === questionForm.category_id)
})

const getCategoryName = (categoryId) => {
  const cat = categories.value.find(c => c.id === categoryId)
  return cat ? cat.name : '未知'
}

const getKnowledgePointName = (kpId) => {
  const kp = knowledgePoints.value.find(k => k.id === kpId)
  return kp ? kp.name : '未知'
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

const getDifficultyLabel = (difficulty) => {
  const labels = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return labels[difficulty] || difficulty
}

const getDifficultyType = (difficulty) => {
  const types = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger'
  }
  return types[difficulty] || 'info'
}

const fetchQuestions = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (filterForm.subject) {
      const cat = categories.value.find(c => c.name === filterForm.subject)
      if (cat) params.subject = cat.name
    }
    if (filterForm.question_type) params.question_type = filterForm.question_type
    if (filterForm.difficulty) params.difficulty = filterForm.difficulty

    const res = await getQuestions(params)
    questions.value = res.data.questions || []
    total.value = res.total || 0
  } catch (error) {
    console.error('获取题目列表失败:', error)
    ElMessage.error('获取题目列表失败')
  } finally {
    loading.value = false
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
  } catch (error) {
    console.error('获取知识点失败:', error)
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchQuestions()
}

const handleReset = () => {
  filterForm.subject = ''
  filterForm.question_type = ''
  filterForm.difficulty = ''
  handleSearch()
}

const handleAdd = () => {
  dialogTitle.value = '新增题目'
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑题目'
  editingId.value = row.id
  Object.assign(questionForm, {
    category_id: row.category_id,
    knowledge_point_id: row.knowledge_point_id,
    question_type: row.question_type,
    difficulty: row.difficulty,
    content: row.content,
    options: row.options ? (typeof row.options === 'string' ? JSON.parse(row.options) : row.options) : [
      { label: 'A', content: '' },
      { label: 'B', content: '' },
      { label: 'C', content: '' },
      { label: 'D', content: '' }
    ],
    answer: row.answer,
    explanation: row.explanation || ''
  })
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除该题目吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteQuestion(row.id)
      ElMessage.success('删除成功')
      fetchQuestions()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

const handleSubmit = async () => {
  if (!questionFormRef.value) return
  
  await questionFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitLoading.value = true
    try {
      const data = {
        ...questionForm,
        options: JSON.stringify(questionForm.options)
      }
      
      if (editingId.value) {
        await updateQuestion(editingId.value, data)
        ElMessage.success('更新成功')
      } else {
        await createQuestion(data)
        ElMessage.success('创建成功')
      }
      
      dialogVisible.value = false
      fetchQuestions()
    } catch (error) {
      ElMessage.error(editingId.value ? '更新失败' : '创建失败')
    } finally {
      submitLoading.value = false
    }
  })
}

const handleDialogClose = () => {
  if (questionFormRef.value) {
    questionFormRef.value.resetFields()
  }
}

const resetForm = () => {
  Object.assign(questionForm, {
    category_id: null,
    knowledge_point_id: null,
    question_type: 'single',
    difficulty: 'easy',
    content: '',
    options: [
      { label: 'A', content: '' },
      { label: 'B', content: '' },
      { label: 'C', content: '' },
      { label: 'D', content: '' }
    ],
    answer: '',
    explanation: ''
  })
}

const addOption = () => {
  const labels = ['A', 'B', 'C', 'D', 'E', 'F']
  const nextLabel = labels[questionForm.options.length] || String.fromCharCode(65 + questionForm.options.length)
  questionForm.options.push({ label: nextLabel, content: '' })
}

const removeOption = (index) => {
  if (questionForm.options.length <= 2) {
    ElMessage.warning('至少需要2个选项')
    return
  }
  questionForm.options.splice(index, 1)
}

const handleImport = () => {
  ElMessage.info('批量导入功能开发中...')
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchQuestions()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchQuestions()
}

onMounted(() => {
  fetchCategories()
  fetchKnowledgePoints()
  fetchQuestions()
})
</script>

<style scoped>
.questions-container {
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

.filter-container {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
</style>