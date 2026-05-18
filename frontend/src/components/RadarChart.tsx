import { useLayoutEffect, useRef } from "react";
import * as echarts from "echarts";

interface Props {
  data: Record<string, number>;
}

const DIMENSION_LABELS: Record<string, string> = {
  content: "内容质量",
  visual: "视觉表现",
  growth: "增长策略",
  user_reaction: "用户反应",
  overall: "综合评分",
};

export default function RadarChart({ data }: Props) {
  const chartRef = useRef<HTMLDivElement>(null);
  const instanceRef = useRef<echarts.ECharts | null>(null);

  useLayoutEffect(() => {
    if (!chartRef.current) return;

    // Dispose existing instance if any
    if (instanceRef.current) {
      instanceRef.current.dispose();
      instanceRef.current = null;
    }

    // Create new instance
    const chartInstance = echarts.init(chartRef.current);
    instanceRef.current = chartInstance;

    const keys = Object.keys(DIMENSION_LABELS);
    const indicators = keys.map((key) => ({
      name: DIMENSION_LABELS[key],
      max: 100,
    }));
    const values = keys.map((key) => data[key] ?? 50);

    chartInstance.setOption({
      animationDuration: 1200,
      radar: {
        indicator: indicators,
        shape: "polygon",
        splitNumber: 4,
        radius: "65%",
        axisName: { color: "#262626", fontSize: 12, fontWeight: 600 },
        splitLine: { lineStyle: { color: "#f0f0f0" } },
        splitArea: { show: false },
        axisLine: { lineStyle: { color: "#e8e8e8" } },
      },
      series: [
        {
          type: "radar",
          data: [
            {
              value: values,
              areaStyle: { color: "rgba(255,36,66,0.15)" },
              lineStyle: { color: "#ff2442", width: 2 },
              itemStyle: { color: "#ff2442", borderColor: "#fff", borderWidth: 2 },
              symbol: "circle",
              symbolSize: 6,
            },
          ],
        },
      ],
      tooltip: {
        trigger: "item",
        backgroundColor: "#fff",
        borderColor: "#f0f0f0",
        textStyle: { color: "#262626", fontSize: 13 },
      },
    });

    const handleResize = () => chartInstance.resize();
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chartInstance.dispose();
      instanceRef.current = null;
    };
  }, [data]);

  return <div ref={chartRef} style={{ height: 280, width: "100%" }} />;
}
