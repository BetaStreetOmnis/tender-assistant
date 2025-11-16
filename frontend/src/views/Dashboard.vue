<template>
  <div class="dashboard">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>数据仪表板</h2>
      <el-button @click="refreshData">
        <el-icon><Refresh /></el-icon>
        刷新数据
      </el-button>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon size="32" color="#409EFF"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalBids }}</div>
              <div class="stat-label">总投标数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon size="32" color="#67C23A"><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.completedBids }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon size="32" color="#E6A23C"><Loading /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.inProgressBids }}</div>
              <div class="stat-label">进行中</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon size="32" color="#F56C6C"><FolderOpened /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalTemplates }}</div>
              <div class="stat-label">模板数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <!-- 投标状态分布 -->
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <span>投标状态分布</span>
          </template>
          <div ref="statusChartRef" class="chart-container"></div>
        </el-card>
      </el-col>

      <!-- 月度趋势 -->
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <span>月度趋势</span>
          </template>
          <div ref="trendChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- 最新活动 -->
      <el-col :span="12">
        <el-card class="activity-card" shadow="never">
          <template #header>
            <span>最新活动</span>
          </template>
          <div class="activity-list">
            <div
              v-for="activity in recentActivities"
              :key="activity.id"
              class="activity-item"
            >
              <div class="activity-icon">
                <el-icon :color="activity.color">
                  <component :is="activity.icon" />
                </el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-time">{{ activity.time }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 快速操作 -->
      <el-col :span="12">
        <el-card class="quick-actions-card" shadow="never">
          <template #header>
            <span>快速操作</span>
          </template>
          <div class="quick-actions-grid">
            <div class="quick-action-item" @click="$router.push('/bidding/create')">
              <el-icon size="24" color="#409EFF"><Plus /></el-icon>
              <span>创建投标</span>
            </div>
            <div class="quick-action-item" @click="$router.push('/analyze')">
              <el-icon size="24" color="#67C23A"><Search /></el-icon>
              <span>分析文档</span>
            </div>
            <div class="quick-action-item" @click="$router.push('/templates/create')">
              <el-icon size="24" color="#E6A23C"><Upload /></el-icon>
              <span>上传模板</span>
            </div>
            <div class="quick-action-item" @click="$router.push('/generate')">
              <el-icon size="24" color="#F56C6C"><Magic /></el-icon>
              <span>生成文档</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { useBiddingStore } from '@/stores/bidding'
import { useTemplateStore } from '@/stores/template'
import * as echarts from 'echarts'

const biddingStore = useBiddingStore()
const templateStore = useTemplateStore()

// 图表引用
const statusChartRef = ref<HTMLDivElement>()
const trendChartRef = ref<HTMLDivElement>()

// 统计数据
const stats = ref({
  totalBids: 0,
  completedBids: 0,
  inProgressBids: 0,
  totalTemplates: 0
})

// 最新活动
const recentActivities = ref([
  {
    id: 1,
    title: '创建了新的投标项目',
    time: '2小时前',
    icon: 'Document',
    color: '#409EFF'
  },
  {
    id: 2,
    title: '完成了招标文档分析',
    time: '4小时前',
    icon: 'Search',
    color: '#67C23A'
  },
  {
    id: 3,
    title: '上传了新的模板',
    time: '1天前',
    icon: 'Upload',
    color: '#E6A23C'
  },
  {
    id: 4,
    title: '生成了一份投标文档',
    time: '2天前',
    icon: 'Magic',
    color: '#F56C6C'
  }
])

// 初始化状态图表
const initStatusChart = () => {
  if (!statusChartRef.value) return

  const chart = echarts.init(statusChartRef.value)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '投标状态',
        type: 'pie',
        radius: '50%',
        data: [
          { value: stats.value.completedBids, name: '已完成' },
          { value: stats.value.inProgressBids, name: '进行中' },
          { value: stats.value.totalBids - stats.value.completedBids - stats.value.inProgressBids, name: '草稿' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }

  chart.setOption(option)
}

// 初始化趋势图表
const initTrendChart = () => {
  if (!trendChartRef.value) return

  const chart = echarts.init(trendChartRef.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['创建数量', '完成数量']
    },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '创建数量',
        type: 'line',
        data: [5, 8, 12, 15, 18, 22],
        smooth: true
      },
      {
        name: '完成数量',
        type: 'line',
        data: [3, 6, 9, 12, 16, 20],
        smooth: true
      }
    ]
  }

  chart.setOption(option)
}

// 加载数据
const loadData = async () => {
  try {
    // 获取投标数据
    await biddingStore.fetchBidResponses({ page: 1, page_size: 100 })
    await templateStore.fetchTemplates()

    // 计算统计数据
    const bids = biddingStore.bidResponses
    stats.value = {
      totalBids: bids.length,
      completedBids: bids.filter(b => b.status === 'completed').length,
      inProgressBids: bids.filter(b => b.status === 'in_progress').length,
      totalTemplates: templateStore.templates.length
    }

    // 初始化图表
    await nextTick()
    initStatusChart()
    initTrendChart()
  } catch (error: any) {
    ElMessage.error(`加载数据失败: ${error.message}`)
  }
}

// 刷新数据
const refreshData = async () => {
  ElMessage.info('正在刷新数据...')
  await loadData()
  ElMessage.success('数据刷新完成')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  height: 120px;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  margin-right: 16px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.chart-card {
  height: 400px;
}

.chart-container {
  height: 320px;
}

.activity-card {
  height: 400px;
}

.activity-list {
  height: 320px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  margin-right: 12px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: #f8f9fa;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #909399;
}

.quick-actions-card {
  height: 400px;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  height: 320px;
}

.quick-action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background-color: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quick-action-item:hover {
  background-color: #e9ecef;
  transform: translateY(-2px);
}

.quick-action-item span {
  margin-top: 12px;
  font-size: 14px;
  color: #303133;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stats-row .el-col {
    margin-bottom: 12px;
  }

  .chart-card,
  .activity-card,
  .quick-actions-card {
    margin-bottom: 20px;
  }

  .quick-actions-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
</style>