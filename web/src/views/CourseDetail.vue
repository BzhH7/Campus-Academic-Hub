<template>
  <div v-loading="loading">
    <div class="container" v-if="courseInfo">
      <el-descriptions class="margin-top" title="课程详情档案" direction="vertical" :column="4" border>
        <el-descriptions-item label="课程号">
          <el-tag>{{ courseInfo.cno }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="课程名称" :span="2">
          <span style="font-weight: bold; font-size: 16px">{{ courseInfo.cname }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="授课教师">{{ courseInfo.tname }}</el-descriptions-item>
        
        <el-descriptions-item label="学分">{{ courseInfo.credit }}</el-descriptions-item>
        <el-descriptions-item label="学时">{{ courseInfo.length }}</el-descriptions-item>
        <el-descriptions-item label="校区">{{ courseInfo.campus }}</el-descriptions-item>
        <el-descriptions-item label="性质">{{ courseInfo.cclf }}</el-descriptions-item>
        
        <el-descriptions-item label="上课时间" :span="2">{{ courseInfo.csche }}</el-descriptions-item>
        <el-descriptions-item label="开课学院" :span="2">{{ courseInfo.dname }}</el-descriptions-item>
        
        <el-descriptions-item label="课程介绍" :span="4">
          {{ courseInfo.description || '暂无详细介绍' }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="comment-section">
        <div class="section-title">
          <h3>💬 课程评价 ({{ comments.length }})</h3>
        </div>
        
        <el-empty v-if="comments.length === 0" description="暂无评价，快来发表第一条神评！"></el-empty>

        <div v-else class="comment-list">
          <div v-for="(item, index) in comments" :key="index" class="comment-item">
            <div class="comment-avatar">{{ item.sno ? item.sno.substring(0,1) : '匿' }}</div>
            <div class="comment-body">
              <div class="comment-user">
                {{ item.sno || '匿名同学' }} 
                <span class="comment-time">{{ item.time }}</span>
                <el-rate v-model="item.sscore" disabled show-score text-color="#ff9900" size="small" v-if="item.sscore"></el-rate>
              </div>
              <div class="comment-content" v-html="item.detail"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="post-section">
        <div class="section-title">✍️ 写评价</div>
        <div class="editor-box" ref="editor"></div>
        <div class="submit-box">
           <span class="tips">温馨提示：评论提交后需通过管理员审核才会显示。</span>
           <el-button type="primary" size="large" @click="syncHTML">提交评价</el-button>
           <el-button @click="goBack">返回列表</el-button>
        </div>
      </div>
    </div>
    
    <div v-else class="error-tip">
      <el-empty description="未找到课程信息，请返回列表重新选择"></el-empty>
      <el-button type="primary" @click="goBack">返回课程列表</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import WangEditor from 'wangeditor';
// 1. 引入 watch 和 nextTick
import { ref, reactive, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from 'element-plus';
import request from '../utils/request';

const route = useRoute();
const router = useRouter();

const loading = ref(true);
const courseInfo = ref<any>(null);
const comments = ref<any[]>([]);
const editor = ref(null);
let instance: any = null;

const currentCno = route.query.cno as string;

const goBack = () => {
  router.push('/table');
};

const initData = async () => {
  if (!currentCno) {
    loading.value = false;
    return;
  }

  try {
    const resCourse = await request.get(`http://localhost:8088/course/search?cno=${currentCno}`);
    if (resCourse.data.code === 200 && resCourse.data.data.length > 0) {
      // 数据赋值
      courseInfo.value = resCourse.data.data[0];
    }

    const resComment = await request.get(`http://localhost:8088/comment/course/visible?cno=${currentCno}`);
    if (resComment.data.code === 200) {
      comments.value = resComment.data.data;
    }
  } catch (e) {
    ElMessage.error("数据加载失败");
  } finally {
    loading.value = false;
  }
};

// 2. 核心修复：监听 courseInfo 的变化
watch(courseInfo, (newVal) => {
  if (newVal) {
    // 只有当 courseInfo 有数据时，DOM 才会渲染，此时再初始化编辑器
    nextTick(() => {
      if (editor.value && !instance) {
        instance = new WangEditor(editor.value);
        instance.config.zIndex = 1;
        instance.config.placeholder = '分享你的上课体验、考试难度或给分情况...';
        instance.create();
      }
    });
  }
});

const content = reactive({
  cno: currentCno,
  cid: 0,
  sno: localStorage.getItem('ms_username') || '匿名',
  time: '',
  detail: '',
  isselect: 1,
  sscore: 5,
  visible: 0,
});

const syncHTML = () => {
  if (!instance || !instance.txt.text()) {
    return ElMessage.warning("写点内容再提交吧~");
  }

  content.detail = instance.txt.html();
  content.time = new Date().toLocaleDateString();

  request.get(`http://localhost:8088/course/comment/num?cno=${currentCno}`).then(res => {
    content.cid = (res.data.data || 0) + 1;
    
    ElMessageBox.confirm('确定提交评论吗？需要管理员审核后才能显示。', '提示', { type: 'info' })
      .then(() => {
        request.post('http://localhost:8088/comment/new', content).then(res => {
          if (res.data.code === 200) {
            ElMessage.success("提交成功！请耐心等待审核。");
            instance.txt.clear();
          } else {
            ElMessage.error("提交失败");
          }
        });
      }).catch(() => {});
  });
};

onMounted(() => {
  initData();
  // 注意：删除了这里原来的初始化代码，改用上面的 watch 实现
});

onBeforeUnmount(() => {
  if (instance) {
    instance.destroy();
    instance = null;
  }
});
</script>

<style scoped>
.container { padding: 20px; background: #fff; border-radius: 8px; }
.margin-top { margin-bottom: 30px; }
.section-title { border-left: 5px solid #409EFF; padding-left: 10px; margin: 30px 0 20px 0; }
.section-title h3 { margin: 0; }

/* 评论列表样式 */
.comment-list { display: flex; flex-direction: column; gap: 20px; }
.comment-item { display: flex; gap: 15px; padding-bottom: 20px; border-bottom: 1px solid #f0f0f0; }
.comment-avatar { width: 45px; height: 45px; background: #e6f7ff; color: #1890ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px; }
.comment-body { flex: 1; }
.comment-user { font-weight: bold; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; }
.comment-time { color: #999; font-weight: normal; font-size: 12px; }
.comment-content { color: #333; line-height: 1.6; font-size: 14px; }

/* 编辑器样式 */
.post-section { margin-top: 40px; background: #f9f9f9; padding: 20px; border-radius: 8px; }
.submit-box { margin-top: 15px; display: flex; justify-content: space-between; align-items: center; }
.tips { color: #909399; font-size: 13px; }
.error-tip { padding: 50px; text-align: center; }
</style>