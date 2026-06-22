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
            <el-button type="danger" @click="handleBatchDelete">
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
              <el-option label="数学" value="math" />
              <el-option label="英语" value="english" />
              <el-option label="物理" value="physics" />
            </el-select>
          </el-form-item>
          <el-form-item label="知识点">
            <el-select v-model="filterForm.knowledgePoint" placeholder="选择知识点" clearable>
              <el-option label="集合" value="set" />
              <el-option label="函数" value="function" />
              <el-option label="三角函数" value="trigonometric" />
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
        <el-table-column prop="subject" label="科目" width="100" />
        <el-table-column prop="knowledgePoint" label="知识点" width="120" />
        <el-table-column prop="content" label="题目内容" show-overflow-tooltip />
        <el-table-column prop="myAnswer" label="我的答案" width="100" />
        <el-table-column prop="correctAnswer" label="正确答案" width="100" />
        <el-table-column prop="errorCount" label="错误次数" width="100">
          <template #default="{ row }">
            <el-tag type="danger">{{ row.errorCount }}次</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastErrorTime" label="最近错误时间" width="150" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleReviewOne(row)">重做</el-button>
            <el-button size="small" @click="handleViewAnalysis(row)">查看解析</el-button>
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
      <div class="analysis-content" v-if="currentQuestion">
        <h4>题目内容</h4>
        <p>{{ currentQuestion.content }}</p>
        
        <h4>正确答案</h4>
        <p>{{ currentQuestion.correctAnswer }}</p>
        
        <h4>解析</h4>
        <p>{{ currentQuestion.analysis }}</p>
        
        <h4>知识点</h4>
        <el-tag>{{ currentQuestion.knowledgePoint }}</el-tag>
      </div>
      <template #footer>
        <el-button @click="analysisVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleReviewOne(currentQuestion)">重做此题</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Refresh, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(50)
const analysisVisible = ref(false)
const currentQuestion = ref(null)
const selectedRows = ref([])

const filterForm = reactive({
  subject: '',
  knowledgePoint: ''
})

const wrongQuestions = ref([
  {
    id: 1,
    subject: '数学',
    knowledgePoint: '集合',
    content: '已知集合A={1,2,3}，B={2,3,4}，则A∩B=',
    myAnswer: 'A',
    correctAnswer: 'B',
    errorCount: 3,
    lastErrorTime: '2026-06-22 14:30',
    analysis: '交集是两个集合共有的元素组成的集合，A和B共有的元素是2和3，所以A∩B={2,3}。'
  },
  {
    id: 2,
    subject: '数学',
    knowledgePoint: '函数',
    content: '函数f(x)=x²-2x+1的最小值为',
    myAnswer: 'C',
    correctAnswer: 'B',
    errorCount: 2,
    lastErrorTime: '2026-06-21 10:15',
    analysis: 'f(x)=(x-1)²≥0，当x=1时取最小值0。这是一个完全平方式，最小值为0。'
  },
  {
    id: 3,
    subject: '英语',
    knowledgePoint: '时态',
    content: 'I ___ to school by bus every day.',
    myAnswer: 'go',
    correctAnswer: 'go',
    errorCount: 1,
    lastErrorTime: '2026-06-20 16:45',
    analysis: 'every day表示经常性动作，用一般现在时。主语是I，动词用原形go。'
  }
])

const handleSearch = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
}

const handleReset = () => {
  filterForm.subject = ''
  filterForm.knowledgePoint = ''
}

const handleSelectionChange = (val) => {
  selectedRows.value = val
}

const handleReview = () => {
  ElMessage.info('错题重做功能（待实现）')
}

const handleReviewOne = (row) => {
  ElMessage.info(`重做题目：${row.id}`)
}

const handleViewAnalysis = (row) => {
  currentQuestion.value = row
  analysisVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除该错题记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
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
  }).then(() => {
    ElMessage.success('批量删除成功')
  }).catch(() => {})
}

const handleSizeChange = (val) => {
  pageSize.value = val
}

const handleCurrentChange = (val) => {
  currentPage.value = val
}
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
</style>