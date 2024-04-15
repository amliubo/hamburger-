<template>
    <div ref="chart" style="width: 100%; height: 500px;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    mounted() {
        this.initChart();
    },
    methods: {
        async initChart() {
            const chartDom = this.$refs.chart;
            // 检查图表容器是否可见
            const rect = chartDom.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) {
                // 图表容器不可见，延迟初始化
                setTimeout(this.initChart, 100);
                return;
            }
            const myChart = echarts.init(chartDom);

            const response = await this.$axios.get('/gold_prices');
            const goldData = response.data;

            const dataset = {
                source: goldData.map(item => {
                    return [item.date, item.JO_52683, item.JO_52684, item.JO_52685];
                })
            };

            const option = {
                animationDuration: 1000,
                dataset: dataset,
                title: {
                    text: '黄金价格可视化：'
                },
                tooltip: {
                    trigger: 'axis'
                },
                xAxis: {
                    type: 'category',
                    nameLocation: 'middle',
                    axisLabel: {
                        formatter: function (value) {
                            // 将日期字符串格式化为 'MM-DD' 形式
                            return value.slice(5);
                        }
                    }
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    { type: 'line', seriesLayoutBy: 'column', encode: { x: 0, y: 1 }, name: '基础' },
                    { type: 'line', seriesLayoutBy: 'column', encode: { x: 0, y: 2 }, name: '零售' },
                    { type: 'line', seriesLayoutBy: 'column', encode: { x: 0, y: 3 }, name: '回收' }
                ]
            };

            myChart.setOption(option);
        }

    }
}
</script>
