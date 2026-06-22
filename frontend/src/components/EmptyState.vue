<template>
  <div class="empty-state">
    <el-empty :description="description">
      <template #image>
        <el-icon :size="64" color="#c0c4cc">
          <component :is="icon" />
        </el-icon>
      </template>
      <slot></slot>
    </el-empty>
  </div>
</template>

<script setup>
defineProps({
  description: {
    type: String,
    default: '暂无数据'
  },
  icon: {
    type: Object,
    default: null
  }
})
</script>

<style scoped>
.empty-state {
  padding: 60px 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>