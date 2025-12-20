<template>
  <div class="container">
    <div class="forum-header">
      <div class="header-left">
        <h2>📌 校园广场</h2>
        <span class="subtitle">畅所欲言，分享生活</span>
      </div>
      <el-button type="primary" size="large" round @click="dialogVisible = true">
        <el-icon><Edit /></el-icon> 发布新帖
      </el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="18">
        <div v-loading="loading">
          <el-empty v-if="posts.length === 0" description="暂无帖子，快来抢沙发！"></el-empty>
          
          <el-card 
            v-for="post in posts" 
            :key="post.id" 
            class="post-card" 
            shadow="hover" 
            @click="$router.push(`/forum/${post.id}`)"
          >
            <div class="post-header">
              <el-tag :type="getTagType(post.tag)" effect="light" round>{{ post.tag }}</el-tag>
              <h3 class="post-title">{{ post.title }}</h3>
            </div>
            <p class="post-content">{{ post.content }}</p>
            <div class="post-footer">
              <span class="author">
                <el-avatar :size="20" style="vertical-align: middle; margin-right: 5px">
                  {{ post.author ? post.author.substring(0,1) : '匿' }}
                </el-avatar>
                {{ post.author }}
              </span>
              <span class="time">{{ formatDate(post.create_time) }}</span>
              <span class="views">🔥 {{ post.view_count || 0 }} 浏览</span>
              
              <span 
                v-if="username === post.author || username === 'admin'" 
                class="delete-btn" 
                @click.stop="handleDelete(post)"
              >
                <el-icon><Delete /></el-icon> 删除
              </span>
            </div>
          </el-card>
        </div>
      </el-col>

      <el-col :span="6">
        <el-card class="sidebar-card">
          <h4>🔥 热门话题</h4>
          <el-divider></el-divider>
          <div class="hot-topic"># 数据库大作业</div>
          <div class="hot-topic"># 考研倒计时</div>
          <div class="hot-topic"># 食堂新菜测评</div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" title="发布新帖" width="500px">
      <el-form :model="form">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="请输入引人注目的标题"></el-input>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.tag" placeholder="选择分类">
            <el-option label="闲聊" value="闲聊"></el-option>
            <el-option label="提问" value="提问"></el-option>
            <el-option label="交易" value="交易"></el-option>
            <el-option label="吐槽" value="吐槽"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="form.content" type="textarea" :rows="4" placeholder="说点什么吧..."></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitPost">🚀 立即发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import request from '../utils/request';
// 引入图标
import { Edit, Delete } from '@element-plus/icons-vue';

interface Post {
  id: number;
  title: string;
  content: string;
  author: string;
  tag: string;
  create_time: string;
  view_count: number;
}

const posts = ref<Post[]>([]);
const loading = ref(true);
const dialogVisible = ref(false);
const username = localStorage.getItem('ms_username') || '匿名同学';

const form = reactive({
  title: '',
  content: '',
  tag: '闲聊',
  author: username
});

// 获取帖子列表
const fetchPosts = async () => {
  loading.value = true;
  try {
    const res = await request.get('http://localhost:8088/forum/all');
    if (res.data.code === 200) {
      posts.value = res.data.data;
    }
  } catch (e) {
    ElMessage.error("加载帖子失败");
  } finally {
    loading.value = false;
  }
};

// 发布帖子
const submitPost = async () => {
  if (!form.title || !form.content) {
    ElMessage.warning("标题和内容不能为空");
    return;
  }
  try {
    const res = await request.post('http://localhost:8088/forum/add', form);
    if (res.data.code === 200 || res.data === "发布成功") {
      ElMessage.success("发布成功！");
      dialogVisible.value = false;
      fetchPosts();
      form.title = '';
      form.content = '';
    } else {
      ElMessage.error("发布失败");
    }
  } catch (e) {
    ElMessage.error("网络错误");
  }
};

// 【新增】删除帖子逻辑
const handleDelete = (post: Post) => {
  ElMessageBox.confirm(
    '确定要删除这条帖子吗？相关的回复也会被一并删除。',
    '警告',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      const res = await request.post('http://localhost:8088/forum/delete', { id: post.id });
      if (res.data.code === 200) {
        ElMessage.success("删除成功");
        fetchPosts(); // 刷新列表
      } else {
        ElMessage.error(res.data.msg || "删除失败");
      }
    } catch (e) {
      ElMessage.error("删除请求出错");
    }
  }).catch(() => {});
};

const getTagType = (tag: string) => {
  const map: Record<string, string> = {
    '闲聊': 'info', '提问': 'warning', '交易': 'success', '吐槽': 'danger'
  };
  return map[tag] || '';
};

const formatDate = (timeStr: string) => {
  if (!timeStr) return '';
  return new Date(timeStr).toLocaleString();
};

onMounted(() => {
  fetchPosts();
});
</script>

<style scoped>
.container { padding: 20px; }
.forum-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05); }
.header-left h2 { margin: 0; color: #303133; }
.subtitle { color: #909399; font-size: 14px; }
.post-card { margin-bottom: 15px; transition: transform 0.2s; cursor: pointer; }
.post-card:hover { transform: translateY(-2px); }
.post-header { display: flex; align-items: center; margin-bottom: 10px; }
.post-title { margin: 0 0 0 10px; font-size: 18px; font-weight: bold; color: #303133; }
.post-content { color: #606266; font-size: 14px; line-height: 1.6; margin-bottom: 15px; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.post-footer { display: flex; align-items: center; color: #909399; font-size: 12px; }
.post-footer span { margin-right: 20px; display: flex; align-items: center; }
.sidebar-card { position: sticky; top: 20px; }
.hot-topic { padding: 10px 0; color: #409EFF; cursor: pointer; }
.hot-topic:hover { text-decoration: underline; }

/* 删除按钮样式 */
.delete-btn { color: #F56C6C; cursor: pointer; transition: color 0.3s; margin-left: auto !important; margin-right: 0 !important; }
.delete-btn:hover { color: #ff0000; font-weight: bold; }
</style>