case模板需要修改：
1. summary部分，不要涉及参数名，只做功能场景描述
2. 道路集合 “road_geo” 的标签分为：平直路，curve，hill
3. 库中的tag应该要根据hill，实车的tag在yaml中体现

改进：
1. 开发一个excel转yaml的工具
3. 配置vscod的编译环境
4. 做两次展开，第一次将逻辑场景展开成带行为参数的case，第二次展开成带odd参数的case