<template>
    <div ref="chart" style="width: 100%; height: 500px;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    data() {
        return {
            chartData: null // 保存数据的变量
        };
    },
    mounted() {
        this.$nextTick(() => {
            this.initChart();
        });
    },
    activated() {
        this.initChart();
    },
    methods: {
        initChart() {
            const chartDom = this.$refs.chart;
            const myChart = echarts.init(chartDom);

            // 模拟测试数据
            const rawData = [
                { Year: 1950, Country: 'Finland', Income: 3000 },
                { Year: 1951, Country: 'Finland', Income: 3200 },
                { Year: 1968, Country: 'Finland', Income: 3000 },
            ];

            const countries = [
                'Finland',
                'France',
                'Germany',
                'Iceland',
                'Norway',
                'Poland',
                'Russia',
                'United Kingdom'
            ];

            const datasetWithFilters = [];
            const seriesList = [];

            countries.forEach(country => {
                var datasetId = 'dataset_' + country;
                datasetWithFilters.push({
                    id: datasetId,
                    fromDatasetId: 'dataset_raw',
                    transform: {
                        type: 'filter',
                        config: {
                            and: [
                                { dimension: 'Year', gte: 1950 },
                                { dimension: 'Country', '=': country }
                            ]
                        }
                    }
                });
                seriesList.push({
                    type: 'line',
                    datasetId: datasetId,
                    showSymbol: false,
                    name: country,
                    endLabel: {
                        show: true,
                        formatter: function (params) {
                            return params.value[3] + ': ' + params.value[0];
                        }
                    },
                    labelLayout: {
                        moveOverlap: 'shiftY'
                    },
                    emphasis: {
                        focus: 'series'
                    },
                    encode: {
                        x: 'Year',
                        y: 'Income',
                        label: ['Country', 'Income'],
                        itemName: 'Year',
                        tooltip: ['Income']
                    }
                });
            });

            const option = {
                animationDuration: 10000,
                dataset: [
                    {
                        id: 'dataset_raw',
                        source: rawData
                    },
                    ...datasetWithFilters
                ],
                title: {
                    text: 'Income of Germany and France since 1950'
                },
                tooltip: {
                    order: 'valueDesc',
                    trigger: 'axis'
                },
                xAxis: {
                    type: 'category',
                    nameLocation: 'middle'
                },
                yAxis: {
                    name: 'Income'
                },
                grid: {
                    right: 140
                },
                series: seriesList
            };
            myChart.setOption(option);
        }
    }
};
</script>
