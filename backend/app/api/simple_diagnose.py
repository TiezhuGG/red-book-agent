"""
简化版诊断 API - 使用演示数据，无需额外依赖
"""
from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from typing import Optional
import json

router = APIRouter()

# 演示诊断结果数据
FALLBACK_REPORT = {
    "overall_score": 68,
    "grade": "B+",
    "radar_data": {
        "content": 72,
        "visual": 65,
        "growth": 60,
        "user_reaction": 70,
        "overall": 68,
    },
    "agent_opinions": [
        {
            "agent_name": "内容分析师",
            "dimension": "内容质量",
            "score": 72,
            "issues": [
                "标题缺少数字和具体数据，吸引力不足",
                "正文段落划分可以更清晰",
            ],
            "suggestions": [
                "在标题中加入具体数字，如「5个方法」「3步搞定」",
                "每段开头用emoji标记，增加可读性",
            ],
            "reasoning": "标题12字，该垂类爆款平均18字，偏短。缺少钩子词和情绪词。",
            "debate_comments": [],
        },
        {
            "agent_name": "视觉诊断师",
            "dimension": "视觉表现",
            "score": 65,
            "issues": [
                "封面色彩饱和度偏低，在信息流中不够醒目",
                "封面无文字覆盖，缺少信息传达",
            ],
            "suggestions": [
                "提高封面饱和度到0.6以上",
                "在封面添加20%-30%的文字区域，突出核心信息",
            ],
            "reasoning": "封面饱和度0.35，低于垂类均值0.55。建议参考爆款封面风格。",
            "debate_comments": [],
        },
        {
            "agent_name": "增长策略师",
            "dimension": "增长策略",
            "score": 60,
            "issues": [
                "标签数量仅3个，该垂类爆款平均使用6个",
                "未使用任何热门标签",
            ],
            "suggestions": [
                "增加至5-8个标签，混合热门标签和长尾标签",
                "建议在18:00-21:00之间发布，该时段互动率最高",
            ],
            "reasoning": "标签覆盖率为0，未命中任何Top10热门标签。建议添加相关垂类标签。",
            "debate_comments": [],
        },
        {
            "agent_name": "用户模拟器",
            "dimension": "用户反应",
            "score": 70,
            "issues": [
                "标题过于平淡，路过用户可能直接跳过",
                "缺少引导互动的话术",
            ],
            "suggestions": [
                "在正文末尾添加互动引导，如「你们觉得呢？评论区聊聊」",
                "增加个人体验和真实感受，提高代入感",
            ],
            "reasoning": "模拟用户反应：核心用户会点开但不一定互动，路过用户大概率跳过。",
            "debate_comments": [],
        },
    ],
    "issues": [
        {
            "severity": "high",
            "description": "标签策略严重不足，热门标签覆盖率为0",
            "from_agent": "增长策略师",
        },
        {
            "severity": "medium",
            "description": "封面视觉吸引力低于垂类平均水平",
            "from_agent": "视觉诊断师",
        },
        {
            "severity": "medium",
            "description": "标题缺少钩子词和数字，点击率可能偏低",
            "from_agent": "内容分析师",
        },
    ],
    "suggestions": [
        {
            "priority": 1,
            "description": "增加标签至5-8个，包含至少3个垂类热门标签",
            "expected_impact": "预计曝光量提升30-50%",
        },
        {
            "priority": 2,
            "description": "重新设计封面，提高饱和度并添加文字标题",
            "expected_impact": "预计点击率提升20-40%",
        },
        {
            "priority": 3,
            "description": "优化标题，加入数字和情绪词",
            "expected_impact": "预计点击率提升15-25%",
        },
    ],
    "debate_summary": "4位专家一致认为标签策略是最大短板。内容分析师和用户模拟器在标题吸引力上存在轻微分歧——内容分析师认为标题信息量不够，用户模拟器则认为标题虽然平淡但不至于扣太多分。最终综合考虑，标题评分取中间值。",
    "simulated_comments": [
        {"username": "爱分享的小李", "avatar_emoji": "👧", "comment": "感觉还不错，但是排版可以再优化一下～", "sentiment": "neutral", "likes": 12, "time_ago": "2小时前"},
        {"username": "挑剔的美食家", "avatar_emoji": "🧑‍🍳", "comment": "内容太笼统了，希望有更详细的步骤", "sentiment": "negative", "likes": 5, "time_ago": "1小时前"},
        {"username": "路过的吃货", "avatar_emoji": "😋", "comment": "收藏了！下次试试看", "sentiment": "positive", "likes": 23, "time_ago": "3小时前"},
        {"username": "认真学习中", "avatar_emoji": "📚", "comment": "图片拍得再好看点就完美了", "sentiment": "neutral", "likes": 8, "time_ago": "4小时前"},
        {"username": "小红薯新人", "avatar_emoji": "🌱", "comment": "谢谢分享！很有帮助", "sentiment": "positive", "likes": 15, "time_ago": "5小时前"},
    ],
    "optimized_title": "5步轻松搞定！零失败的懒人食谱｜新手必看🔥",
    "optimized_content": "今天给大家分享一个超级简单的懒人食谱！\n\n✅ 食材准备（5分钟）\n只需要鸡蛋、米饭、酱油、葱花，冰箱里随时有的食材就够了。\n\n✅ 制作步骤（10分钟）\n1. 隔夜饭打散备用\n2. 鸡蛋打散加少许盐\n3. 热锅下油，先炒蛋再加饭\n4. 加酱油调色，大火翻炒\n5. 出锅撒葱花，完美！\n\n✅ 小贴士\n米饭一定要用隔夜饭，粒粒分明才好吃！\n\n你们平时最爱做什么快手菜？评论区聊聊👇",
    "cover_direction": {
        "layout": "上文下图或左文右图，主体食物占画面60%以上",
        "color_scheme": "暖色调为主（橙色/黄色），饱和度拉高到0.6+",
        "text_style": "封面大字写「5分钟搞定」，副标题「零失败懒人食谱」",
        "tips": [
            "食物特写比全景更吸引人",
            "加一双筷子或手增加真实感",
            "避免滤镜过重导致食物颜色失真",
        ],
    },
    "debate_timeline": [
        {"round": 2, "agent_name": "内容分析师", "kind": "agree", "text": "同意增长策略师关于标签不足的判断——标签覆盖率为0确实是最大短板。"},
        {"round": 2, "agent_name": "视觉诊断师", "kind": "rebuttal", "text": "不完全同意用户模拟器的评分。即使标题平淡，视觉封面不行才是路过用户跳过的主因。"},
        {"round": 2, "agent_name": "增长策略师", "kind": "add", "text": "补充一个被忽略的问题：正文末尾缺少互动引导语，如「你们觉得呢？」，这会显著影响评论率。"},
        {"round": 2, "agent_name": "用户模拟器", "kind": "agree", "text": "同意视觉诊断师的观点。封面确实需要更鲜明的色彩才能在信息流中脱颖而出。"},
    ],
}

# 预评分演示数据
FALLBACK_PRESCORE = {
    "total_score": 65,
    "dimensions": {
        "title_quality": 58,
        "content_quality": 70,
        "visual_quality": 62,
        "tag_strategy": 55,
        "engagement_potential": 68,
    },
    "weights": {
        "title_quality": 0.25,
        "content_quality": 0.20,
        "visual_quality": 0.25,
        "tag_strategy": 0.15,
        "engagement_potential": 0.15,
    },
    "level": "B",
    "baseline": {
        "avg_engagement": 1250,
        "median": 890,
        "viral_threshold": 5000,
        "sample_size": 874,
    },
    "category": "food",
    "category_cn": "美食",
}

@router.post("/pre-score")
async def pre_score(title: str = Form(""), content: str = Form(""), category: str = Form("food"), tags: str = Form(""), image_count: int = Form(0)):
    """简化版预评分 API"""
    result = FALLBACK_PRESCORE.copy()
    result["category"] = category
    category_cn_map = {
        "food": "美食",
        "fashion": "穿搭",
        "tech": "科技",
        "travel": "旅行",
        "beauty": "美妆",
        "fitness": "健身",
        "lifestyle": "生活",
        "home": "家居",
    }
    result["category_cn"] = category_cn_map.get(category, "其他")
    return result

@router.post("/diagnose")
async def diagnose(title: str = Form(""), content: str = Form(""), category: str = Form(...), tags: str = Form("")):
    """简化版诊断 API"""
    if not title:
        raise HTTPException(status_code=400, detail="请提供标题")
    
    result = FALLBACK_REPORT.copy()
    title_len = len(title)
    if title_len >= 18:
        result["overall_score"] = min(75, result["overall_score"] + 5)
        result["radar_data"]["content"] = min(80, result["radar_data"]["content"] + 8)
    
    return result

@router.post("/diagnose-stream")
async def diagnose_stream(title: str = Form(""), content: str = Form(""), category: str = Form(...), tags: str = Form("")):
    """简化版流式诊断 API"""
    import asyncio
    from fastapi.responses import StreamingResponse
    
    async def generate():
        yield f"event: pre_score\ndata: {json.dumps(FALLBACK_PRESCORE)}\n\n"
        await asyncio.sleep(1)
        
        steps = [
            ("parse_start", "正在解析笔记内容..."),
            ("parse_done", "内容解析完成"),
            ("baseline_start", "正在对比垂类数据..."),
            ("baseline_done", "基线对比完成"),
            ("round1_start", "内容分析师诊断中..."),
            ("round1_content_done", "内容分析完成"),
            ("round1_visual_done", "视觉诊断完成"),
            ("round1_growth_done", "增长策略分析完成"),
            ("round1_user_done", "用户模拟完成"),
            ("debate_start", "Agent 辩论中..."),
            ("debate_done", "辩论完成"),
            ("judge_start", "综合裁判评定中..."),
            ("judge_done", "评定完成"),
            ("finalizing", "生成诊断报告..."),
        ]
        
        for step, message in steps:
            yield f"event: progress\ndata: {json.dumps({'step': step, 'message': message})}\n\n"
            await asyncio.sleep(0.8)
        
        yield f"event: result\ndata: {json.dumps(FALLBACK_REPORT)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.post("/optimize")
async def optimize(title: str = Form(""), content: str = Form(""), category: str = Form("food"), issues: str = Form(""), suggestions: str = Form(""), overall_score: int = Form(60)):
    """简化版优化建议 API"""
    return {
        "original_score": overall_score,
        "plans": [
            {
                "strategy": "标题优化",
                "optimized_title": f"🔥{title}｜亲测有效",
                "optimized_content": content,
                "key_changes": "添加情绪词和钩子",
                "score": overall_score + 8,
                "score_delta": 8,
                "recommended": True,
            },
            {
                "strategy": "内容重构",
                "optimized_title": title,
                "optimized_content": f"【核心要点】\n\n{content}\n\n💡 小贴士：记得点赞收藏哦！",
                "key_changes": "结构化排版，添加互动引导",
                "score": overall_score + 5,
                "score_delta": 5,
            },
            {
                "strategy": "标签强化",
                "optimized_title": title,
                "optimized_content": content,
                "key_changes": "添加热门标签",
                "score": overall_score + 10,
                "score_delta": 10,
            },
        ],
    }

@router.post("/generate-comments")
async def generate_comments(title: str = Form(""), content: str = Form(""), category: str = Form("food"), existing_count: int = Form(0)):
    """简化版评论生成 API"""
    return {"comments": FALLBACK_REPORT["simulated_comments"]}

@router.post("/screenshot/quick-recognize")
async def quick_recognize(file: Optional[UploadFile] = File(None), slot_hint: Optional[str] = Form(None)):
    """简化版截图识别 API"""
    return {
        "success": True,
        "slot_type": "content",
        "category": "food",
        "title": "懒人食谱｜5分钟搞定的美味",
        "content_text": "今天给大家分享一个超级简单的懒人食谱，只需要鸡蛋、米饭、酱油、葱花就够了。",
        "summary": "这是一篇美食类笔记，分享了一个简单的懒人食谱。",
        "confidence": 0.85,
    }
