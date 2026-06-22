<template>
  <div class="api-test-container">
    <el-card>
      <template #header>
        <span>API联调测试</span>
      </template>
      
      <el-button type="primary" @click="testHealthCheck" :loading="loading">
        测试健康检查
      </el-button>
      
      <el-button @click="testGetQuestions" :loading="loading">
        测试获取题目
      </el-button>
      
      <el-button @click="testGetCategories" :loading="loading">
        测试获取分类
      </el-button>
      
      <div class="result-area" v-if="result">
        <h4>测试结果：</h4>
        <pre>{{ JSON.stringify(result, null, 2) }}</pre>
      </div>
      
      <div class="error-area" v-if="error">
        <h4>错误信息：</h4>
        <pre>{{ error }}</pre>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { healthCheck, getQuestions, getCategories } from '../api'

const loading = ref(false)
const result = ref(null)
const error = ref(null)

const testHealthCheck = async () => {
  loading.value = true
  result.value = null
  error.value = null
  
  try {
    const res = await healthCheck()
    result.value = res
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const testGetQuestions = async () => {
  loading.value = true
  result.value = null
  error.value = null
  
  try {
    const res = await getQuestions({ page: 1, page_size: 10 })
    result.value = res
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const testGetCategories = async () => {
  loading.value = true
  result.value = null
  error.value = null
  
  try {
    const res = await getCategories()
    result.value = res
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.api-test-container {
  padding: 20px;
}

.result-area,
.error-area {
  margin-top: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.result-area pre,
.error-area pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.error-area {
  background-color: #fef0f0;
  color: #f56c6c;
}
</style>