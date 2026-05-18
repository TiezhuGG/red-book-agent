/**
 * 维度评分柱状图组件
 * 显示各维度的评分和进度条
 */
import { Box, Typography, LinearProgress } from "@mui/material";

interface DimensionBarsProps {
  data: Record<string, number>;
}

const dimensions = [
  { key: "content", label: "内容质量", color: "#6366f1" },
  { key: "visual", label: "视觉表现", color: "#ec4899" },
  { key: "growth", label: "增长策略", color: "#10b981" },
  { key: "user_reaction", label: "互动潜力", color: "#f59e0b" },
  { key: "overall", label: "综合评分", color: "#8b5cf6" },
];

export default function DimensionBars({ data }: DimensionBarsProps) {
  return (
    <Box sx={{ padding: 2 }}>
      {dimensions.map((dim) => {
        const value = data[dim.key as keyof typeof data];
        const grade = value >= 80 ? "优秀" : value >= 60 ? "良好" : value >= 40 ? "一般" : "待提升";
        const gradeColor = value >= 80 ? "#10b981" : value >= 60 ? "#f59e0b" : value >= 40 ? "#f97316" : "#ef4444";
        
        return (
          <Box key={dim.key} sx={{ mb: 2 }}>
            <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 1 }}>
              <Typography sx={{ fontSize: 13, fontWeight: 500 }}>{dim.label}</Typography>
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <Typography sx={{ fontSize: 14, fontWeight: 600, color: dim.color }}>{value}</Typography>
                <Typography sx={{ fontSize: 11, color: gradeColor }}>{grade}</Typography>
              </Box>
            </Box>
            <LinearProgress
              variant="determinate"
              value={value}
              sx={{
                height: 6,
                borderRadius: 3,
                bgcolor: "#f0f0f0",
                "& .MuiLinearProgress-bar": {
                  bgcolor: dim.color,
                  borderRadius: 3,
                },
              }}
            />
          </Box>
        );
      })}
    </Box>
  );
}
