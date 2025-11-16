<template>
  <div class="create-bid">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>创建投标项目</span>
          <el-button @click="$router.go(-1)">返回</el-button>
        </div>
      </template>

      <el-form :model="bidForm" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="项目标题" prop="title">
          <el-input v-model="bidForm.title" placeholder="请输入投标项目标题" />
        </el-form-item>

        <el-form-item label="招标ID" prop="tender_id">
          <el-input v-model="bidForm.tender_id" placeholder="请输入招标ID（可选）" />
        </el-form-item>

        <el-form-item label="项目内容" prop="content">
          <el-input
            v-model="bidForm.content"
            type="textarea"
            :rows="10"
            placeholder="请输入项目详细内容描述..."
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">
            创建项目
          </el-button>
          <el-button @click="resetForm">重置</el-button>
          <el-button @click="$router.go(-1)">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import { useBiddingStore } from '@/stores/bidding'

const router = useRouter()
const biddingStore = useBiddingStore()

const formRef = ref<FormInstance>()
const loading = ref(false)

const bidForm = reactive({
  title: '',
  tender_id: '',
  content: '',
  status: 'draft' as const
})

const rules = {
  title: [
    { required: true, message: '请输入项目标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入项目内容', trigger: 'blur' },
    { min: 10, message: '内容至少需要 10 个字符', trigger: 'blur' }
  ]
}

const submitForm = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    await biddingStore.createBidResponse(bidForm)
    ElMessage.success('投标项目创建成功')
    router.push('/bidding')
  } catch (error: any) {
    if (error.message) {
      ElMessage.error(`创建失败: ${error.message}`)
    }
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
}
</script>

<style scoped>
.create-bid {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>