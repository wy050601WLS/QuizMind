<template>
  <div class="page-header">
    <div class="header-left">
      <h2>{{ title }}</h2>
      <span class="subtitle" v-if="subtitle">{{ subtitle }}</span>
    </div>
    <div class="header-right">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.header-left h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.subtitle {
  font-size: 14px;
  color: #909399;
}

.header-right {
  display: flex;
  gap: 10px;
}
</style>