<template>
  <div class="container" v-loading="loading">
    <div class="back-btn">
      <el-button link @click="$router.go(-1)">← 返回列表</el-button>
    </div>

    <el-card class="main-post" v-if="post">
      <div class="post-header">
        <el-tag size="large">{{ post.tag }}</el-tag>
        <h1 class="title">{{ post.title }}</h1>
      </div>
      <div class="meta-info">
        <span>👤 {{ post.author }}</span>
        <span>🕒 {{ formatDate(post.create_time) }}</span>
        <span>🔥 {{ post.view_count || 0 }} 浏览</span>
      </div>
      <el-divider></el-divider>
      <div class="content">{{ post.content }}</div>
    </el-card>

    <div class="reply-section">
      <h3>💬 全部回复 ({{ replies.length }})</h3>
      
      <div v-for="(item, index) in replies" :key="item.id" class="reply-item">
        <div class="reply-avatar">{{ item.author.substring(0,1) }}</div>
        <div class="reply-body">
          <div class="reply-user">{{ item.author }} <span class="floor">#{{ index + 1 }}楼</span></div>
          <div class="reply-content">{{ item.content }}</div>
          <div class="reply-time">{{ formatDate(item.create_time) }}</div>
        </div>
      </div>
      <el-empty v-if="replies.length === 0" description="暂无回复，快来抢沙发"></el-empty>

      <div class="reply-box">
        <el-input
          v-model="replyContent"
          type="textarea"
          :rows="3"
          placeholder="友善评论，理性交流..."
        ></el-input>
        <div class="reply-action">
          <el-button type="primary" @click="submitReply">发送评论</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import request from '../utils/request';

const route = useRoute();
const postId = route.params.id;
const loading = ref(true);
const post = ref<any>(null);
const replies = ref<any[]>([]);
const replyContent = ref('');
const username = localStorage.getItem('ms_username') || '匿名同学';

const loadData = async () => {
  loading.value = true;
  try {
    // 并行请求帖子详情和评论
    const [resPost, resReply] = await Promise.all([
      request.get(`http://localhost:8088/forum/detail?id=${postId}`),
      request.get(`http://localhost:8088/forum/replies?postId=${postId}`)
    ]);

    if (resPost.data.code === 200) post.value = resPost.data.data;
    if (resReply.data.code === 200) replies.value = resReply.data.data;
  } catch (e) {
    ElMessage.error("加载失败");
  } finally {
    loading.value = false;
  }
};

const submitReply = async () => {
  if (!replyContent.value.trim()) return ElMessage.warning("写点什么吧");
  
  try {
    const res = await request.post('http://localhost:8088/forum/reply/add', {
      post_id: postId,
      content: replyContent.value,
      author: username
    });
    if (res.data.code === 200) {
      ElMessage.success("回复成功");
      replyContent.value = '';
      loadData(); // 刷新评论
    }
  } catch (e) {
    ElMessage.error("发送失败");
  }
};

const formatDate = (str: string) => {
  return str ? new Date(str).toLocaleString() : '';
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
.container { padding: 20px; max-width: 1000px; margin: 0 auto; }
.back-btn { margin-bottom: 10px; }
.main-post { margin-bottom: 20px; border-radius: 8px; }
.post-header { display: flex; align-items: center; gap: 15px; margin-bottom: 15px; }
.title { margin: 0; font-size: 24px; color: #333; }
.meta-info { color: #999; font-size: 13px; display: flex; gap: 20px; }
.content { font-size: 16px; line-height: 1.8; color: #333; min-height: 100px; white-space: pre-wrap; }

.reply-section { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05); }
.reply-item { display: flex; gap: 15px; padding: 15px 0; border-bottom: 1px solid #eee; }
.reply-avatar { width: 40px; height: 40px; background: #e0e0e0; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #666; font-weight: bold; }
.reply-body { flex: 1; }
.reply-user { font-weight: bold; font-size: 14px; margin-bottom: 5px; }
.floor { float: right; color: #ccc; font-weight: normal; font-size: 12px; }
.reply-content { font-size: 14px; color: #555; line-height: 1.6; margin-bottom: 8px; }
.reply-time { font-size: 12px; color: #999; }

.reply-box { margin-top: 30px; background: #f9f9f9; padding: 20px; border-radius: 8px; }
.reply-action { margin-top: 10px; text-align: right; }
</style>