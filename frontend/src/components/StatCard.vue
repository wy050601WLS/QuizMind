<template>
  <el-card class="stat-card" shadow="hover">
    <div class="stat-content">
      <div class="stat-icon" :style="{ backgroundColor: color }">
        <el-icon :size="iconSize">
          <component :is="icon" />
        </el-icon>
      </div>
      <div class="stat-info">
        <div class="stat-value">{{ value }}</div>
        <div class="stat-label">{{ label }}</div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
defineProps({
  icon: {
    type: Object,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  label: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: '#409eff'
  },
  iconSize: {
    type: Number,
    default: 24
  }
})
</script>

<style scoped>
.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-right: 12px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}
</style>