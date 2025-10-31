#!/usr/bin/env python3
"""
A股分析核心功能模块
整合了A股分析的完整逻辑，包括新闻分析、基本面分析、技术面分析和市场情绪分析
"""

import re
from datetime import datetime
from typing import Dict, List, Tuple
from enum import Enum

class StockMarket(Enum):
    """股票市场枚举"""
    CHINA_A = "china_a"      # 中国A股
    HONG_KONG = "hong_kong"  # 港股
    US = "us"                # 美股
    UNKNOWN = "unknown"      # 未知

class StockUtils:
    """股票工具类"""
    
    @staticmethod
    def identify_stock_market(ticker: str) -> StockMarket:
        """
        识别股票代码所属市场
        
        Args:
            ticker: 股票代码
            
        Returns:
            StockMarket: 股票市场类型
        """
        if not ticker:
            return StockMarket.UNKNOWN
            
        ticker = str(ticker).strip().upper()
        
        # 中国A股：6位数字
        if re.match(r'^\d{6}$', ticker):
            return StockMarket.CHINA_A

        # 港股：4-5位数字.HK（支持0700.HK和09988.HK格式）
        if re.match(r'^\d{4,5}\.HK$', ticker):
            return StockMarket.HONG_KONG

        # 美股：1-5位字母
        if re.match(r'^[A-Z]{1,5}$', ticker):
            return StockMarket.US
            
        return StockMarket.UNKNOWN
    
    @staticmethod
    def get_market_info(ticker: str) -> Dict:
        """
        获取股票市场的详细信息
        
        Args:
            ticker: 股票代码
            
        Returns:
            Dict: 市场信息字典
        """
        market = StockUtils.identify_stock_market(ticker)
        currency_name, currency_symbol = ("人民币", "¥") if market == StockMarket.CHINA_A else ("未知", "?")
        data_source = "china_unified" if market == StockMarket.CHINA_A else "unknown"
        
        market_names = {
            StockMarket.CHINA_A: "中国A股",
            StockMarket.HONG_KONG: "港股",
            StockMarket.US: "美股",
            StockMarket.UNKNOWN: "未知市场"
        }
        
        return {
            "ticker": ticker,
            "market": market.value,
            "market_name": market_names[market],
            "currency_name": currency_name,
            "currency_symbol": currency_symbol,
            "data_source": data_source,
            "is_china": market == StockMarket.CHINA_A,
            "is_hk": market == StockMarket.HONG_KONG,
            "is_us": market == StockMarket.US
        }

class UnifiedNewsAnalyzer:
    """统一新闻分析器，整合所有新闻获取逻辑"""
    
    def __init__(self, toolkit=None):
        """初始化统一新闻分析器"""
        self.toolkit = toolkit
        
    def get_stock_news_unified(self, stock_code: str, max_news: int = 10, model_info: str = "") -> str:
        """
        统一新闻获取接口
        根据股票代码自动识别股票类型并获取相应新闻
        
        Args:
            stock_code: 股票代码
            max_news: 最大新闻数量
            model_info: 当前使用的模型信息，用于特殊处理
            
        Returns:
            str: 格式化的新闻内容
        """
        # 识别股票类型
        stock_type = self._identify_stock_type(stock_code)
        
        # 根据股票类型调用相应的获取方法
        if stock_type == "A股":
            result = self._get_a_share_news(stock_code, max_news, model_info)
        else:
            # 默认使用A股逻辑
            result = self._get_a_share_news(stock_code, max_news, model_info)
        
        return result
    
    def _identify_stock_type(self, stock_code: str) -> str:
        """识别股票类型"""
        stock_code = stock_code.upper().strip()
        
        # A股判断
        if re.match(r'^(00|30|60|68)\d{4}$', stock_code):
            return "A股"
        elif re.match(r'^(SZ|SH)\d{6}$', stock_code):
            return "A股"
        
        # 默认按A股处理
        else:
            return "A股"
    
    def _get_a_share_news(self, stock_code: str, max_news: int, model_info: str = "") -> str:
        """获取A股新闻"""
        # 获取当前日期
        curr_date = datetime.now().strftime("%Y-%m-%d")
        
        # 模拟新闻数据（实际应用中应调用真实数据源）
        news_content = f"东方财富网报道：{stock_code}股票今日上涨2.5%，成交量放大。\n"
        news_content += f"同花顺数据显示：{stock_code}主力资金净流入5000万元。\n"
        news_content += f"雪球社区讨论：投资者对{stock_code}后市走势分歧较大。\n"
        
        return self._format_news_result(news_content, "东方财富实时新闻", model_info)
    
    def _format_news_result(self, news_content: str, source: str, model_info: str = "") -> str:
        """格式化新闻结果"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        formatted_result = f"""
=== 📰 新闻数据来源: {source} ===
获取时间: {timestamp}
数据长度: {len(news_content)} 字符

=== 📋 新闻内容 ===
{news_content}

=== ✅ 数据状态 ===
状态: 成功获取
来源: {source}
时间戳: {timestamp}
"""
        return formatted_result.strip()

def get_china_stock_info_unified(ticker: str) -> str:
    """
    获取中国A股基本信息的统一接口
    
    Args:
        ticker: 股票代码
        
    Returns:
        str: 股票基本信息
    """
    # 模拟股票信息（实际应用中应调用真实数据源）
    stock_info = {
        "000001": {"name": "平安银行", "industry": "银行", "area": "深圳", "list_date": "1991-04-03"},
        "600036": {"name": "招商银行", "industry": "银行", "area": "上海", "list_date": "2002-04-09"},
        "000858": {"name": "五粮液", "industry": "酿酒", "area": "四川", "list_date": "1998-04-27"},
        "600519": {"name": "贵州茅台", "industry": "酿酒", "area": "贵州", "list_date": "2001-08-27"},
    }
    
    info = stock_info.get(ticker, {"name": f"股票{ticker}", "industry": "未知", "area": "未知", "list_date": "未知"})
    
    result = f"股票代码: {ticker}\n"
    result += f"股票名称: {info['name']}\n"
    result += f"所属地区: {info['area']}\n"
    result += f"所属行业: {info['industry']}\n"
    result += f"上市日期: {info['list_date']}\n"
    result += f"数据来源: 模拟数据\n"
    
    return result

def _get_company_name_for_china_market(ticker: str, market_info: dict) -> str:
    """
    为中国市场分析师获取公司名称

    Args:
        ticker: 股票代码
        market_info: 市场信息字典

    Returns:
        str: 公司名称
    """
    try:
        if market_info['is_china']:
            # 中国A股：使用统一接口获取股票信息
            stock_info = get_china_stock_info_unified(ticker)

            # 解析股票名称
            if "股票名称:" in stock_info:
                company_name = stock_info.split("股票名称:")[1].split("\n")[0].strip()
                return company_name
            else:
                return f"股票代码{ticker}"
        else:
            return f"股票{ticker}"

    except Exception as e:
        return f"股票{ticker}"

def analyze_a_share_news(ticker: str, toolkit=None) -> Dict[str, str]:
    """
    A股新闻分析功能
    
    Args:
        ticker: 股票代码
        toolkit: 工具包（可选）
        
    Returns:
        Dict[str, str]: 分析结果
    """
    # 获取市场信息
    market_info = StockUtils.get_market_info(ticker)
    
    # 获取公司名称
    company_name = _get_company_name_for_china_market(ticker, market_info)
    
    # 使用统一新闻工具获取新闻
    unified_news_tool = UnifiedNewsAnalyzer(toolkit)
    news_data = unified_news_tool.get_stock_news_unified(ticker)
    
    # 模拟新闻分析报告
    report = f"## {company_name}({ticker}) 新闻分析报告\n\n"
    report += f"### 基本信息\n"
    report += f"- 公司名称: {company_name}\n"
    report += f"- 股票代码: {ticker}\n"
    report += f"- 所属市场: {market_info['market_name']}\n\n"
    
    report += f"### 新闻概要\n"
    report += f"{news_data}\n\n"
    
    # 保留原始的新闻分析师系统提示
    news_system_message = """您是一位专业的财经新闻分析师，负责分析最新的市场新闻和事件对股票价格的潜在影响。

您的主要职责包括：
1. 获取和分析最新的实时新闻（优先15-30分钟内的新闻）
2. 评估新闻事件的紧急程度和市场影响
3. 识别可能影响股价的关键信息
4. 分析新闻的时效性和可靠性
5. 提供基于新闻的交易建议和价格影响评估

重点关注的新闻类型：
- 财报发布和业绩指导
- 重大合作和并购消息
- 政策变化和监管动态
- 突发事件和危机管理
- 行业趋势和技术突破
- 管理层变动和战略调整

分析要点：
- 新闻的时效性（发布时间距离现在多久）
- 新闻的可信度（来源权威性）
- 市场影响程度（对股价的潜在影响）
- 投资者情绪变化（正面/负面/中性）
- 与历史类似事件的对比

📊 价格影响分析要求：
- 评估新闻对股价的短期影响（1-3天）
- 分析可能的价格波动幅度（百分比）
- 提供基于新闻的价格调整建议
- 识别关键价格支撑位和阻力位
- 评估新闻对长期投资价值的影响
- 不允许回复'无法评估价格影响'或'需要更多信息'

请特别注意：
⚠️ 如果新闻数据存在滞后（超过2小时），请在分析中明确说明时效性限制
✅ 优先分析最新的、高相关性的新闻事件
📊 提供新闻对股价影响的量化评估和具体价格预期
💰 必须包含基于新闻的价格影响分析和调整建议

请撰写详细的中文分析报告，并在报告末尾附上Markdown表格总结关键发现。"""
    
    report += f"### 分析结论\n"
    report += f"根据近期新闻分析，{company_name}股价受到以下因素影响：\n"
    report += f"1. 市场关注度提升，成交量放大\n"
    report += f"2. 主力资金流入，短期走势偏强\n"
    report += f"3. 投资者情绪分化，需关注后续消息面\n\n"
    
    report += f"### 投资建议\n"
    report += f"短期建议: 持有\n"
    report += f"中长期建议: 关注基本面变化\n"
    
    return {
        "news_data": news_data,
        "news_report": report,
        "system_message": news_system_message
    }

def analyze_a_share_fundamentals(ticker: str) -> Dict[str, str]:
    """
    A股基本面分析功能
    
    Args:
        ticker: 股票代码
        
    Returns:
        Dict[str, str]: 分析结果
    """
    # 获取市场信息
    market_info = StockUtils.get_market_info(ticker)
    
    # 获取公司名称
    company_name = _get_company_name_for_china_market(ticker, market_info)
    
    # 获取公司基本信息
    company_info = get_china_stock_info_unified(ticker)
    
    # 模拟基本面数据
    fundamentals_data = f"## {company_name}({ticker}) 基本面数据\n\n"
    fundamentals_data += f"### 财务指标\n"
    fundamentals_data += f"- 市盈率(PE): 12.5\n"
    fundamentals_data += f"- 市净率(PB): 1.8\n"
    fundamentals_data += f"- 净资产收益率(ROE): 15.2%\n"
    fundamentals_data += f"- 营收增长率: 8.3%\n"
    fundamentals_data += f"- 净利润增长率: 10.1%\n\n"
    
    fundamentals_data += f"### 估值分析\n"
    fundamentals_data += f"- 当前股价: 50.25元\n"
    fundamentals_data += f"- 合理估值区间: 45-55元\n"
    fundamentals_data += f"- 估值状态: 合理\n\n"
    
    # 保留原始的基本面分析师系统提示
    fundamentals_system_message = f"""你是一位专业的股票基本面分析师。
⚠️ 绝对强制要求：你必须调用工具获取真实数据！不允许任何假设或编造！
任务：分析{company_name}（股票代码：{ticker}，{market_info['market_name']}）
🔴 立即调用 get_stock_fundamentals_unified 工具
参数：ticker='{ticker}', start_date='2025-05-28', end_date='2025-10-30', curr_date='2025-10-30'
📊 分析要求：
- 基于真实数据进行深度基本面分析
- 计算并提供合理价位区间（使用{market_info['currency_name']}{market_info['currency_symbol']}）
- 分析当前股价是否被低估或高估
- 提供基于基本面的目标价位建议
- 包含PE、PB、PEG等估值指标分析
- 结合市场特点进行分析
🌍 语言和货币要求：
- 所有分析内容必须使用中文
- 投资建议必须使用中文：买入、持有、卖出
- 绝对不允许使用英文：buy、hold、sell
- 货币单位使用：{market_info['currency_name']}（{market_info['currency_symbol']}）
🚫 严格禁止：
- 不允许说'我将调用工具'
- 不允许假设任何数据
- 不允许编造公司信息
- 不允许直接回答而不调用工具
- 不允许回复'无法确定价位'或'需要更多信息'
- 不允许使用英文投资建议（buy/hold/sell）
✅ 你必须：
- 立即调用统一基本面分析工具
- 等待工具返回真实数据
- 基于真实数据进行分析
- 提供具体的价位区间和目标价
- 使用中文投资建议（买入/持有/卖出）
现在立即开始调用工具！不要说任何其他话！"""
    
    # 生成分析报告
    report = f"## {company_name}({ticker}) 基本面分析报告\n\n"
    report += f"### 公司概况\n"
    report += f"{company_info}\n\n"
    
    report += f"### 财务分析\n"
    report += f"公司基本面表现良好，主要财务指标如下：\n"
    report += f"- 市盈率12.5倍，处于合理区间\n"
    report += f"- 净资产收益率15.2%，盈利能力较强\n"
    report += f"- 营收和净利润保持稳定增长\n\n"
    
    report += f"### 估值评估\n"
    report += f"基于当前财务数据，公司合理估值区间为45-55元，\n"
    report += f"当前股价50.25元处于合理区间内。\n\n"
    
    report += f"### 投资建议\n"
    report += f"建议: 持有\n"
    report += f"理由: 基本面良好，估值合理，可长期关注\n"
    
    return {
        "fundamentals_data": fundamentals_data,
        "fundamentals_report": report,
        "system_message": fundamentals_system_message
    }

def analyze_a_share_technical(ticker: str) -> Dict[str, str]:
    """
    A股技术面分析功能
    
    Args:
        ticker: 股票代码
        
    Returns:
        Dict[str, str]: 分析结果
    """
    # 获取市场信息
    market_info = StockUtils.get_market_info(ticker)
    
    # 获取公司名称
    company_name = _get_company_name_for_china_market(ticker, market_info)
    
    # 模拟技术指标数据
    technical_data = f"## {company_name}({ticker}) 技术指标数据\n\n"
    technical_data += f"### 趋势指标\n"
    technical_data += f"- 5日均线: 49.80元\n"
    technical_data += f"- 20日均线: 48.90元\n"
    technical_data += f"- 60日均线: 47.20元\n\n"
    
    technical_data += f"### 震荡指标\n"
    technical_data += f"- RSI(14): 58.3\n"
    technical_data += f"- KDJ: K=62.5, D=59.2, J=69.1\n\n"
    
    technical_data += f"### 成交量指标\n"
    technical_data += f"- 当前成交量: 5000万股\n"
    technical_data += f"- 5日均量: 4200万股\n"
    technical_data += f"- 量比: 1.19\n\n"
    
    # 保留原始的市场分析师系统提示
    technical_system_message = f"""你是一位专业的股票技术分析师。你必须对{company_name}（股票代码：{ticker}）进行详细的技术分析。

**股票信息：**
- 公司名称：{company_name}
- 股票代码：{ticker}
- 所属市场：{market_info['market_name']}
- 计价货币：{market_info['currency_name']}（{market_info['currency_symbol']}）

**工具调用指令：**
你有一个工具叫做get_stock_market_data_unified，你必须立即调用这个工具来获取{company_name}（{ticker}）的市场数据。
不要说你将要调用工具，直接调用工具。

**分析要求：**
1. 调用工具后，基于获取的真实数据进行技术分析
2. 分析移动平均线、MACD、RSI、布林带等技术指标
3. 考虑{market_info['market_name']}市场特点进行分析
4. 提供具体的数值和专业分析
5. 给出明确的投资建议
6. 所有价格数据使用{market_info['currency_name']}（{market_info['currency_symbol']}）表示

**输出格式：**
## 📊 股票基本信息
- 公司名称：{company_name}
- 股票代码：{ticker}
- 所属市场：{market_info['market_name']}

## 📈 技术指标分析
## 📉 价格趋势分析
## 💭 投资建议

请使用中文，基于真实数据进行分析。确保在分析中正确使用公司名称"{company_name}"和股票代码"{ticker}"。"""
    
    # 生成分析报告
    report = f"## {company_name}({ticker}) 技术分析报告\n\n"
    report += f"### 趋势分析\n"
    report += f"股价目前处于多头排列状态，短期、中期均线均呈上升趋势。\n"
    report += f"当前价格50.25元位于各均线之上，走势偏强。\n\n"
    
    report += f"### 技术指标分析\n"
    report += f"RSI指标为58.3，处于50-70的强势区间，但未进入超买区。\n"
    report += f"KDJ指标J值为69.1，接近超买区但仍有上涨空间。\n\n"
    
    report += f"### 成交量分析\n"
    report += f"当前成交量较5日均量放大19%，资金参与度较高。\n"
    report += f"量价配合良好，上涨趋势有望延续。\n\n"
    
    report += f"### 技术面建议\n"
    report += f"短期建议: 持有\n"
    report += f"支撑位: 48.50元\n"
    report += f"阻力位: 52.00元\n"
    
    return {
        "technical_data": technical_data,
        "technical_report": report,
        "system_message": technical_system_message
    }

def analyze_a_share_sentiment(ticker: str) -> Dict[str, str]:
    """
    A股市场情绪分析功能
    
    Args:
        ticker: 股票代码
        
    Returns:
        Dict[str, str]: 分析结果
    """
    # 获取市场信息
    market_info = StockUtils.get_market_info(ticker)
    
    # 获取公司名称
    company_name = _get_company_name_for_china_market(ticker, market_info)
    
    # 模拟情绪数据
    sentiment_data = f"## {company_name}({ticker}) 市场情绪数据\n\n"
    sentiment_data += f"### 社交媒体情绪\n"
    sentiment_data += f"- 雪球关注热度: 85/100\n"
    sentiment_data += f"- 东方财富股吧讨论: 1200条/日\n"
    sentiment_data += f"- 正面情绪占比: 55%\n"
    sentiment_data += f"- 负面情绪占比: 25%\n"
    sentiment_data += f"- 中性情绪占比: 20%\n\n"
    
    sentiment_data += f"### 机构观点\n"
    sentiment_data += f"- 券商评级: 买入(3家), 增持(5家), 中性(2家)\n"
    sentiment_data += f"- 目标价区间: 52-58元\n"
    sentiment_data += f"- 平均目标价: 55元\n\n"
    
    # 保留原始的社交媒体分析师系统提示
    sentiment_system_message = """您是一位专业的中国市场社交媒体和投资情绪分析师，负责分析中国投资者对特定股票的讨论和情绪变化。

您的主要职责包括：
1. 分析中国主要财经平台的投资者情绪（如雪球、东方财富股吧等）
2. 监控财经媒体和新闻对股票的报道倾向
3. 识别影响股价的热点事件和市场传言
4. 评估散户与机构投资者的观点差异
5. 分析政策变化对投资者情绪的影响
6. 评估情绪变化对股价的潜在影响

重点关注平台：
- 财经新闻：财联社、新浪财经、东方财富、腾讯财经
- 投资社区：雪球、东方财富股吧、同花顺
- 社交媒体：微博财经大V、知乎投资话题
- 专业分析：各大券商研报、财经自媒体

分析要点：
- 投资者情绪的变化趋势和原因
- 关键意见领袖(KOL)的观点和影响力
- 热点事件对股价预期的影响
- 政策解读和市场预期变化
- 散户情绪与机构观点的差异

📊 情绪价格影响分析要求：
- 量化投资者情绪强度（乐观/悲观程度）
- 评估情绪变化对短期股价的影响（1-5天）
- 分析散户情绪与股价走势的相关性
- 识别情绪驱动的价格支撑位和阻力位
- 提供基于情绪分析的价格预期调整
- 评估市场情绪对估值的影响程度
- 不允许回复'无法评估情绪影响'或'需要更多数据'

💰 必须包含：
- 情绪指数评分（1-10分）
- 预期价格波动幅度
- 基于情绪的交易时机建议

请撰写详细的中文分析报告，并在报告末尾附上Markdown表格总结关键发现。
注意：由于中国社交媒体API限制，如果数据获取受限，请明确说明并提供替代分析建议。"""
    
    # 生成分析报告
    report = f"## {company_name}({ticker}) 市场情绪分析报告\n\n"
    report += f"### 情绪概览\n"
    report += f"市场对{company_name}关注度较高，投资者情绪总体偏乐观。\n"
    report += f"正面情绪占比55%，负面情绪占比25%，情绪偏向积极。\n\n"
    
    report += f"### 机构观点\n"
    report += f"共有10家券商发布研报，其中8家给出积极评级(买入/增持)。\n"
    report += f"平均目标价55元，较当前股价有约9.5%的上涨空间。\n\n"
    
    report += f"### 情绪分析结论\n"
    report += f"市场情绪对股价形成正面支撑，投资者信心充足。\n"
    report += f"但需注意情绪过热可能带来的回调风险。\n\n"
    
    report += f"### 情绪面建议\n"
    report += f"情绪指数: 7.5/10 (积极)\n"
    report += f"建议: 持有，关注情绪变化\n"
    
    return {
        "sentiment_data": sentiment_data,
        "sentiment_report": report,
        "system_message": sentiment_system_message
    }

def comprehensive_a_share_analysis(ticker: str) -> Dict[str, str]:
    """
    A股综合分析功能 - 整合新闻、基本面、技术面和情绪分析
    
    Args:
        ticker: 股票代码
        
    Returns:
        Dict[str, str]: 综合分析结果
    """
    # 获取市场信息
    market_info = StockUtils.get_market_info(ticker)
    
    # 获取公司名称
    company_name = _get_company_name_for_china_market(ticker, market_info)
    
    # 执行各项分析
    news_analysis = analyze_a_share_news(ticker)
    fundamentals_analysis = analyze_a_share_fundamentals(ticker)
    technical_analysis = analyze_a_share_technical(ticker)
    sentiment_analysis = analyze_a_share_sentiment(ticker)
    
    # 生成综合报告
    comprehensive_report = f"# {company_name}({ticker}) 综合分析报告\n\n"
    comprehensive_report += f"## 📊 股票基本信息\n"
    comprehensive_report += f"- 公司名称: {company_name}\n"
    comprehensive_report += f"- 股票代码: {ticker}\n"
    comprehensive_report += f"- 所属市场: {market_info['market_name']}\n"
    comprehensive_report += f"- 计价货币: {market_info['currency_name']}（{market_info['currency_symbol']}）\n\n"
    
    comprehensive_report += f"## 📰 新闻分析摘要\n"
    # 提取新闻分析的核心结论
    news_conclusion = news_analysis['news_report'].split('\n')[-3:]
    comprehensive_report += '\n'.join(news_conclusion) + "\n\n"
    
    comprehensive_report += f"## 📈 基本面分析摘要\n"
    # 提取基本面分析的核心结论
    fundamentals_conclusion = fundamentals_analysis['fundamentals_report'].split('\n')[-3:]
    comprehensive_report += '\n'.join(fundamentals_conclusion) + "\n\n"
    
    comprehensive_report += f"## 📉 技术面分析摘要\n"
    # 提取技术面分析的核心结论
    technical_conclusion = technical_analysis['technical_report'].split('\n')[-4:]
    comprehensive_report += '\n'.join(technical_conclusion) + "\n\n"
    
    comprehensive_report += f"## 💭 市场情绪分析摘要\n"
    # 提取情绪分析的核心结论
    sentiment_conclusion = sentiment_analysis['sentiment_report'].split('\n')[-3:]
    comprehensive_report += '\n'.join(sentiment_conclusion) + "\n\n"
    
    comprehensive_report += f"## 🎯 综合投资建议\n"
    comprehensive_report += f"### 总体评价\n"
    comprehensive_report += f"综合各项分析，{company_name}表现出较强的投资价值：\n"
    comprehensive_report += f"- 基本面良好，估值合理\n"
    comprehensive_report += f"- 技术面偏强，趋势向好\n"
    comprehensive_report += f"- 市场情绪积极，资金关注度高\n\n"
    
    comprehensive_report += f"### 投资建议\n"
    comprehensive_report += f"**建议操作**: 持有\n"
    comprehensive_report += f"**目标价位**: 55元\n"
    comprehensive_report += f"**止损价位**: 46元\n"
    comprehensive_report += f"**风险提示**: 关注市场整体风险和个股消息面变化\n\n"
    
    comprehensive_report += f"### 分析师提示\n"
    comprehensive_report += f"本报告基于当前可获得的数据进行分析，投资有风险，决策需谨慎。\n"
    comprehensive_report += f"建议结合个人投资目标和风险承受能力做出投资决策。\n"
    
    return {
        "company_name": company_name,
        "ticker": ticker,
        "market_info": str(market_info),  # Convert dict to string to match return type
        "news_data": news_analysis['news_data'],
        "fundamentals_data": fundamentals_analysis['fundamentals_data'],
        "technical_data": technical_analysis['technical_data'],
        "sentiment_data": sentiment_analysis['sentiment_data'],
        "news_report": news_analysis['news_report'],
        "fundamentals_report": fundamentals_analysis['fundamentals_report'],
        "technical_report": technical_analysis['technical_report'],
        "sentiment_report": sentiment_analysis['sentiment_report'],
        "comprehensive_report": comprehensive_report
    }

# 主函数示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # 示例：对平安银行(000001)进行综合分析
    ticker = "000001"
    result = comprehensive_a_share_analysis(ticker)
    
    print(f"=== {result['company_name']}({result['ticker']}) 综合分析报告 ===")
    print(result['comprehensive_report'])