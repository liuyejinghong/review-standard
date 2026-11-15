# 证据、不采用理由与待校准项

本文件说明 `SKILL.md` 各条规则的依据。执行审查不必读本文件。

证据标签：

- `实测`：源码核对，或有样本的研究。
- `声称`：厂商或规范文档的说法。
- `推断`：本框架的归纳，没有直接证据。
- `作者实测`：作者在自己项目上的一次实测。范围是单一项目的单一特性，共 8 轮审查，其中 5 轮是双审。样本小，不能当作普遍结论。
- `估算`：没有实测的 token 数字，必须由对照实验校准。
- `FSR`：吸收自作者早期项目 full-spectrum-review v0.13.0（<https://github.com/liuyejinghong/full-spectrum-review>）。该项目的规则来自作者的审计经验，没有对照实验。它自带一次小型种子案例的回归记录，该记录自己写明不证明跨项目准确率和误报率。本标准吸收后没有重跑。标 `FSR` 的规则，强度一律按 `推断` 看待。

## 作者项目实测摘要

| 项 | 结果 |
|---|---|
| 审查发现的真问题 | 8 个，其中高严重度 6 个 |
| 高严重度真问题的发现方 | 2 个两路都报；4 个只由合同追踪路发现，全部属于身份、未知结果、合同类 |
| 全维度路（未沿合同追踪）的漏检 | 高严重度 4/6；全维度路的独有发现只有文档类小问题 |
| 合同追踪路的漏检 | 高严重度 0/6 |
| 审查者全部漏掉的真问题 | 1 个，属于未知结果处理。主控读实现报告时发现 |
| 复审的产出 | 3 轮复审中 2 轮只产出 1 个小问题和 1 条误报；另 1 轮产出 2 个高严重度真问题，都位于修复触及的高风险面 |
| 误报 | 合同追踪路 4/9，全维度路 0/3。4 条都属于推测性加校验、既有规则、不可达路径 |
| 小改双审 | 1 次，产出 0 个真问题和 1 条误报 |

漏检问题的形态，供 A 路任务书参考：

- 外部调用确认对象已进入终态后，同一次调用仍按调用前读到的旧状态继续动作。
- 把服务端错误响应里携带的“对象不存在”错误码当作对象不存在的证据。
- 结果未知的操作经精确查询得到“不存在”或终态后，仍然只查询，不推进状态。

限制：

- 两路的差异可能来自岗位配置（工具集、effort、任务书），不一定来自审法或模型。
- 发现方统计按调研摘要和主控裁决推算，没有回到原始记录逐条重数。
- harness 汇报的子代理 token 值是最后一次请求的上下文大小。一次审查的账面值是 37,514，峰值是 237,104。作者项目的 token 数字只能当粗略量级。

## 规则的来源与证据强度

| 规则（SKILL.md 位置） | 证据 | 强度 |
|---|---|---|
| 准入条件；不报表扬、纯提问、未来工作 | Microsoft 对 150 万条评论的研究：这三类多被作者判为无用（MSR 2015） | `实测` |
| 报告有可度量代价的代码健康问题 | 人类研究中缺陷评论约占 14%，代码改进约占 29%；只报 bug 会漏掉 D3 到 D8（Bacchelli & Bird 2013） | `实测`；作者已裁定 |
| 分级用确定性信号 | 没有公开工具把确定性风险信号接到审查强度上 | `推断`；阈值待校准 |
| 默认高风险面清单 | 归纳自作者项目高严重度问题的类别 | `推断`；作者已裁定内置、项目可覆盖 |
| P1 确定性检查先行 | Google、Microsoft 规范；Meta RADAR 的漏斗 | `声称`；`实测`（观察性） |
| P2 文件过滤 | PR-Agent、CodeRabbit、Graphite 的实现 | `实测` 实现；节省量未测 |
| P3 约 400 行 | Cisco 研究：超过 400 行缺陷发现下降（2006，单一产品组）；SWR-Bench：5 处以上改动的 PR 召回率从 38.35% 降到 8.88% | `实测`；人类数字，不能直接换算 token |
| P4 任务书写明既有规则与不可达前提 | 合同追踪路的 4 条误报都能由任务书预先排除 | `作者实测`，n=4 |
| P5 实现报告；主控自己读 | 审查者都漏掉的 1 个真问题由主控读报告发现 | `作者实测`，n=1 |
| L0 保留 1 位轻量核对 | RADAR：风险漏斗后 60.31% 自动通过，revert 约为对照的 1/3。RADAR 依赖训练过的风险评分 | `实测`（观察性）；作者已裁定保留核对 |
| L1 一位一遍全维度 | Google：中位审查者 1 人；作者项目小改双审无产出 | `实测`；`作者实测`，n=1 |
| L2 两位独立审查者 | Rigby & Bird：2 位审查者发现的缺陷与 4 位一样多；Greptile 关于失败相关性的论证 | `实测`；`声称` |
| L2 A 路必须有、不降配 | 4 个高严重度独有问题全部来自合同追踪 | `作者实测`，5 个双审轮 |
| L2 分路代替两遍全维度 | 第 2 遍全维度审查没有新增高严重度发现。“B 路的轻量上下文足够”没有实测 | `作者实测`；置信度中等，对照期内待定 |
| A 路逐个走通返回分支 | 3 个真问题都出在这类分支上。能否拦住同类问题没有实测 | `作者实测`；`推断` |
| L3 合并为 3 路 | D1/D2/D5 共享调用链上下文，D3/D4/D6 共享结构视图；多代理约为对话 15 倍的 token（research 任务） | `推断`；`声称` |
| effort 默认值 | 没有审查场景的对照证据 | `推断` |
| diff 为起点，按需读取 | Bugbot：按需读取是其 40 次实验中最大的单项质量增益；SWR-Bench：48% 误报来自缺上下文，更多仓库上下文会分散注意 | `声称`；`实测` |
| 稳定前缀、首尾位置、错开启动 | Claude Code 文档：缓存按前缀精确匹配；缓存读约为基价的 0.1 倍；长上下文中段召回最低（Lost in the Middle、RULER） | `声称`；`实测`；命中率未测 |
| 发现先落盘、压缩后重读 | OCR 与 Kodus 的压缩实现；作者项目 A 路 1 次审查在结束前被压缩 84% | `实测`；`作者实测` |
| 只核实候选发现；只删被证伪的 | Claude Code 官方 code-review 插件的结构；open-code-review 的 review filter 设计；HalluJudge 验证器 F1 0.85 | `实测` |
| 跨路去重 | Bugbot、PR-Agent 的实现 | `声称`；`实测` 实现 |
| 输出不写完整补丁 | 要求解释加修复的 prompt 提高误判率（arXiv 2603.00539） | `实测` |
| 结论判定顺序；`INCOMPLETE` | PR-Agent：装不下就换模型或分块，并列出未审文件 | `实测`，源码 |
| 单个 `APPROVE` 不是放行证据 | 1 轮中一位 approve，另一位报告的 2 个高严重度问题都成立 | `作者实测` |
| R1 | Google eng-practices | `声称` |
| R3 | OCR：一轮无新增即停；Rigby & Bird | `实测` |
| R4 | 不触及高风险面的复审产出低；PR-Agent 用发现状态避免重提 | `作者实测`；`实测` |
| R5 | 8 个真问题里 2 个在复审中发现，都位于修复触及的高风险面 | `作者实测` |
| R6 的 30% | 各工具都保留全量出口；具体数字没有依据 | `声称`；起步值 |
| 记账 3 项 | harness 账面值与峰值相差数倍 | `作者实测`，`实测`；作者已裁定 |
| 模式按审查对象判断 | 两种模式的起点和产出不同；触发方式与对象可以不一致 | `推断`；作者已裁定 |
| 存量审查：按高风险面、改动频率、事故记录排序，分批审，列出未审模块 | OWASP Code Review Guide 的按风险取舍思路。排序规则和“高/中/低”的划分没有实测 | `声称`；`推断` |
| 存量审查：“高”级模块派 A 路与全维度两路 | 作者项目实测全维度路漏检合同类问题 4/6，故合同追踪单独成路（召回优先于少读一遍）。A 路在没有 diff 的现存代码上是否同样有效，没有实测 | `推断` |
| 存量审查：核实 `阻断`、`阻断待核实`、触及高风险面的 `应改` | 沿用 L2 与 L3 的核实范围之间的折中，没有实测 | `推断` |
| D4 四步审法与强制反证；无历史时至少 2 类反证来源（`necessity.md` 第 1 节） | `FSR` 的 first-principles-review。“2 类”这个数字没有依据 | `推断`；起步值 |
| 补丁堆考古（`necessity.md` 第 2 节） | `FSR` 的 first-principles-review | `推断` |
| 业务语义 4 个检查面；意图无法确认时不造发现（`necessity.md` 第 3 节） | `FSR` 的 business-logic-review。本标准只取 4 个面，其余与 D1、D2 重叠 | `推断` |
| 有界集合逐成员枚举，采样不算已审（第 4 节） | `FSR` 的 orchestration-protocol。逻辑依据：集合按最弱成员失效 | `推断` |
| 按根因去重（第 6 节） | `FSR` 的 finding-protocol。替换 0.1.0 的“同文件同行且失败场景相同”：旧规则会把同一行上不同根因的发现合并，也不合并散在多处的同根因症状 | `推断` |
| 已接受权衡不重报；发现的 `status` 字段（第 5 节） | `FSR` 的 finding-protocol；PR-Agent 用发现状态避免重提 | `推断`；`实测` 实现 |
| 按真实暴露面定级；频率标实测或推断（第 5 节） | `FSR` 的 finding-protocol。作者项目的误报里有“不可达路径”一类，方向一致，但不是同一条规则的实测 | `推断` |
| 测试通过是证据不是证明（第 6 节） | `FSR`；与 D7“现有测试在缺陷下仍然通过”的准入一致 | `推断` |
| 主控采信高严重度发现前先复述机制（第 6 节） | `FSR` 的 orchestration-protocol | `推断` |
| 任务书额外上下文的准入测试（P4） | `FSR` 的 orchestration-protocol；SWR-Bench：更多上下文会分散注意 | `推断`；`实测`（间接） |
| 同一次审查固定同一提交；head 变动的处理（3.3） | `FSR` 的 exact-revision 规则；PR-Agent 列出未审部分的做法 | `推断` |
| 存量审查：入口、可变事实、外部边界 3 张清单 | `FSR` 的审计计划做法 | `推断` |
| 存量审查产出：值得保留的设计、待确认问题 | `FSR` 的 reporting 做法。没有作者反驳时，这两项防止整改顺手删掉有理由的约束、防止把意图不明写成缺陷 | `推断` |
| 回归网（`evals/`） | `FSR` 的 evals。4 个案例的陷阱机制取自 `FSR`；夹具改写为中性领域（审计事件导出、提交服务、告警回放、批量迁移），期望文件按本标准术语重写。2026-11-13 首次运行 4/4 通过，见 `evals/results/2026-11-13-v0.2.0.md` | 实测（单次） |
| 内置 `/code-review` 的发现也要核实 | 官方文档没有写明本机运行的 `/code-review` 各 effort 是否有独立核实阶段 | 未知 |

### 0.3.0 新增规则

强度分三档：强、中、推断；括号内注明对应的原有证据标签。

| 规则（SKILL.md 位置） | 来源 | 强度 |
|---|---|---|
| P1 包含为本次改动事先准备的确定性核对 | Factory 的任务规范要求写明要跑的检查、由证据判断完成：<https://factory.com/articles/coding-agent-task-specifications>；Agentless 用回归与复现测试做 patch validation：<https://arxiv.org/html/2407.01489v2>；SWE-agent 的 linter gate 直接拒收无效编辑：<https://arxiv.org/html/2405.15793v3>；Claude Code 最佳实践要求给代理可运行、返回通过与失败的检查：<https://code.claude.com/docs/en/best-practices> | 强（`声称` + `实测`；把调用点脚本列为 P1 是 `推断`） |
| P3 结构改动与行为改动拆成不同审查单元 | Beck：同一提交不混结构改动与行为改动，结构改动用改前改后同一组测试提供行为不变的证据：<https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes>；Google 小 CL：重构与功能/修复分开提交：<https://google.github.io/eng-practices/review/developer/small-cls.html> | 强（`声称`；Beck 的两句出自该文附录给 AI 的规则，不是正文论述） |
| P5 实现报告新增两项必填：(a) 关键事实配测试与反向验证证据；(b) 既有测试改动逐条对应事先批准的规则或测试变更项 | (a) Google 评审标准问“代码坏了测试会不会失败”：<https://google.github.io/eng-practices/review/reviewer/looking-for.html>；Google 变异测试中 1,159,723 个变异体、>87% 被杀：<https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46584.pdf>；Agentless 的复现测试只有 213/300 在原仓库复现，测试本身也要验证：<https://arxiv.org/html/2407.01489v2>。(b) Google 小 CL：重构不动测试，行为改动显式改测试：<https://google.github.io/eng-practices/review/developer/small-cls.html>；Factory：审查者不必猜缺失的测试是否有意：<https://factory.com/articles/reviewing-agent-generated-pull-requests> | 中（`声称` + `实测` 间接；把反向验证和测试变更单列为报告必填是 `推断`） |
| 第 3 节只跑定向测试、反向验证用隔离副本；D7 抽查 1–2 条反向验证 | Factory 测试影响分析：按改动选最可能发现回归的测试，选择逻辑放脚本，不确定时扩大集合：<https://factory.com/articles/test-impact-analysis-coding-agents>；Devin Review 在后续 push 时携带上一轮 finding，核对新提交是否修复：<https://docs.devin.ai/work-with-devin/devin-review>；Google 的“代码坏了测试会不会失败”用于抽查：<https://google.github.io/eng-practices/review/reviewer/looking-for.html> | 中（`声称` + `推断`；不重跑全量的节省幅度未测） |
| R7 只有已成立的阻断触发返工轮 | Google 评审标准：CL 确实改善整体代码健康就应批准，小建议标 Nit：<https://google.github.io/eng-practices/review/reviewer/standard.html>；Factory Review 分级中 P0 合并/部署前必修、P1 完成前必修：<https://docs.factory.com/onboarding/configuring-your-review-droid/review-droid-guidelines> | 中（`声称`；应改与可选的具体去向由主控决定，无对照数据） |

### 0.4.0 新增规则

| 规则（SKILL.md 位置） | 来源 | 强度 |
|---|---|---|
| R8 重复发现转为常驻确定性检查，白名单只减不增 | pstack 作者 poteto 的演讲 “All Code Is Slop (Except Mine)”：每次纠正代理，先改成确定性检查或用 API/架构消除，规则文本放最后；代理会照抄代码库里的既有写法（来源为用户提供的中文译稿，原始链接未核） | 推断（`声称`，无对照数据） |
| D5 新增“注释为绕过辩护” | 同一演讲：代理在注释与文档里为没做对找理由，注释不可强制执行 | 推断（`声称`） |
| D7 新增“时序缺陷只测一种顺序” | 同一演讲提到基于属性的测试已抓到 UI 缺陷；作者项目实测：一次关轮修复后的竞态由审查者手工注入时序才复现 | 推断（`声称` + 单例 `实测`） |

## 对照轮用 3 个 run 的权衡

对照轮跑 3 个 run：审查者甲 A 路、审查者甲全维度、审查者乙 B 路。审查者乙全维度只在审查者甲全维度漏掉审查者甲 A 路独有的高严重度真问题时补跑。

- 得到的：对照轮的常规成本从 4 个 run 降到 3 个。审查者甲的两个 run 已能回答首要问题：同一配置下，合同追踪是否比全维度多发现高严重度问题。
- 放弃的：审查者乙上“B 路对全维度”的对比不是每轮都有。“两遍全维度”的合并召回只在补跑的轮次里有完整数据。
- 补跑条件的理由：审查者甲全维度没有漏检时，第 2 遍全维度不改变“两遍全维度是否漏掉 A 路问题”的答案。漏检时才需要知道第 2 遍能否补上。
- 选择标准的理由：对照要回答的是高严重度问题的召回。不触及高风险面核心路径的改动产生不了这类样本，只增加成本。

## 不采用清单

| 做法 | 不采用的原因 |
|---|---|
| 跳过变更行、不读测试 | 直接降低标准。Google 规范要求读每一行 |
| 为省 token 调低 effort | 官方文档说明低 effort 减少边界覆盖 |
| 发现数量上限 | 会静默丢弃真发现。数量由严重度排序和准入条件控制 |
| 标量置信度阈值代替核实 | Claude 插件已从“0 到 100 分、阈值 80”改为逐条核实；没有公开对照证明分数足够 |
| 同一审法重复跑 n 遍再投票 | 有利证据：SWR-Bench 中 Gemini Flash 采样 5 遍聚合的 F1 为 20.48，高于 Gemini-2.5-Pro 单遍的 19.38，每个 PR 成本 $3.68e-3 对 $5.86e-3（`实测`）。不采用的原因：两者 F1 都在 20% 左右，没有强模型上的对照；投票会淘汰只出现一次的真发现，而作者项目 4 个高严重度独有问题都只有 1 位审查者报告。作者裁定：列为低优先级实验，不进默认流程 |
| 超过 2 遍的全量审查 | 2 位之后收益递减（Rigby & Bird） |
| 预装整个仓库或代码图索引 | 整仓上下文分散注意；图索引的构建成本和过期风险不在 token 账内 |
| 压缩或截断 diff | 截断后的审查不完整，却容易被当作完整审查 |
| 自建工具历史压缩 | 压缩属于 harness。自建会与 harness 的压缩叠加 |
| 只做增量审查 | 漏掉跨提交的合同破坏 |
| 审查者省略项目规则 | 省下的是最高标准本身 |
| 8 个维度各开一路 | 共享上下文的维度拆开后重复读取同样的材料 |
| L0 无审查自动通过 | RADAR 的做法依赖训练过的风险评分。作者项目没有分级准确率数据 |
| 默认使用 `/code-review ultra` | 误报率和与本机 `/code-review` 的对比数据都没有公开；每次约 $5 到 $25。作者裁定不默认使用 |
| 审查中调用 `/simplify` | `/simplify` 直接修改被审工作区的代码，审查是只读的。D4、D6 的发现成立后，由作者或主控决定是否用 `/simplify` 修复 |

## 待校准项

所有阈值都绑定当前模型代际。主控取得实测数据后，直接修改 `SKILL.md` 中的数值，并在本节记录依据。

1. L2 的两种编排。按 `SKILL.md` 3.1 的对照期规则收集数据后保留一种。“5 个对照轮、2 个以上特性”和“每个特性 1 到 2 轮”是起步值。
2. 约 400 行的规模阈值。不同语言每行的 token 数差异大，必须在目标仓库测量。
3. R6 的 30%。
4. 分级的准确率。L0 是否可以免审取决于这个数字。
5. 所有 `估算` 的节省幅度：L0 约 -90%，L1 约 -50%，L2 分路 -15% 到 -30%，窄化复审约 -50%。没有公开研究报告 LLM 代码审查的 token 消耗。
6. 并行子代理的缓存实际命中率。
7. effort 默认值。
8. 作者项目实测摘要里的发现方统计，必须回到原始记录重数一次。
9. 存量审查的重点排序。3 项信号的权重、“改动频率居项目前列”的界线、取多长的版本历史，都没有校准。校准方法：记录每批的真问题数，核对排序靠前的批次是否产出更多高严重度真问题。
10. 存量审查的分路方式（按模块或按维度）和单路能读完的模块规模。没有实测。
11. 存量审查中“高”级模块派两路的成本是否值得：若实际使用中全维度路已能覆盖 A 路发现，可考虑合并为一路。
12. 存量审查的核实范围。不核实的 `应改` 里误报占多少，没有数据。

13. 回归网。4 个案例在本标准下还没有跑过；通过标准和运行时机是起步值。案例数少，只覆盖 4 种陷阱形态。
14. `necessity.md` 的按需读取。B 路、乙路多读约 80 行是否值得，以及审查者是否真的按 4 步执行，没有实测。
15. R5（高风险修复复审保持 L2）对很小的修复 diff 是否可降为单人加 A 路审法。需要对照数据，未校准前 R5 不变。

开放问题：

- 质量基线宜用历史事故和已裁决的审查发现组成回放集。只用种子缺陷不能证明质量不降。
- 最小充分上下文没有定论。hunk、所在函数、调用方、测试、schema 各防哪类漏报，要按缺陷类型做消融。
- 大改动分块后的跨块不变量是已知盲区。当前靠 P3 拆分和 A 路全上下文追踪缓解。
- 检查单对 LLM 是提高召回还是诱导过度报告，没有定论。
- 没有可运行测试的项目，核实只能靠代码走查。这种核实对 D2 和 D4 是否足够，未知。
- 紧急变更通道由项目规则决定。事后补审按原等级执行，等级不因已合入而降低。

## 参考来源

人类审查规范与研究

- Google Engineering Practices：<https://google.github.io/eng-practices/review/reviewer/standard.html>、<https://google.github.io/eng-practices/review/reviewer/looking-for.html>、<https://google.github.io/eng-practices/review/reviewer/navigate.html>、<https://google.github.io/eng-practices/review/developer/small-cls.html>、<https://google.github.io/eng-practices/review/emergencies.html>
- Kent Beck，Augmented Coding: Beyond the Vibes：<https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes>
- Sadowski 等，Modern Code Review: A Case Study at Google（ICSE-SEIP 2018）：<https://storage.googleapis.com/gweb-research2023-media/pubtools/4476.pdf>
- Software Engineering at Google 第 9 章：<https://abseil.io/resources/swe-book/html/ch09.html>
- Bosu 等，Characteristics of Useful Code Reviews（MSR 2015）：<https://amiangshu.me/papers/CodeReview-MSR-2015.pdf>
- Bacchelli & Bird，Expectations, Outcomes, and Challenges of Modern Code Review（ICSE 2013）：<https://sback.it/publications/icse2013.pdf>
- Rigby & Bird，Convergent Contemporary Software Peer Review Practices（FSE 2013）：<https://users.encs.concordia.ca/~pcr/paper/Rigby2013FSE.pdf>
- Cisco/SmartBear 现场研究（2006）：<https://static1.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf>
- Meta RADAR：<https://arxiv.org/pdf/2605.30208>
- Microsoft Code With Engineering Playbook：<https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/>
- OWASP Code Review Guide v2：<https://wiki.owasp.org/index.php/OWASP_Code_review_V2_Table_of_Contents>、<https://wiki.owasp.org/index.php/CRV2_RiskBasedApproach>

AI 审查工具（源码或文档）

- Qodo PR-Agent：<https://github.com/qodo-ai/pr-agent/blob/main/pr_agent/algo/pr_processing.py>、<https://github.com/qodo-ai/pr-agent/blob/main/pr_agent/algo/token_budget.py>、<https://github.com/qodo-ai/pr-agent/blob/main/pr_agent/algo/file_filter.py>、<https://github.com/qodo-ai/pr-agent/blob/main/pr_agent/algo/review_merge.py>
- Alibaba open-code-review：<https://github.com/alibaba/open-code-review/blob/main/internal/agent/agent.go>、<https://github.com/alibaba/open-code-review/blob/main/internal/config/template/prompts/review_filter_task_system.md>、<https://github.com/alibaba/open-code-review/blob/main/internal/llmloop/compression.go>
- Claude Code 官方 code-review 插件：<https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md>
- Kodus：<https://github.com/kodustech/kodus-ai/blob/main/libs/agent-harness/infrastructure/compression/context-compressor.ts>
- Cursor Bugbot：<https://cursor.com/blog/building-bugbot>
- CodeRabbit：<https://www.coderabbit.ai/blog/context-engineering-ai-code-reviews>
- Graphite：<https://graphite.com/guides/ai-code-review-context-full-repo-vs-diff>
- Factory：任务规范 <https://factory.com/articles/coding-agent-task-specifications>、审查 agent 生成的 PR <https://factory.com/articles/reviewing-agent-generated-pull-requests>、测试影响分析 <https://factory.com/articles/test-impact-analysis-coding-agents>、Review 分级 <https://docs.factory.com/onboarding/configuring-your-review-droid/review-droid-guidelines>
- Devin Review：<https://docs.devin.ai/work-with-devin/devin-review>

论文

- SWR-Bench：<https://arxiv.org/abs/2509.01494>；HalluJudge：<https://arxiv.org/abs/2601.19072>
- Agentless：<https://arxiv.org/html/2407.01489v2>；SWE-agent：<https://arxiv.org/html/2405.15793v3>
- Google 变异测试：<https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46584.pdf>
- Lost in the Middle：<https://arxiv.org/abs/2307.03172>；RULER：<https://arxiv.org/abs/2404.06654>
- 过度纠错：<https://arxiv.org/abs/2603.00539>；MAST 多代理失败模式：<https://arxiv.org/abs/2503.13657>
- Anthropic 多代理研究系统：<https://www.anthropic.com/engineering/built-multi-agent-research-system>

Claude Code 官方文档

- <https://code.claude.com/docs/en/code-review-local.md>、<https://code.claude.com/docs/en/ultrareview.md>、<https://code.claude.com/docs/en/sub-agents.md>、<https://code.claude.com/docs/en/prompt-caching.md>、<https://code.claude.com/docs/en/costs.md>、<https://code.claude.com/docs/en/best-practices>
- 缓存定价：<https://platform.claude.com/docs/en/build-with-claude/prompt-caching>
