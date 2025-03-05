# 🌟 SpectreCore (影芯) - 智能群聊互动插件

<div align="center">

![SpectreCore](https://avatars.githubusercontent.com/u/129108081?s=48&v=4)

[![version](https://img.shields.io/badge/version-v1.0-blue.svg?style=flat-square)](https://github.com/23q3/astrbot_plugin_SpectreCore)
[![license](https://img.shields.io/badge/license-AGPL--3.0-green.svg?style=flat-square)](LICENSE)
[![author](https://img.shields.io/badge/author-23q3-orange.svg?style=flat-square)](https://github.com/23q3)

*让 AI 成为群聊中最受欢迎的成员*

</div>

<p align="center">
  <a href="#-简介">简介</a> •
  <a href="#-特性">特性</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-使用技巧">使用技巧</a> •
  <a href="#-更新日志">更新日志</a>
</p>

---

## 📝 简介

<table>
<tr>
<td>

SpectreCore (影芯) 是一个为 AstrBot 设计的高级群聊互动插件，它能让大语言模型更好地参与到群聊对话中，带来生动和沉浸式的群聊体验。通过智能的消息处理和上下文理解，让 AI 像真实群友一样自然地参与讨论。

> 💡 **灵感来源**：本项目的灵感来自 [【当你发现聊了99+的群友是DeepSeek.......】](https://www.bilibili.com/video/BV1amAneGE3P)

</td>
</tr>
</table>

## ✨ 特性

- 🤖 **智能消息识别与回复** - 自动分析群聊上下文进行回复
- 🎭 **支持自定义 AI 人格设定** - 让 AI 拥有特定的性格与说话风格
- 📸 **支持图片理解和多模态互动** - 可以理解并回复包含图片的消息
- 📜 **群聊历史记录保存与上下文理解** - 记住之前的对话内容，保持连贯性
- ⚡ **高性能消息处理** - 高效处理大量群消息
- 🔧 **灵活的配置选项** - 可根据需求自定义插件行为
- 🔍 **支持读空气** - AI 可智能判断何时应该回复，何时保持沉默
- 📨 **高级消息格式处理**
  - ✓ 支持合并转发消息解析
  - ✓ 支持 @ 消息智能理解
  - ✓ 支持引用消息上下文关联
  - ✓ 自动将复杂消息转换为大模型可理解的格式

## 🚀 快速开始

### 安装

<details>
<summary>展开查看安装步骤</summary>

1. 首先确保已部署 AstrBot
2. 在插件市场中搜索 SpectreCore 点击安装
3. 或点击右下角加号，输入本插件仓库链接安装：
   ```
   https://github.com/23q3/astrbot_plugin_SpectreCore
   ```
4. 重启 AstrBot 使插件生效

</details>

### 配置

插件支持多种配置选项，可以在 AstrBot 的插件管理界面进行设置：

<div align="center">

| 配置项 | 说明 | 默认值 |
|:------|:-----|:-------|
| 群消息历史记录数量 | 记录的历史消息数量 | 20 |
| 图片处理数量 | 每次处理的最大图片数 | 0 |
| AI 人格设定 | 设定 AI 的性格与回复风格 | 默认 |
| 消息过滤规则 | 设置哪些消息需要回复 | 全部 |
| 读空气模式 | 是否启用智能判断回复 | 关闭 |

</div>

## 💡 使用技巧

### 如何让 AI 读空气？

<details>
<summary>展开查看详细设置</summary>

1. 在插件配置中开启读空气功能
2. 在人格设置中添加提示 比如：
   ```
   当群聊中出现以下情况时，请不要回复：
   1. 群友在讨论专业话题，而你无法提供有价值的见解
   2. 群内正在进行命令操作，不需要你的干扰
   3. 当话题与你无关，或者你的回复可能会打断当前的对话流
   ```
3. AI 会根据你设置的提示自动判断何时应该回复，何时保持沉默

</details>

## 🔧 支持的消息适配器

<div align="center">
  
| 平台 | 状态 | 说明 |
|:-----|:----:|:-----|
| aiocqhttp | ✅ | 完全支持 |

</div>

## 📋 更新日志

<details open>
<summary><b>最新版本</b></summary>

### v1.0.1 (2025-03-05)
- 🔍 增加了读空气功能
- 🔍 增加了函数工具开关配置
- 🔄 更换了request_llm方法调用大模型，提高兼容性
- 🛠️ 优化部分代码

</details>

<details>
<summary><b>历史版本</b></summary>

### v1.0.0 (2025-03-04)
- 🎉 首次发布
- ✨ 实现基本的群聊互动功能

</details>

## 🔗 可能感兴趣的项目

<div align="center">
<table>
<tr>
<td align="center">
<a href="https://github.com/SengokuCola/MaiMBot">
<img src="https://avatars.githubusercontent.com/u/25811392?s=48&v=4" width="80" alt="MaiMBot"><br>
<sub><b>MaiMBot (麦麦)</b></sub>
</a><br>
<sub>一款专注于群组聊天的赛博网友QQ机器人</sub>
</td>
</tr>
</table>
</div>

## ⚠️ 注意事项

- 代码部分由 AI 辅助生成，使用时请仔细甄别
- 本插件和AstarBot自带的主动回复功能之间没有任何联系，在使用本插件时请关闭AstarBot的主动回复功能，以免重复回复。
- 为避免不必要的响应，建议为开启读空气功能并为AI提示明确的回复条件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！

<details>
<summary>贡献者</summary>

- [23q3](https://github.com/23q3) - 主要开发者
- 感谢所有提供反馈和建议的用户！

</details>

## 📄 许可证

<details>
<summary>查看许可证信息</summary>

本项目采用 GNU Affero General Public License v3.0 (AGPL-3.0) 许可证。这意味着：

- ✅ 您可以自由使用、修改和分发本软件
- ✅ 如果您修改了本软件，必须开源您的修改
- ✅ 如果您通过网络提供本软件的服务，必须开源您的完整源代码
- ✅ 任何衍生作品必须使用相同的许可证（AGPL-3.0）

详细信息请查看 [LICENSE](LICENSE) 文件。

</details>

---

<div align="center">

**[SpectreCore (影芯)](https://github.com/23q3/astrbot_plugin_SpectreCore)** | Powered by [AstrBot](https://github.com/Soulter/AstrBot)

<sub>Made with ❤️ by [23q3](https://github.com/23q3)</sub>

</div>
