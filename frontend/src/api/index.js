import request from '../utils/request'

export function healthCheck() {
  return request({
    url: '/health',
    method: 'get'
  })
}

export function getQuestions(params) {
  return request({
    url: '/questions',
    method: 'get',
    params
  })
}

export function getQuestion(id) {
  return request({
    url: `/questions/${id}`,
    method: 'get'
  })
}

export function createQuestion(data) {
  return request({
    url: '/questions',
    method: 'post',
    data
  })
}

export function updateQuestion(id, data) {
  return request({
    url: `/questions/${id}`,
    method: 'put',
    data
  })
}

export function deleteQuestion(id) {
  return request({
    url: `/questions/${id}`,
    method: 'delete'
  })
}

export function getCategories() {
  return request({
    url: '/categories',
    method: 'get'
  })
}

export function getKnowledgePoints() {
  return request({
    url: '/knowledge-points',
    method: 'get'
  })
}

export function submitAnswer(data) {
  return request({
    url: '/practice/submit',
    method: 'post',
    data
  })
}

export function getPracticeRecords(params) {
  return request({
    url: '/practice/records',
    method: 'get',
    params
  })
}

export function getPracticeStatistics(params) {
  return request({
    url: '/practice/statistics',
    method: 'get',
    params
  })
}

export function getWrongQuestions(params) {
  return request({
    url: '/wrong-questions',
    method: 'get',
    params
  })
}

export function markWrongQuestion(id) {
  return request({
    url: `/wrong-questions/${id}/mark`,
    method: 'put'
  })
}

export function deleteWrongQuestion(id) {
  return request({
    url: `/wrong-questions/${id}`,
    method: 'delete'
  })
}

// AI相关接口
export function aiHealthCheck() {
  return request({
    url: '/ai/health',
    method: 'get'
  })
}

export function aiGenerateQuestion(data) {
  return request({
    url: '/ai/generate-question',
    method: 'post',
    data
  })
}

export function aiAnalyzeWrongQuestion(data) {
  return request({
    url: '/ai/analyze-wrong-question',
    method: 'post',
    data
  })
}

export function aiGenerateSuggestions() {
  return request({
    url: '/ai/generate-suggestions',
    method: 'post'
  })
}

export function aiGenerateExam(data) {
  return request({
    url: '/ai/generate-exam',
    method: 'post',
    data
  })
}