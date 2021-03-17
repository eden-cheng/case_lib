要求：
1. relation.yaml中的行列关系，必须与case库中的关系一致
2. 参数yaml中的参数名必须与case库中summary部分的参数名一致

想法记录：
1. 开发一个excel转yaml的工具
3. 配置vscod的编译环境
4. 做两次展开，第一次将逻辑场景展开成带行为参数的case，第二次展开成带odd参数的case

0316改进：（程伟）
1. 调整了case库文件的格式，比如
  1）区分实车测试和HILL测试的推荐测试
  2）推荐参数区分为odd和action
  3）将action和通过条件部分，从格式上往前移，避免后期tag频繁变更，需要调整行列关系
2. yaml中调整
  1）调整了relation.yaml中的行列对应关系；
  2) 原para改为para_odd和para_action；
  3）para_odd部分“1% uphill”改为“1%”，“500m curve”改为“500m“；
3， 代码调整
  1）针对上面的yaml调整，对rule.py做修改；
  2）原先para_action部分也采用追加形式，现在修改为参数替换replace的方式。前一种方式，不同case需要不同的追加描述，后者适应性更好;
  3）通过上一步的改进，rule.py的适用性更好，不仅可以使用cc,而且可以使用ilc 