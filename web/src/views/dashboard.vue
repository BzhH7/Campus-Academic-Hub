<template>
	<div>
		<el-row :gutter="20">
			<el-col :span="24">
          <el-card shadow="hover" class="mgb20" style="height: 100%">
            <div id="myChart" v-loading="loading" :element-loading-text="loadingText" :style="{width: '100%', height: '80vh'}"></div>
          </el-card>
			</el-col>
		</el-row>
	</div>
</template>

<script setup lang="ts" name="dashboard">
import { onMounted, ref } from 'vue';
import { ECharts, EChartsOption, init } from 'echarts';
// 注意：这里引入了新增的 getAllLabels
import { getRelationByNames, selectCourseByLabel, getAllLabels } from "../api";
import { ElMessage } from "element-plus";

const loading = ref(true);
const loadingText = ref("正在探测数据库中的课程标签...");

onMounted(async () => {
  const course_with_labels: any[] = [];
  const edges_with_labels: any[] = [];
  let labels: string[] = [];

  // ------------------------------------------------
  // 第一步：自动获取数据库里所有的标签
  // ------------------------------------------------
  try {
    const labelRes = await getAllLabels();
    if (labelRes.data.code === 200 && labelRes.data.data.length > 0) {
      labels = labelRes.data.data;
      console.log("检测到标签：", labels);
      loadingText.value = `检测到 ${labels.length} 个标签，正在加载课程数据...`;
    } else {
      ElMessage.warning("数据库中没有检测到任何标签，请先运行数据生成脚本！");
      loading.value = false;
      return;
    }
  } catch (e) {
    ElMessage.error("连接后端失败，请检查后端是否启动");
    loading.value = false;
    return;
  }

  // ------------------------------------------------
  // 第二步：根据检测到的标签，并行获取课程节点
  // ------------------------------------------------
  try {
    const nodePromises = labels.map(label => selectCourseByLabel(label));
    const results = await Promise.all(nodePromises);

    results.forEach((res, index) => {
      if (res.data.code === 200) {
        const nodes = res.data.data.map((item: any) => ({
          ...item,
          category: labels[index] // 绑定正确的分类
        }));
        course_with_labels.push(...nodes);
      }
    });
  } catch (error) {
    console.error(error);
  }

  // 去重（防止同一个课程有多个标签导致节点重复）
  const uniqueNodes = Array.from(new Map(course_with_labels.map(item => [item.name, item])).values());

  if (uniqueNodes.length === 0) {
    ElMessage.warning("标签下没有关联任何课程！");
    loading.value = false;
    return;
  }

  loadingText.value = "正在构建课程关系网...";

  // ------------------------------------------------
  // 第三步：建立连线关系
  // ------------------------------------------------
  const relationPromises = [];
  // 限制计算量，防止浏览器卡死
  const limitNode = Math.min(uniqueNodes.length, 60); 

  for (let i = 0; i < limitNode; i++) {
    for (let j = i + 1; j < limitNode; j++) {
        const p = getRelationByNames(uniqueNodes[i]['name'], uniqueNodes[j]['name'])
          .then(res => {
            if (res.data.code !== 404 && res.data.data > 0) {
              edges_with_labels.push({
                source: uniqueNodes[i]['name'],
                target: uniqueNodes[j]['name'],
                lineStyle: { width: res.data.data }
              });
            }
          }).catch(() => {});
        relationPromises.push(p);
    }
  }

  await Promise.all(relationPromises);

  // ------------------------------------------------
  // 第四步：渲染图表
  // ------------------------------------------------
  loading.value = false;
  initChart(uniqueNodes, edges_with_labels, labels);
});

function initChart(nodes: any[], links: any[], categories: string[]) {
  const myChartEl = document.getElementById('myChart');
  if (!myChartEl) return;

  // 销毁旧实例，防止缓存
  let charEch = init(myChartEl);
  
  const option: EChartsOption = {
    backgroundColor: '#ffffff',
    // 自动生成更多颜色
    color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
    title: {
      text: '课程知识图谱 (自动生成)',
      subtext: `自动检测到 ${categories.length} 类标签，包含 ${nodes.length} 门课程`,
      textStyle: { fontWeight: 700, fontSize: 24 }
    },
    tooltip: {},
    legend: [{
      data: categories,
      orient: 'vertical',
      right: 10,
      top: 'center'
    }],
    series: [
      {
        type: 'graph',
        layout: 'force',
        categories: categories.map(l => ({ name: l })),
        force: {
          repulsion: 400,
          edgeLength: [50, 150]
        },
        label: {
          show: true,
          position: 'right'
        },
        symbolSize: 40,
        roam: true,
        draggable: true,
        edgeSymbol: ['circle', 'arrow'],
        edgeSymbolSize: [4, 10],
        lineStyle: {
          color: 'source',
          curveness: 0.3
        },
        data: nodes.map(n => ({
          name: n.name,
          category: categories.findIndex(l => l === n.category),
          symbolSize: 40 + (Math.random() * 15)
        })),
        links: links
      }
    ]
  };
  charEch.setOption(option);
  window.addEventListener('resize', () => charEch.resize());
}
</script>

<style scoped>
.mgb20 { margin-bottom: 20px; }
</style>