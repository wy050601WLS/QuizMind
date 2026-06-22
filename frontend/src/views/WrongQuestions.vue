<template>
  <div class="wrong-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>错题本</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleReview">
              <el-icon><Refresh /></el-icon>
              错题重做
            </el-button>
            <el-button type="danger" @click="handleBatchDelete" :disabled="selectedRows.length === 0">
              <el-icon><Delete /></el-icon>
              批量删除
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
          <el-form-item label="知识点">
            <el-select v-model="filterForm.knowledge_point_id" placeholder="选择知识点" clearable>
              <el-option
                v-for="kp in knowledgePoints"
                :key="kp.id"
                :label="kp.name"
                :value="kp.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table
        :data="wrongQuestions"
        style="width: 100%"
        @selection-change="handleSelectionChange"
        v-loading="loading"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="科目" width="100">
          <template #default="{ row }">
            {{ getCategoryName(row.question?.category_id) }}
          </template>
        </el-table-column>
        <el-table-column label="知识点" width="120">
          <template #default="{ row }">
            {{ getKnowledgePointName(row.question?.knowledge_point_id) }}
          </template>
        </el-table-column>
        <el-table-column label="题目内容" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.question?.content || '未知题目' }}
          </template>
        </el-table-column>
        <el-table-column prop="my_answer" label="我的答案" width="100" />
        <el-table-column label="正确答案" width="100">
          <template #default="{ row }">
            {{ row.question?.answer || '未知' }}
          </template>
        </el-table-column>
        <el-table-column prop="error_count" label="错误次数" width="100">
          <template #default="{ row }">
            <el-tag type="danger">{{ row.error_count }}次</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="最近错误时间" width="150">
          <template #default="{ row }">
            {{ formatTime(row.last_error_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleReviewOne(row)">重做</el-button>
            <el-button size="small" @click="handleViewAnalysis(row)">查看解析</el-button>
            <el-button size="small" type="success" @click="handleAiAnalysis(row)">
              AI分析
            </el-button>
            <el-button size="small" @click="handleMark(row)">
              {{ row.is_marked ? '取消标记' : '标记' }}
            </el-button>
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

    <el-dialog v-model="analysisVisible" title="题目解析" width="600px">
      <div class="analysis-content" v-if="currentWrongQuestion">
        <h4>题目内容</h4>
        <p>{{ currentWrongQuestion.question?.content }}</p>
        
        <h4>我的答案</h4>
        <p :class="{ 'error-answer': !isAnswerCorrect }">{{ currentWrongQuestion.my_answer }}</p>
        
        <h4>正确答案</h4>
        <p class="correct-answer">{{ currentWrongQuestion.question?.answer }}</p>
        
        <h4>解析</h4>
        <p>{{ currentWrongQuestion.question?.explanation || '暂无解析' }}</p>
        
        <h4>知识点</h4>
        <el-tag>{{ getKnowledgePointName(currentWrongQuestion.question?.knowledge_point_id) }}</el-tag>
      </div>
      <template #footer>
        <el-button @click="analysisVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleReviewOne(currentWrongQuestion)">重做此题</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="aiAnalysisVisible" title="AI智能分析" width="700px">
      <div class="ai-analysis-content" v-loading="aiAnalysisLoading">
        <template v-if="aiAnalysisResult">
          <h4>错误原因</h4>
          <p>{{ aiAnalysisResult.error_reason }}</p>
          
          <h4>涉及知识点</h4>
          <div class="knowledge-tags">
            <el-tag v-for="(point, index) in aiAnalysisResult.knowledge_points" :key="index" type="info">
              {{ point }}
            </el-tag>
          </div>
          
          <h4>易错点提醒</h4>
          <p>{{ aiAnalysisResult.mistake_tips }}</p>
          
          <h4>学习建议</h4>
          <ul>
            <li v-for="(suggestion, index) in aiAnalysisResult.suggestions" :key="index">
              {{ suggestion }}
            </li>
          </ul>
        </template>
        <el-empty v-else-if="!aiAnalysisLoading" description="暂无AI分析结果" />
      </div>
      <template #footer>
        <el-button @click="aiAnalysisVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Refresh, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import {
  getWrongQuestions,
  markWrongQuestion,
  deleteWrongQuestion,
  getCategories,
  getKnowledgePoints,
  aiAnalyzeWrongQuestion
} from '../api'

const router = useRouter()
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const analysisVisible = ref(false)
const aiAnalysisVisible = ref(false)
const aiAnalysisLoading = ref(false)
const aiAnalysisResult = ref(null)
const currentWrongQuestion = ref(null)
const selectedRows = ref([])

const filterForm = reactive({
  subject: '',
  knowledge_point_id: null
})

const wrongQuestions = ref([])
const categories = ref([])
const knowledgePoints = ref([])

const isAnswerCorrect = ref(false)

const getCategoryName = (categoryId) => {
  const cat = categories.value.find(c => c.id === categoryId)
  return cat ? cat.name : '未知'
}

const getKnowledgePointName = (kpId) => {
  const kp = knowledgePoints.value.find(k => k.id === kpId)
  return kp ? kp.name : '未知'
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

const fetchWrongQuestions = async () => {
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
    if (filterForm.knowledge_point_id) {
      params.knowledge_point_id = filterForm.knowledge_point_id
    }

    const res = await getWrongQuestions(params)
    wrongQuestions.value = res.data.wrong_questions || []
    total.value = res.total || 0
  } catch (error) {
    console.error('获取错题列表失败:', error)
    ElMessage.error('获取错题列表失败')
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
  fetchWrongQuestions()
}

const handleReset = () => {
  filterForm.subject = ''
  filterForm.knowledge_point_id = null
  handleSearch()
}

const handleSelectionChange = (val) => {
  selectedRows.value = val
}

const handleReview = () => {
  if (wrongQuestions.value.length === 0) {
    ElMessage.info('暂无错题需要重做')
    return
  }
  router.push('/practice')
}

const handleReviewOne = (row) => {
  if (row && row.question_id) {
    router.push({
      path: '/practice',
      query: { question_id: row.question_id }
    })
  }
}

const handleViewAnalysis = (row) => {
  currentWrongQuestion.value = row
  isAnswerCorrect.value = row.my_answer === row.question?.answer
  analysisVisible.value = true
}

const handleAiAnalysis = async (row) => {
  aiAnalysisVisible.value = true
  aiAnalysisLoading.value = true
  aiAnalysisResult.value = null
  
  try {
    const res = await aiAnalyzeWrongQuestion({
      question_id: row.question_id,
      user_answer: row.my_answer
    })
    
    if (res && res.data) {
      aiAnalysisResult.value = res.data
    }
  } catch (error) {
    ElMessage.error('AI分析失败：' + (error.message || '未知错误'))
  } finally {
    aiAnalysisLoading.value = false
  }
}

const handleMark = async (row) => {
  try {
    await markWrongQuestion(row.id)
    ElMessage.success(row.is_marked ? '已取消标记' : '已标记')
    fetchWrongQuestions()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除该错题记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteWrongQuestion(row.id)
      ElMessage.success('删除成功')
      fetchWrongQuestions()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

const handleBatchDelete = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要删除的记录')
    return
  }
  ElMessageBox.confirm(`确定删除选中的${selectedRows.value.length}条记录吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      for (const row of selectedRows.value) {
        await deleteWrongQuestion(row.id)
      }
      ElMessage.success('批量删除成功')
      fetchWrongQuestions()
    } catch (error) {
      ElMessage.error('批量删除失败')
    }
  }).catch(() => {})
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchWrongQuestions()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchWrongQuestions()
}

onMounted(() => {
  fetchCategories()
  fetchKnowledgePoints()
  fetchWrongQuestions()
})
</script>

<style scoped>
.wrong-container {
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

.analysis-content h4 {
  margin: 15px 0 8px 0;
  color: #303133;
}

.analysis-content p {
  line-height: 1.8;
  color: #606266;
}

.error-answer {
  color: #f56c6c;
  font-weight: bold;
}

.correct-answer {
  color: #67c23a;
  font-weight: bold;
}

.ai-analysis-content {
  min-height: 200px;
}

.ai-analysis-content h4 {
  margin: 15px 0 8px 0;
  color: #303133;
}

.ai-analysis-content p {
  line-height: 1.8;
  color: #606266;
}

.knowledge-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 10px 0;
}

.ai-analysis-content ul {
  margin: 10px 0 10px 20px;
}

.ai-analysis-content li {
  margin: 5px 0;
  line-height: 1.6;
}
</style>