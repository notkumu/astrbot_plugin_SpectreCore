# SpectreCore - 智能群聊互动插件

<p align="center">
  <img src="https://img.shields.io/badge/version-v1.0-blue.svg" alt="version">
  <img src="https://img.shields.io/badge/license-AGPL--3.0-green.svg" alt="license">
  <img src="https://img.shields.io/badge/author-23q3-orange.svg" alt="author">
</p>

## 📝 简介

SpectreCore 是一个为 AstrBot 设计的高级群聊互动插件，它能让大语言模型更好地参与到群聊对话中，带来生动和沉浸式的群聊体验。通过智能的消息处理和上下文理解，让 AI 像真实群友一样自然地参与讨论。

## ✨ 特性

- 🤖 智能消息识别与回复
- 🎭 支持自定义 AI 人格设定
- 📸 支持图片理解和多模态互动
- 📜 群聊历史记录保存与上下文理解
- ⚡ 高性能消息处理
- 🔧 灵活的配置选项
- 📨 高级消息格式处理
  - 支持合并转发消息解析
  - 支持 @ 消息智能理解
  - 支持引用消息上下文关联
  - 自动将复杂消息转换为大模型可理解的格式

## 🚀 快速开始

### 安装
1. 部署 AstrBot
2. 在插件市场中 搜索SpectreCore 点击安装 或点击右下角加号 输入本插件仓库链接安装

### 配置
插件支持多种配置选项，可以在 AstrBot 的插件管理界面进行设置：

- 群消息历史记录数量
- 图片处理数量
- AI 人格设定
- 消息过滤规则
- 等等...

## 💡 使用技巧

### 如何让 AI 读空气？
1. 在 AstrBot 配置中启用"分段回复"
2. 关闭"仅对 LLM 结果分段"
3. 在过滤分段后的内容中填写 `<不发送消息>` 或自定义标签
4. 在人格设置中告诉 AI 在不需要发送消息时输出 `<不发送消息>`

## 🔧 支持的消息适配器
- aiocqhttp

## ⚠️ 注意事项
- 代码部分由 AI 辅助生成，使用时请仔细甄别
- 本插件和AstarBot自带的主动回复功能之间没有任何联系，在使用本插件时请关闭AstarBot的主动回复功能，以免重复回复。

## 🤝 贡献
欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！

## 📄 许可证
本项目采用 GNU Affero General Public License v3.0 (AGPL-3.0) 许可证。这意味着：

- ✅ 您可以自由使用、修改和分发本软件
- ✅ 如果您修改了本软件，必须开源您的修改
- ✅ 如果您通过网络提供本软件的服务，必须开源您的完整源代码
- ✅ 任何衍生作品必须使用相同的许可证（AGPL-3.0）

详细信息请查看 [LICENSE](LICENSE) 文件。