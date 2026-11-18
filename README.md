# 训练场预约页面与采集场次资料接续

现有项目保存训练场预约与设备表的冻结来源响应。transport 核对请求和原文字节，domain 提取来源声明的资料身份，ledger 原子保存版本，view 展示已收资料及待核状态。合成样例不访问外部站点，门户默认范围的稳定卡片已通过 portal_workflow 写入原文账本和持久采集收据，待采范围由 portal-sources.json 登记，重进时不会重复建版本；切换后的范围仍待业务采集逻辑接续。双来源初版资料已可按当前字段核对并判断发布；后续更正、撤回与范围变化尚待接续。来源字段见 docs/source-contract.md。

在项目根目录运行：

    python -m unittest discover -s tests -v
    python -m compileall -q capture_service tests
    python -m capture_service.cli inspect data/normal.json

本地页面演练：python -m capture_service.browser_capture data/portal.html。

容器运行：docker build -t robot-collection-005 .；docker run --rm robot-collection-005。
