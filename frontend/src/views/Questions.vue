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
              <el-option label="数学" value="math" />
              <el-option label="英语" value="english" />
              <el-option label="物理" value="physics" />
              <el-option label="化学" value="chemistry" />
            </el-select>
          </el-form-item>
          <el-form-item label="题型">
            <el-select v-model="filterForm.type" placeholder="选择题型" clearable>
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
        <el-table-column prop="subject" label="科目" width="100" />
        <el-table-column prop="type" label="题型" width="100" />
        <el-table-column prop="difficulty" label="难度" width="80">
          <template #default="{ row }">
            <el-tag :type="getDifficultyType(row.difficulty)">
              {{ row.difficulty }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="题目内容" show-overflow-tooltip />
        <el-table-column prop="knowledgePoint" label="知识点" width="120" />
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
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Plus, Upload } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

const filterForm = reactive({
  subject: '',
  type: '',
  difficulty: ''
})

const questions = ref([
  { id: 1, subject: '数学', type: '单选题', difficulty: '简单', content: '已知集合A={1,2,3}，B={2,3,4}，则A∩B=', knowledgePoint: '集合' },
  { id: 2, subject: '数学', type: '单选题', difficulty: '中等', content: '函数f(x)=x²-2x+1的最小值为', knowledgePoint: '函数' },
  { id: 3, subject: '英语', type: '单选题', difficulty: '简单', content: 'I ___ to school by bus every day.', knowledgePoint: '时态' },
  { id: 4, subject: '物理', type: '判断题', difficulty: '困难', content: '力是改变物体运动状态的原因', knowledgePoint: '牛顿定律' }
])

const getDifficultyType = (difficulty) => {
  const types = {
    '简单': 'success',
    '中等': 'warning',
    '困难': 'danger'
  }
  return types[difficulty] || 'info'
}

const handleAdd = () => {
  ElMessage.info('新增题目功能（待实现）')
}

const handleImport = () => {
  ElMessage.info('批量导入功能（待实现）')
}

const handleSearch = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
}

const handleReset = () => {
  filterForm.subject = ''
  filterForm.type = ''
  filterForm.difficulty = ''
}

const handleEdit = (row) => {
  ElMessage.info(`编辑题目：${row.id}`)
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除该题目吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
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
</style>