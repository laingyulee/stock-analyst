# stock-analyst
AI股票分析师

> 本项目旨在实现一个轻量级的股票价值分析系统
> 用户可以使用本地LLM和免费的金融数据源进行分析

## 逻辑核心

Fork自TradingAgents的prompts，并进行优化，调用多个LLM进行深度分析。
逻辑核心位于 `/skeleton`


## 回测流程

根据买卖建议进行模拟买卖，并计算收益率。
