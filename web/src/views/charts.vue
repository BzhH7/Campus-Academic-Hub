<template>
    <div class="container" v-loading="loading" element-loading-text="正在分析教务数据...">
        <div class="plugins-tips">
            数据来源：实时教务数据库统计 | 渲染引擎：Apache ECharts
        </div>
        
        <el-row :gutter="20">
            <el-col :span="24">
                <el-card shadow="hover" class="mgb20">
                    <template #header>
                        <div class="content-title">📊 各学院/系 开课数量统计</div>
                    </template>
                    <div id="barChart" class="schart" style="width: 100%; height: 400px;"></div>
                </el-card>
            </el-col>
        </el-row>

        <el-row :gutter="20">
            <el-col :span="8">
                <el-card shadow="hover" class="mgb20">
                    <template #header>
                        <div class="content-title">🍰 课程学分分布</div>
                    </template>
                    <div id="pieChart" class="schart" style="width: 100%; height: 350px;"></div>
                </el-card>
            </el-col>

            <el-col :span="8">
                <el-card shadow="hover" class="mgb20">
                    <template #header>
                        <div class="content-title">🏫 校区课程资源占比</div>
                    </template>
                    <div id="ringChart" class="schart" style="width: 100%; height: 350px;"></div>
                </el-card>
            </el-col>
            
             <el-col :span="8">
                <el-card shadow="hover" class="mgb20">
                    <template #header>
                        <div class="content-title">📑 课程性质/分类构成</div>
                    </template>
                    <div id="roseChart" class="schart" style="width: 100%; height: 350px;"></div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script setup lang="ts" name="basecharts">
import { onMounted, ref } from 'vue';
import { fetchData } from '../api'; // 使用已有的获取所有课程接口
import * as echarts from 'echarts';

const loading = ref(true);

onMounted(async () => {
    // 1. 获取真实数据
    try {
        const res = await fetchData(); // 调用 /course/all
        if (res.data.code === 200) {
            const courseList = res.data.data;
            processDataAndRender(courseList);
        }
    } catch (error) {
        console.error("获取图表数据失败", error);
    } finally {
        loading.value = false;
    }
});

// 数据处理与渲染逻辑
const processDataAndRender = (data: any[]) => {
    // --- 数据聚合 ---
    
    // 1. 按学院 (dname) 统计
    const deptMap = new Map();
    // 2. 按学分 (credit) 统计
    const creditMap = new Map();
    // 3. 按校区 (campus) 统计
    const campusMap = new Map();
    // 4. 按分类 (cclf) 统计
    const typeMap = new Map();

    data.forEach(item => {
        // 学院
        const dname = item.dname || '未知学院';
        deptMap.set(dname, (deptMap.get(dname) || 0) + 1);

        // 学分
        const credit = item.credit + '学分';
        creditMap.set(credit, (creditMap.get(credit) || 0) + 1);

        // 校区
        const campus = item.campus || '未知校区';
        campusMap.set(campus, (campusMap.get(campus) || 0) + 1);

        // 分类
        const cclf = item.cclf || '其他';
        typeMap.set(cclf, (typeMap.get(cclf) || 0) + 1);
    });

    // --- 渲染图表 ---
    renderBarChart(deptMap);
    renderPieChart(creditMap);
    renderRingChart(campusMap);
    renderRoseChart(typeMap);
};

// 1. 柱状图：学院分布
const renderBarChart = (map: Map<string, number>) => {
    const chartDom = document.getElementById('barChart')!;
    const myChart = echarts.init(chartDom);
    
    // 排序，取前15个学院，避免X轴太挤
    const sortedArray = Array.from(map).sort((a, b) => b[1] - a[1]).slice(0, 15);
    
    const option = {
        tooltip: { trigger: 'axis' },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { 
            type: 'category', 
            data: sortedArray.map(i => i[0]),
            axisLabel: { interval: 0, rotate: 30 } // 标签倾斜防止重叠
        },
        yAxis: { type: 'value' },
        series: [{
            name: '开课数',
            type: 'bar',
            data: sortedArray.map(i => i[1]),
            itemStyle: { color: '#409EFF' },
            label: { show: true, position: 'top' }
        }]
    };
    myChart.setOption(option);
    window.addEventListener('resize', () => myChart.resize());
};

// 2. 饼图：学分分布
const renderPieChart = (map: Map<string, number>) => {
    const chartDom = document.getElementById('pieChart')!;
    const myChart = echarts.init(chartDom);
    
    const data = Array.from(map).map(i => ({ value: i[1], name: i[0] }));
    
    const option = {
        tooltip: { trigger: 'item' },
        legend: { bottom: '0%', left: 'center' },
        color: ['#ee6666', '#fac858', '#91cc75', '#5470c6', '#73c0de'],
        series: [{
            name: '学分分布',
            type: 'pie',
            radius: '50%',
            data: data,
            emphasis: {
                itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }
            }
        }]
    };
    myChart.setOption(option);
    window.addEventListener('resize', () => myChart.resize());
};

// 3. 环形图：校区分布
const renderRingChart = (map: Map<string, number>) => {
    const chartDom = document.getElementById('ringChart')!;
    const myChart = echarts.init(chartDom);
    
    const data = Array.from(map).map(i => ({ value: i[1], name: i[0] }));

    const option = {
        tooltip: { trigger: 'item' },
        legend: { top: '5%', left: 'center' },
        series: [{
            name: '校区分布',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
            label: { show: false, position: 'center' },
            emphasis: {
                label: { show: true, fontSize: '20', fontWeight: 'bold' }
            },
            data: data
        }]
    };
    myChart.setOption(option);
    window.addEventListener('resize', () => myChart.resize());
};

// 4. 玫瑰图：课程性质
const renderRoseChart = (map: Map<string, number>) => {
    const chartDom = document.getElementById('roseChart')!;
    const myChart = echarts.init(chartDom);

    const data = Array.from(map).map(i => ({ value: i[1], name: i[0] }));

    const option = {
        tooltip: { trigger: 'item' },
        legend: { top: 'bottom' },
        series: [{
            name: '课程性质',
            type: 'pie',
            radius: [20, 100],
            center: ['50%', '50%'],
            roseType: 'area',
            itemStyle: { borderRadius: 8 },
            data: data
        }]
    };
    myChart.setOption(option);
    window.addEventListener('resize', () => myChart.resize());
};
</script>

<style scoped>
.container {
    padding: 20px;
    background: #f0f2f5;
}
.plugins-tips {
    background: #eef1f6;
    padding: 10px 20px;
    margin-bottom: 20px;
    border-radius: 4px;
    font-size: 14px;
    color: #606266;
}
.schart-box {
    display: inline-block;
    margin: 20px;
}
.content-title {
    font-weight: bold;
    font-size: 16px;
    color: #1f2f3d;
}
.mgb20 {
    margin-bottom: 20px;
}
</style>