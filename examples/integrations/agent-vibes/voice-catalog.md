---
title: "语音目录"
description: "Agent Vibes 可用语音完整目录 — 按功能和语言分类"
tags: [integration, voice, catalog, audio]
---

# 语音目录

Agent Vibes 语音的完整目录。

## 概览

本文档列出了 Agent Vibes 中所有可用语音，包括：

- 英语语音（多口音）
- 多语言语音（20+ 种语言）
- 特殊用途语音（导航、新闻、对话等）
- 神经语音（高质量、自然发音）
- 标准语音（较低质量、更快响应）

## 语音引擎

Agent Vibes 支持多种语音引擎：

| 引擎         | 质量 | 延迟 | 离线 | 说明               |
| ------------ | ---- | ---- | ---- | ------------------ |
| Azure        | 高   | 低   | 否   | 默认引擎，神经 TTS |
| OpenAI       | 高   | 中   | 否   | 需要 API 密钥      |
| ElevenLabs   | 极高 | 中   | 否   | 高级语音克隆       |
| macOS        | 中   | 极低 | 是   | 系统内置 TTS       |
| Windows SAPI | 中   | 极低 | 是   | 系统内置 TTS       |
| eSpeak-NG    | 低   | 极低 | 是   | 轻量级离线 TTS     |

## Azure 神经语音

### 英语（美国）

| 语音 ID                   | 名称        | 性别 | 风格             | 建议用途             |
| ------------------------- | ----------- | ---- | ---------------- | -------------------- |
| `en-US-JennyNeural`       | Jenny       | 女   | 友好、清晰       | 通用、编程助手、教程 |
| `en-US-GuyNeural`         | Guy         | 男   | 专业、权威       | 技术文档、说明       |
| `en-US-AriaNeural`        | Aria        | 女   | 温暖、热情       | 创意写作、演示       |
| `en-US-DavisNeural`       | Davis       | 男   | 冷静、沉稳       | 调试、错误说明       |
| `en-US-JaneNeural`        | Jane        | 女   | 活泼、有活力     | 交互式对话           |
| `en-US-JasonNeural`       | Jason       | 男   | 中性、平衡       | 默认中性声音         |
| `en-US-SaraNeural`        | Sara        | 女   | 自然、流畅       | 叙述、长篇阅读       |
| `en-US-TonyNeural`        | Tony        | 男   | 友好、可靠       | 代码审查             |
| `en-US-NancyNeural`       | Nancy       | 女   | 成熟、温柔       | 文档阅读             |
| `en-US-AmberNeural`       | Amber       | 女   | 年轻、开朗       | 学习模式             |
| `en-US-AnaNeural`         | Ana         | 女   | 清晰、儿童友好   | 教育内容             |
| `en-US-AshleyNeural`      | Ashley      | 女   | 专业、清晰       | 企业培训             |
| `en-US-BrandonNeural`     | Brandon     | 男   | 深沉、权威       | 法律/合规文档        |
| `en-US-ChristopherNeural` | Christopher | 男   | 温暖、有磁性     | 播客式叙述           |
| `en-US-CoraNeural`        | Cora        | 女   | 柔软、舒缓       | 放松/冥想            |
| `en-US-ElizabethNeural`   | Elizabeth   | 女   | 高雅、专业       | 商业演示             |
| `en-US-EricNeural`        | Eric        | 男   | 专业、具有分析力 | 技术分析             |
| `en-US-JacobNeural`       | Jacob       | 男   | 年轻、有活力     | 现代内容             |
| `en-US-MichelleNeural`    | Michelle    | 女   | 友好、易于接近   | 客户服务             |
| `en-US-MonicaNeural`      | Monica      | 女   | 活泼、温暖       | 交互式内容           |
| `en-US-RogerNeural`       | Roger       | 男   | 成熟、可靠       | 正式文档             |

### 英语（英国）

| 语音 ID              | 名称   | 性别 | 风格         | 建议用途 |
| -------------------- | ------ | ---- | ------------ | -------- |
| `en-GB-SoniaNeural`  | Sonia  | 女   | 专业、清晰   | 正式文档 |
| `en-GB-RyanNeural`   | Ryan   | 男   | 友好、亲切   | 技术支持 |
| `en-GB-LibbyNeural`  | Libby  | 女   | 温暖、热情   | 创意内容 |
| `en-GB-MaisieNeural` | Maisie | 女   | 年轻、有活力 | 娱乐内容 |
| `en-GB-AbbiNeural`   | Abbi   | 女   | 清新、自然   | 教育内容 |

### 英语（澳大利亚）

| 语音 ID               | 名称    | 性别 | 风格       | 建议用途 |
| --------------------- | ------- | ---- | ---------- | -------- |
| `en-AU-NatashaNeural` | Natasha | 女   | 友好、活泼 | 通用     |

### 英语（加拿大）

| 语音 ID             | 名称  | 性别 | 风格       | 建议用途 |
| ------------------- | ----- | ---- | ---------- | -------- |
| `en-CA-ClaraNeural` | Clara | 女   | 清晰、友好 | 通用     |

### 英语（其他地区）

| 语音 ID                        | 名称     | 地区   | 建议用途 |
| ------------------------------ | -------- | ------ | -------- |
| `en-IN-NeerjaExpressiveNeural` | Neerja   | 印度   | 通用     |
| `en-IE-ConnorNeural`           | Connor   | 爱尔兰 | 通用     |
| `en-NZ-MitchellNeural`         | Mitchell | 新西兰 | 通用     |
| `en-SG-LunaNeural`             | Luna     | 新加坡 | 通用     |
| `en-PH-RosaNeural`             | Rosa     | 菲律宾 | 通用     |

## 中文语音

| 语音 ID                 | 名称 | 性别 | 风格       | 说明       |
| ----------------------- | ---- | ---- | ---------- | ---------- |
| `zh-CN-XiaoxiaoNeural`  | 晓晓 | 女   | 自然、清晰 | 普通话     |
| `zh-CN-YunxiNeural`     | 云希 | 男   | 友好       | 普通话     |
| `zh-CN-YunjianNeural`   | 云健 | 男   | 运动风格   | 普通话     |
| `zh-CN-XiaoyiNeural`    | 晓伊 | 女   | 温暖       | 普通话     |
| `zh-CN-YunyangNeural`   | 云扬 | 男   | 新闻风格   | 普通话     |
| `zh-TW-HsiaoChenNeural` | 晓臻 | 女   | 自然       | 台湾普通话 |
| `zh-HK-HiuMaanNeural`   | 曉曼 | 女   | 自然       | 香港粤语   |

## 日语语音

| 语音 ID              | 名称 | 性别 | 风格 | 说明 |
| -------------------- | ---- | ---- | ---- | ---- |
| `ja-JP-NanamiNeural` | 七海 | 女   | 专业 | 通用 |
| `ja-JP-KeitaNeural`  | 圭太 | 男   | 清晰 | 通用 |
| `ja-JP-AoiNeural`    | 葵   | 女   | 温暖 | 通用 |
| `ja-JP-DaichiNeural` | 大地 | 男   | 深沉 | 通用 |
| `ja-JP-MayuNeural`   | 真弓 | 女   | 柔和 | 通用 |
| `ja-JP-NaokiNeural`  | 直树 | 男   | 专业 | 通用 |

## 韩语语音

| 语音 ID              | 名称 | 性别 | 风格 |
| -------------------- | ---- | ---- | ---- |
| `ko-KR-SunHiNeural`  | 선희 | 女   | 友好 |
| `ko-KR-InJoonNeural` | 인준 | 男   | 专业 |
| `ko-KR-JiMinNeural`  | 지민 | 女   | 活泼 |

## 法语语音

| 语音 ID               | 名称    | 性别 | 风格 | 地区   |
| --------------------- | ------- | ---- | ---- | ------ |
| `fr-FR-DeniseNeural`  | Denise  | 女   | 专业 | 法国   |
| `fr-FR-HenriNeural`   | Henri   | 男   | 权威 | 法国   |
| `fr-CA-SylvieNeural`  | Sylvie  | 女   | 友好 | 加拿大 |
| `fr-CA-AntoineNeural` | Antoine | 男   | 温暖 | 加拿大 |
| `fr-CH-ArianeNeural`  | Ariane  | 女   | 高雅 | 瑞士   |

## 德语语音

| 语音 ID              | 名称   | 性别 | 风格 |
| -------------------- | ------ | ---- | ---- |
| `de-DE-KatjaNeural`  | Katja  | 女   | 专业 |
| `de-DE-ConradNeural` | Conrad | 男   | 权威 |
| `de-DE-LouisaNeural` | Louisa | 女   | 温暖 |

## 西班牙语语音

| 语音 ID              | 名称   | 性别 | 风格 | 地区   |
| -------------------- | ------ | ---- | ---- | ------ |
| `es-ES-ElviraNeural` | Elvira | 女   | 清晰 | 西班牙 |
| `es-ES-AlvaroNeural` | Alvaro | 男   | 专业 | 西班牙 |
| `es-MX-DaliaNeural`  | Dalia  | 女   | 友好 | 墨西哥 |
| `es-MX-JorgeNeural`  | Jorge  | 男   | 温暖 | 墨西哥 |

## 意大利语语音

| 语音 ID                | 名称     | 性别 | 风格 |
| ---------------------- | -------- | ---- | ---- |
| `it-IT-ElsaNeural`     | Elsa     | 女   | 专业 |
| `it-IT-IsabellaNeural` | Isabella | 女   | 热情 |
| `it-IT-DiegoNeural`    | Diego    | 男   | 友好 |

## 葡萄牙语语音

| 语音 ID                 | 名称      | 性别 | 风格 | 地区   |
| ----------------------- | --------- | ---- | ---- | ------ |
| `pt-BR-FranciscaNeural` | Francisca | 女   | 温暖 | 巴西   |
| `pt-BR-AntonioNeural`   | Antonio   | 男   | 专业 | 巴西   |
| `pt-PT-FernandaNeural`  | Fernanda  | 女   | 清晰 | 葡萄牙 |

## 其他语言

### 荷兰语

| 语音 ID               | 名称    | 性别 |
| --------------------- | ------- | ---- |
| `nl-NL-ColetteNeural` | Colette | 女   |
| `nl-NL-FennaNeural`   | Fenna   | 女   |

### 瑞典语

| 语音 ID             | 名称  | 性别 |
| ------------------- | ----- | ---- |
| `sv-SE-SofieNeural` | Sofie | 女   |

### 挪威语

| 语音 ID                | 名称     | 性别 |
| ---------------------- | -------- | ---- |
| `nb-NO-PernilleNeural` | Pernille | 女   |

### 丹麦语

| 语音 ID                | 名称     | 性别 |
| ---------------------- | -------- | ---- |
| `da-DK-ChristelNeural` | Christel | 女   |

### 芬兰语

| 语音 ID             | 名称  | 性别 |
| ------------------- | ----- | ---- |
| `fi-FI-SelmaNeural` | Selma | 女   |

### 波兰语

| 语音 ID                 | 名称      | 性别 |
| ----------------------- | --------- | ---- |
| `pl-PL-AgnieszkaNeural` | Agnieszka | 女   |

### 俄语

| 语音 ID                | 名称     | 性别 |
| ---------------------- | -------- | ---- |
| `ru-RU-SvetlanaNeural` | Svetlana | 女   |
| `ru-RU-DariyaNeural`   | Dariya   | 女   |

### 阿拉伯语

| 语音 ID               | 名称    | 性别 |
| --------------------- | ------- | ---- |
| `ar-SA-ZariyahNeural` | Zariyah | 女   |

### 土耳其语

| 语音 ID            | 名称 | 性别 |
| ------------------ | ---- | ---- |
| `tr-TR-EmelNeural` | Emel | 女   |

### 泰语

| 语音 ID                 | 名称      | 性别 |
| ----------------------- | --------- | ---- |
| `th-TH-PremwadeeNeural` | Premwadee | 女   |

### 印地语

| 语音 ID              | 名称   | 性别 |
| -------------------- | ------ | ---- |
| `hi-IN-SwaraNeural`  | Swara  | 女   |
| `hi-IN-MadhurNeural` | Madhur | 男   |

## 语音风格

某些语音支持多种风格：

| 语音 ID             | 风格                     | 说明               |
| ------------------- | ------------------------ | ------------------ |
| `en-US-GuyNeural`   | `newscast`               | 新闻播报和正式阅读 |
| `en-US-AriaNeural`  | `chat`                   | 对话式和口语化     |
| `en-US-AriaNeural`  | `customerservice`        | 客户服务场景       |
| `en-US-AriaNeural`  | `narration-professional` | 专业叙述           |
| `en-US-JennyNeural` | `assistant`              | 虚拟助手场景       |
| `en-US-JennyNeural` | `chat`                   | 对话式和口语化     |
| `en-US-JennyNeural` | `customerservice`        | 客户服务场景       |
| `en-US-JennyNeural` | `newscast`               | 新闻播报和正式阅读 |
| `en-US-JasonNeural` | `narration`              | 通用叙述           |

## 发音调整

使用 SSML（语音合成标记语言）执行高级语音调整：

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis">
  <voice name="en-US-JennyNeural">
    <prosody rate="slow" pitch="high">
      这是缓慢、高音调的发音。
    </prosody>

    <break time="500ms" />

    <prosody rate="fast" pitch="low">
      这是快速、低音调的发音。
    </prosody>

    <emphasis level="strong">
      这句话会特别强调。
    </emphasis>

    <say-as interpret-as="characters">
      API
    </say-as>

    读作字母 A-P-I，而非单词。
  </voice>
</speak>
```

## 语音定制

### 创建自定义语音

```bash
# 创建自定义语音配置
agent-vibes voice create my-voice \
  --engine azure \
  --voice "en-US-JennyNeural" \
  --style "chat" \
  --rate 1.1 \
  --pitch 1.0

# 使用自定义语音
agent-vibes config set voice "custom:my-voice"
```

### 语音预设

预设是为特定场景优化的预配置语音设置：

```bash
# 列出可用预设
agent-vibes voice presets list

# 使用预设
agent-vibes voice preset use "code-review"

# 创建自定义预设
agent-vibes voice preset create my-preset
```

### 可用预设

| 预设                | 语音                      | 速率 | 风格              | 说明                 |
| ------------------- | ------------------------- | ---- | ----------------- | -------------------- |
| `default`           | `en-US-JennyNeural`       | 1.0  | `friendly`        | 默认语音             |
| `code-review`       | `en-US-GuyNeural`         | 1.1  | `professional`    | 代码审查优化         |
| `tutorial`          | `en-US-JennyNeural`       | 0.9  | `assistant`       | 较慢、清晰的教程语音 |
| `storytelling`      | `en-US-AriaNeural`        | 1.0  | `narration`       | 叙述与叙事           |
| `debugging`         | `en-US-DavisNeural`       | 1.2  | `calm`            | 调试时更快语速       |
| `documentation`     | `en-GB-SoniaNeural`       | 1.0  | `professional`    | 正式文档阅读         |
| `language-learning` | `en-US-AmberNeural`       | 0.8  | `clear`           | 语言学习减速语音     |
| `presentation`      | `en-US-ElizabethNeural`   | 1.1  | `elegant`         | 演示优化             |
| `meditation`        | `en-US-CoraNeural`        | 0.8  | `soft`            | 冥想与放松           |
| `news`              | `en-US-GuyNeural`         | 1.2  | `newscast`        | 新闻风格播报         |
| `customer-service`  | `en-US-MichelleNeural`    | 1.0  | `customerservice` | 客户服务场景         |
| `podcast`           | `en-US-ChristopherNeural` | 1.0  | `warm`            | 播客式叙述           |
| `legal`             | `en-US-BrandonNeural`     | 1.0  | `authoritative`   | 法律/合规阅读        |

## 语音质量指标

| 指标       | 神经语音 | 标准语音 | 本地 TTS |
| ---------- | -------- | -------- | -------- |
| 自然度     | 极高     | 高       | 中等     |
| 音色准确度 | 极高     | 高       | 中低     |
| 纠正发音   | 优秀     | 良好     | 基础     |
| 情感表达   | 支持     | 有限     | 不支持   |
| 风格支持   | 支持     | 有限     | 不支持   |
| 延迟       | 中       | 低       | 极低     |
| 成本       | 付费     | 付费     | 免费     |

## 贡献

要贡献新语音或预设，请参阅[贡献指南](../CONTRIBUTING.md)。

---

_通过完美匹配的语音增强 AI 交互_
