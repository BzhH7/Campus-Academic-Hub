<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="8">
                <el-card shadow="hover" class="mgb20" style="height: 252px">
                    <div class="user-info">
                        <el-avatar :size="120" :src="imgurl" />
                        <div class="user-info-cont">
                            <div class="user-info-name">{{ name }}</div>
                            <div>{{ role }}</div>
                        </div>
                    </div>
                    <div class="user-info-list">
                        上次登录：<span>{{ new Date().toLocaleDateString() }}</span>
                    </div>
                    <div class="user-info-list">
                        我的状态：<span style="color: #64d572">在线</span>
                    </div>
                </el-card>

                <el-card shadow="hover" style="height: 252px">
                    <template #header>
                        <div class="clearfix">
                            <span>⚡ 常用工作台</span>
                        </div>
                    </template>
                    <div class="shortcut-grid">
                        <el-button type="primary" plain @click="$router.push('/table')">
                            <el-icon><Search /></el-icon> 查课
                        </el-button>
                        <el-button type="success" plain @click="$router.push('/forum')">
                            <el-icon><ChatLineRound /></el-icon> 论坛
                        </el-button>
                        <el-button type="warning" plain @click="$router.push('/newCourse')">
                            <el-icon><Plus /></el-icon> 开课
                        </el-button>
                        <el-button type="danger" plain @click="$router.push('/ManageComment')">
                            <el-icon><Comment /></el-icon> 审核
                        </el-button>
                        <el-button type="info" plain @click="$router.push('/charts')">
                            <el-icon><PieChart /></el-icon> 报表
                        </el-button>
                        <el-button type="primary" plain @click="$router.push('/user')">
                            <el-icon><User /></el-icon> 个人
                        </el-button>
                    </div>
                </el-card>
            </el-col>

            <el-col :span="16">
                <el-row :gutter="20" class="mgb20">
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{ padding: '0px' }">
                            <div class="grid-content grid-con-1">
                                <el-icon class="grid-con-icon"><Reading /></el-icon>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ courseNum }}</div>
                                    <div>课程总数</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{ padding: '0px' }">
                            <div class="grid-content grid-con-2">
                                <el-icon class="grid-con-icon"><ChatDotRound /></el-icon>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ commentNum }}</div>
                                    <div>社区互动数</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{ padding: '0px' }">
                            <div class="grid-content grid-con-3">
                                <el-icon class="grid-con-icon"><CollectionTag /></el-icon>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ labelNum }}</div>
                                    <div>学科分类</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>

                <el-card shadow="hover" style="height: 403px">
                    <template #header>
                        <div class="clearfix">
                            <span>🕸️ 课程知识交互图谱</span>
                            <el-tooltip content="全屏查看图谱" placement="top">
                                <el-button style="float: right; padding: 3px 0" text type="primary" @click="openFullGraph">
                                    <el-icon style="font-size: 18px"><FullScreen /></el-icon> 全屏探索
                                </el-button>
                            </el-tooltip>
                        </div>
                    </template>
                    <div id="smallChart" v-loading="loading" :element-loading-text="loadingText" style="width: 100%; height: 340px;"></div>
                </el-card>
            </el-col>
        </el-row>

        <el-dialog
            v-model="dialogVisible"
            title="课程知识全景图"
            fullscreen
            destroy-on-close
            @opened="initBigChart"
        >
            <div id="bigChart" style="width: 100%; height: 85vh;"></div>
        </el-dialog>
    </div>
</template>

<script setup lang="ts" name="dashboard">
import { onMounted, ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { EChartsOption, init } from 'echarts';
import { getRelationByNames, selectCourseByLabel, getAllLabels, getCourseNum, getCommentNum } from "../api";
import { ElMessage } from "element-plus";
import imgurl from '../assets/img/img.jpg';
import { Search, ChatLineRound, Plus, Comment, PieChart, User, Reading, ChatDotRound, CollectionTag, FullScreen } from '@element-plus/icons-vue';

const name = localStorage.getItem('ms_username') || 'Student';
const role = name === 'admin' ? '超级管理员' : '普通用户';

// 状态控制
const loading = ref(true);
const loadingText = ref("正在探测数据库中的课程标签...");
const dialogVisible = ref(false);

// 统计数据
const courseNum = ref(0);
const commentNum = ref(0);
const labelNum = ref(0);

// 图谱数据 (缓存起来，供大图和小图复用)
const graphData = reactive({
    nodes: [] as any[],
    links: [] as any[],
    categories: [] as string[]
});

const router = useRouter();

onMounted(async () => {
    // 1. 获取统计数字
    loadStatistics();
    // 2. 获取图谱数据并渲染小图
    await loadGraphData();
    initChart('smallChart', false);
});

// 加载统计
const loadStatistics = async () => {
    try {
        const cRes = await getCourseNum();
        if(cRes.data.code === 200) courseNum.value = cRes.data.data;
        const comRes = await getCommentNum();
        if(comRes.data.code === 200) commentNum.value = comRes.data.data || 0;
    } catch(e) {}
};

// 核心：加载图谱数据 (逻辑与你之前的一致，但存入了 graphData 变量)
const loadGraphData = async () => {
    const course_with_labels: any[] = [];
    const edges_with_labels: any[] = [];
    let labels: string[] = [];

    try {
        const labelRes = await getAllLabels();
        if (labelRes.data.code === 200 && labelRes.data.data.length > 0) {
            labels = labelRes.data.data;
            labelNum.value = labels.length;
            graphData.categories = labels;
            loadingText.value = `检测到 ${labels.length} 个学科，正在构建...`;
        } else {
            loading.value = false;
            return;
        }

        const nodePromises = labels.map(label => selectCourseByLabel(label));
        const results = await Promise.all(nodePromises);
        results.forEach((res, index) => {
            if (res.data.code === 200) {
                const nodes = res.data.data.map((item: any) => ({
                    ...item,
                    category: labels[index]
                }));
                course_with_labels.push(...nodes);
            }
        });

        // 去重
        const uniqueNodes = Array.from(new Map(course_with_labels.map(item => [item.name, item])).values());
        graphData.nodes = uniqueNodes;

        if (uniqueNodes.length === 0) {
            loading.value = false;
            return;
        }

        // 构建边
        const relationPromises = [];
        const limitNode = Math.min(uniqueNodes.length, 60); 
        for (let i = 0; i < limitNode; i++) {
            for (let j = i + 1; j < limitNode; j++) {
                relationPromises.push(
                    getRelationByNames(uniqueNodes[i]['name'], uniqueNodes[j]['name'])
                        .then(res => {
                            if (res.data.code !== 404 && res.data.data > 0) {
                                edges_with_labels.push({
                                    source: uniqueNodes[i]['name'],
                                    target: uniqueNodes[j]['name'],
                                    lineStyle: { width: res.data.data }
                                });
                            }
                        }).catch(() => {})
                );
            }
        }
        await Promise.all(relationPromises);
        graphData.links = edges_with_labels;
        loading.value = false;

    } catch (e) {
        loading.value = false;
        ElMessage.error("图谱数据加载异常");
    }
};

// 打开全屏图谱
const openFullGraph = () => {
    if (graphData.nodes.length === 0) {
        ElMessage.warning("数据尚未加载完毕");
        return;
    }
    dialogVisible.value = true;
};

// Dialog 打开后的回调：渲染大图
const initBigChart = () => {
    initChart('bigChart', true);
};

// 通用渲染函数 (containerId: 容器ID, isBig: 是否是大图)
function initChart(containerId: string, isBig: boolean) {
    const myChartEl = document.getElementById(containerId);
    if (!myChartEl) return;
    
    // 销毁旧实例
    try {
        const oldInstance =  (window as any).echarts?.getInstanceByDom(myChartEl);
        if(oldInstance) oldInstance.dispose();
    } catch(e){}

    let charEch = init(myChartEl);
    
    const option: EChartsOption = {
        // 大图显示标题，小图不显示
        title: isBig ? {
            text: '课程知识体系全景',
            subtext: '支持拖拽节点、缩放查看',
            left: 'center'
        } : undefined,
        tooltip: {},
        legend: {
            data: graphData.categories,
            type: 'scroll',
            orient: 'vertical',
            right: 10,
            top: 20,
            bottom: 20
        },
        series: [
            {
                type: 'graph',
                layout: 'force',
                categories: graphData.categories.map(l => ({ name: l })),
                force: {
                    // 大图斥力更大，看着更松散舒适
                    repulsion: isBig ? 800 : 300,
                    edgeLength: isBig ? [50, 200] : [30, 100]
                },
                symbolSize: isBig ? 40 : 20, // 大图节点更大
                roam: true,
                draggable: true,
                edgeSymbol: ['none', 'arrow'],
                edgeSymbolSize: 5,
                lineStyle: {
                    color: 'source',
                    curveness: 0.3
                },
                label: {
                    show: true,
                    position: 'bottom',
                    fontSize: isBig ? 14 : 10 // 大图文字更大
                },
                data: graphData.nodes.map(n => ({
                    name: n.name,
                    category: graphData.categories.findIndex(l => l === n.category),
                    symbolSize: (isBig ? 30 : 15) + Math.random() * (isBig ? 30 : 15)
                })),
                links: graphData.links
            }
        ]
    };
    charEch.setOption(option);
    window.addEventListener('resize', () => charEch.resize());
}
</script>

<style scoped>
.el-row { margin-bottom: 20px; }

/* 统计卡片样式 */
.grid-content { display: flex; align-items: center; height: 100px; }
.grid-cont-right { flex: 1; text-align: center; font-size: 14px; color: #999; }
.grid-num { font-size: 30px; font-weight: bold; }
.grid-con-icon { font-size: 50px; width: 100px; height: 100px; text-align: center; line-height: 100px; color: #fff; }
.grid-con-1 .grid-con-icon { background: #2d8cf0; }
.grid-con-1 .grid-num { color: #2d8cf0; }
.grid-con-2 .grid-con-icon { background: #64d572; }
.grid-con-2 .grid-num { color: #64d572; }
.grid-con-3 .grid-con-icon { background: #f25e43; }
.grid-con-3 .grid-num { color: #f25e43; }

/* 用户卡片样式 */
.user-info { display: flex; align-items: center; padding-bottom: 20px; border-bottom: 2px solid #ccc; margin-bottom: 20px; }
.user-info-cont { padding-left: 50px; flex: 1; font-size: 14px; color: #999; }
.user-info-cont div:first-child { font-size: 30px; color: #222; }
.user-info-list { font-size: 14px; color: #999; line-height: 25px; }
.user-info-list span { margin-left: 70px; }
.mgb20 { margin-bottom: 20px; }

/* 快捷操作样式 */
.shortcut-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; padding: 10px; }
.shortcut-grid .el-button { width: 100%; margin-left: 0; height: 50px; }
</style>