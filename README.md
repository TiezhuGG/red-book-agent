<div align="center">

# 红薯医生

### AI 驱动的小红书笔记诊断平台

**基于 Multi-Agent 辩论架构的智能内容分析系统**

</div>

---

## 核心功能

- **多模态输入**：支持截图上传、Ctrl+V 粘贴，AI 自动识别标题、正文、分类
- **Multi-Agent 诊断**：5 位 AI 专家（内容分析、视觉诊断、增长策略、用户模拟、综合裁判）三轮辩论得出量化诊断报告
- **五维雷达评分**：内容质量 · 视觉表现 · 增长策略 · 互动潜力 · 综合评分
- **AI 模拟评论区**：真实 XHS 风格评论预测，含情绪分布与点赞预估
- **迭代优化引擎**：一键生成高分改写方案，自动重新评分
- **诊断历史**：本地存储，隐私安全

## 技术架构

### 前端
- React 19 · TypeScript · MUI v9 · Framer Motion · ECharts · Vite

### 后端
- FastAPI · asyncio · SSE 流式推送 · SQLite

### AI 核心
- 多模态视觉识别（OCR + Vision）
- 量化预测引擎（基于 874 条真实笔记训练）
- Multi-Agent 辩论系统

## 快速开始

```bash
# 克隆项目
git clone git@github.com:TiezhuGG/red-book-agent.git

# 配置环境变量
cp .env.example backend/.env

# 安装依赖
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# 启动后端（终端1）
cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 启动前端开发服务器（终端2）
cd frontend && npm run dev
```

访问 `http://localhost:5173`

## 项目结构

```
noterx/
├── frontend/                    # 前端应用
│   ├── src/
│   │   ├── components/         # 核心组件
│   │   │   ├── AgentDebate.tsx     # Agent 辩论展示
│   │   │   ├── ScoreCard.tsx       # 评分卡片
│   │   │   ├── RadarChart.tsx      # 雷达图
│   │   │   ├── UploadZone.tsx      # 上传区域
│   │   │   └── ...
│   │   ├── pages/              # 页面
│   │   │   ├── Home.tsx            # 首页（上传 + 识别）
│   │   │   ├── Diagnosing.tsx      # 诊断中页面
│   │   │   ├── Report.tsx          # 诊断报告
│   │   │   └── History.tsx         # 历史记录
│   │   └── utils/              # 工具函数
│   │       └── api.ts              # API 调用封装
│   └── package.json
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── main.py             # FastAPI 入口
│   │   ├── api/                # API 路由
│   │   │   ├── diagnose.py         # 诊断 API
│   │   │   ├── screenshot_api.py   # 截图分析 API
│   │   │   └── ...
│   │   ├── agents/             # Agent 实现
│   │   │   ├── orchestrator.py     # 多 Agent 编排
│   │   │   ├── content_agent.py    # 内容分析 Agent
│   │   │   ├── visual_agent.py     # 视觉诊断 Agent
│   │   │   ├── growth_agent.py     # 增长策略 Agent
│   │   │   ├── user_sim_agent.py   # 用户模拟 Agent
│   │   │   └── judge_agent.py      # 综合裁判 Agent
│   │   └── analysis/           # 分析模块
│   │       ├── ocr_processor.py    # OCR 处理
│   │       ├── image_analyzer.py   # 图片分析
│   │       └── ...
│   └── requirements.txt
├── data/                       # 数据文件
└── README.md
```

