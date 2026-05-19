import { useNavigate } from "react-router-dom";
import { Box, Button, Typography } from "@mui/material";
import { motion } from "framer-motion";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "#faf9f7", display: "flex", alignItems: "center", justifyContent: "center", px: { xs: 4, md: 8 } }}>
      <Box sx={{ textAlign: "center", maxWidth: 600 }}>
        {/* Logo Badge */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Box
            sx={{
              display: "inline-block",
              px: 3,
              py: 1,
              bgcolor: "#fff0f1",
              borderRadius: "20px",
              mb: 6,
            }}
          >
            <Typography sx={{ fontSize: 12, fontWeight: 600, color: "#ff2442" }}>
              红薯医生
            </Typography>
          </Box>
        </motion.div>

        {/* Main Heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <Typography
            sx={{
              fontSize: { xs: 32, md: 48, lg: 56 },
              fontWeight: 800,
              color: "#262626",
              lineHeight: 1.2,
              mb: 4,
            }}
          >
            用数据拆解
            <br />
            <span style={{ color: "#ff2442" }}>小红书</span>的
            <span style={{ color: "#ff2442" }}>爆款密码</span>
          </Typography>
        </motion.div>

        {/* Subtitle */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <Typography sx={{ fontSize: 14, color: "#666", mb: 2 }}>
            传统回归聚类分析 + LLM 拆解内容逻辑
          </Typography>
          <Typography sx={{ fontSize: 13, color: "#999", mb: 8 }}>
            基于真实笔记 + 评论，双轨验证每一条诊断建议
          </Typography>
        </motion.div>

        {/* Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <Box sx={{ display: "flex", gap: 3, justifyContent: "center", flexWrap: "wrap" }}>
            <Button
              variant="contained"
              onClick={() => navigate("/app")}
              sx={{
                px: 8,
                py: 2.25,
                fontSize: 15,
                fontWeight: 700,
                borderRadius: "12px",
                background: "linear-gradient(135deg, #ff3d5c, #e61e3d)",
                boxShadow: "0 4px 16px rgba(255,36,66,0.25)",
                "&:hover": {
                  boxShadow: "0 6px 24px rgba(255,36,66,0.35)",
                  transform: "translateY(-1px)",
                },
                transition: "all 0.2s ease",
              }}
            >
              开始诊断笔记
            </Button>
            {/* <Button
              variant="outlined"
              endIcon={<ArrowDownward sx={{ fontSize: 16 }} />}
              sx={{
                px: 6,
                py: 2.25,
                fontSize: 14,
                fontWeight: 500,
                borderRadius: "12px",
                borderColor: "#e8e8e8",
                color: "#666",
                "&:hover": {
                  borderColor: "#ff2442",
                  color: "#ff2442",
                },
              }}
            >
              看看我们发现了什么
            </Button> */}
          </Box>
        </motion.div>
      </Box>
    </Box>
  );
}
