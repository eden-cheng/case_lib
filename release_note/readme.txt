优点：
1. 参数，表格的行列关系都通过yaml的方式，如果场景库表格反复修改，只需要修改yaml即可，不需要动代码部分，后期可以通过自动化自动生成yaml
2. 六层嵌套满足不同筛选需求，留好了接口，便于拓展
3. 为后期GUI设计留好了调用的接口

要求：
对case库
1. summary中待替换的参数名，一定要与yaml中参数名保持一直

对yaml
1. relation.yaml中的行列关系，必须与case库中的关系一致
2. 参数yaml中的参数名必须与case库中summary部分的参数名一致
3. para，para_action，para_odd中及时后面是空的，也要写

说明：
六层嵌套满足不同筛选需求
1. 实车或仿真需求层：
   举例：veh_test还是hill_test
   实现：mian函数中做调用
2. feature层：
   举例：比如cc,ilc
   实现：通过函数调用或不调用
3. odd层：
   举例：对空载，满载，无目标，轿车目标，卡车目标做展开。
   实现：通过遍历预设的参数yaml文件夹
4. case一级目录：
   举例：比如cc_3
   实现：通过函数调或不调用
5. case二级目录：
   举例：比如noload时候，cc_3_1, cc_3_2，但是在payload时候只有cc_3_2或者没有cc_3的case
   实现：根据yaml中预设项筛选
6. 单个case的参数层：
   举例：比如3%常规坡道情况下，需要对20、40、60kph做测试，但是5%大坡道情况下，仅对40kph做展开。
   实现：根据yaml中不同odd参数与action参数的绑定关系
备注：除了上面的几层嵌套，还有yaml本身的嵌套关系。后续看看是否可以做些简化。

想法记录：
1. 开发一个excel转yaml的工具
2. relation.yaml 中行列关系，通过自动化抓取的方式实现
<<<<<<< HEAD:readme.txt
=======
3. 可以对生成后的case做二次整理，生成一张表格
>>>>>>> eden0318:release_note/readme.txt
