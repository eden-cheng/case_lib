想法记录：
1. 开发一个excel转yaml的工具
3. 配置vscod的编译环境
4. 做两次展开，第一次将逻辑场景展开成带行为参数的case，第二次展开成带odd参数的case

0316改进：
1. 调整了case库文件的格式，比如
  1）区分实车测试和HILL测试的推荐测试
  2）推荐参数区分为odd和action
  3）将action和通过条件部分，从格式上往前移，避免后期tag频繁变更，需要调整行列关系
2. yaml中调整
  1）原para改为para_odd和para_action
  2）para_odd部分“1% uphill”改为“1%”，“500m curve”改为“500m“
3， 