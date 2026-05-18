/**
 * 基线对比组件 - 简化版
 * 显示用户笔记与垂类基准数据的对比
 */
import { useState, useEffect } from "react";
import { Box, Typography, Chip } from "@mui/material";

interface BaselineComparisonProps {
  category: string;
  userTitle: string;
  userTags: string[];
}

export default function BaselineComparison({ category, userTitle, userTags }: BaselineComparisonProps) {
  const [baseline, setBaseline] = useState<{
    avgTitleLength: number;
    avgTagCount: number;
    bestHours: number[];
    hotTags: string[];
  }>({
    avgTitleLength: 18,
    avgTagCount: 6,
    bestHours: [18, 19, 20],
    hotTags: [],
  });

  useEffect(() => {
    const fetchBaseline = async () => {
      try {
        const response = await fetch(`/api/baseline/category/${category}`);
        if (response.ok) {
          const data = await response.json();
          setBaseline({
            avgTitleLength: data.stats?.avg_title_length || 18,
            avgTagCount: data.stats?.avg_tag_count || 6,
            bestHours: data.stats?.hour_distribution
              ? (JSON.parse(data.stats.hour_distribution) as { hour: number }[])
                  .sort((a, b) => b.hour - a.hour)
                  .slice(0, 3)
                  .map((h) => h.hour)
              : [18, 19, 20],
            hotTags: data.stats?.top_tags
              ? (JSON.parse(data.stats.top_tags) as { tag: string }[]).map((t) => t.tag)
              : [],
          });
        }
      } catch (error) {
        console.warn("Failed to fetch baseline data:", error);
      }
    };
    fetchBaseline();
  }, [category]);

  const titleVerdict = userTitle.length >= baseline.avgTitleLength * 0.8 && userTitle.length <= baseline.avgTitleLength * 1.3
    ? { text: "长度合适", color: "success" }
    : userTitle.length < baseline.avgTitleLength * 0.8
    ? { text: "偏短", color: "warning" }
    : { text: "偏长", color: "warning" };

  const tagVerdict = userTags.length >= baseline.avgTagCount * 0.7
    ? { text: "数量充足", color: "success" }
    : { text: "建议增加", color: "warning" };

  return (
    <Box sx={{ padding: 2 }}>
      <Box sx={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 2, mb: 3 }}>
        <Box>
          <Typography sx={{ fontSize: 12, color: "#999", mb: 1 }}>标题长度</Typography>
          <Typography sx={{ fontSize: 16, fontWeight: 600 }}>
            {userTitle.length} <span style={{ fontSize: 12, fontWeight: 400, color: "#999" }}>/ {baseline.avgTitleLength}字</span>
          </Typography>
          <Chip
            label={titleVerdict.text}
            size="small"
            sx={{
              mt: 1,
              bgcolor: titleVerdict.color === "success" ? "#e8f5e9" : "#fff3e0",
              color: titleVerdict.color === "success" ? "#2e7d32" : "#e65100",
              fontSize: 11,
            }}
          />
        </Box>
        <Box>
          <Typography sx={{ fontSize: 12, color: "#999", mb: 1 }}>标签数量</Typography>
          <Typography sx={{ fontSize: 16, fontWeight: 600 }}>
            {userTags.length} <span style={{ fontSize: 12, fontWeight: 400, color: "#999" }}>/ {baseline.avgTagCount}个</span>
          </Typography>
          <Chip
            label={tagVerdict.text}
            size="small"
            sx={{
              mt: 1,
              bgcolor: tagVerdict.color === "success" ? "#e8f5e9" : "#fff3e0",
              color: tagVerdict.color === "success" ? "#2e7d32" : "#e65100",
              fontSize: 11,
            }}
          />
        </Box>
      </Box>
      <Box>
        <Typography sx={{ fontSize: 12, color: "#999", mb: 1 }}>最佳发布时段</Typography>
        <Box sx={{ display: "flex", gap: 1 }}>
          {baseline.bestHours.map((hour) => (
            <Chip
              key={hour}
              label={`${hour}:00`}
              size="small"
              sx={{ bgcolor: "#e3f2fd", color: "#1976d2", fontSize: 11 }}
            />
          ))}
        </Box>
      </Box>
      {baseline.hotTags.length > 0 && (
        <Box sx={{ mt: 2 }}>
          <Typography sx={{ fontSize: 12, color: "#999", mb: 1 }}>热门标签参考</Typography>
          <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
            {baseline.hotTags.slice(0, 5).map((tag) => (
              <Chip
                key={tag}
                label={tag}
                size="small"
                sx={{ bgcolor: "#fff", border: "1px solid #e0e0e0", fontSize: 11 }}
              />
            ))}
          </Box>
        </Box>
      )}
    </Box>
  );
}
