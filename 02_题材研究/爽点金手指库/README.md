# 凡尘纪爽点金手指库 — 调用说明

> **库版本**：v1.0  
> **生成日期**：2026-07-22  
> **适用对象**：凡尘纪长篇小说写作团队 / 后续 AI 写作代理 / 任何想基于本卡库创作玄幻爽文的作者  
> **配套主文件**：`凡尘纪_爽点卡片库.json`

---

## 一、这套卡库是什么？

这是一套**可编程拼装的玄幻小说组件库**。它把《斗罗大陆》《斗破苍穹》《凡尘纪》三本经典玄幻小说的爽点结构拆解成一张张可独立调用、可任意组合的卡片。

每张卡片都包含：
- **id**：唯一编号（MS-* = 主角人设，KZ-* = 金手指，SH-* = 爽点，ZY-* = 资源榜，SHI-* = 势力，HB-* = 伙伴，FB-* = 副本）
- **name**：卡片名称
- **source**：灵感来源（凡尘纪原创 / 斗罗 / 斗破）
- **compatible_with**：与其他哪些卡片可搭配
- **核心字段**：每类卡片的专属字段

---

## 二、卡片七大类与字段说明

### 2.1 主角人设卡（MS-*）

**用途**：定义故事的核心人物。  
**核心字段**：
- `archetype`：原型（废物+觉醒者 / 穿越者 / 叛徒等）
- `open_hook`：开局钩子（前 3 章的事件）
- `growth_path`：成长曲线
- `limitation`：必须保留的限制（灵魂不能丢）

### 2.2 金手指机制卡（KZ-*）

**用途**：定义主角的"超能力"。  
**核心字段**：
- `type`：类型（信息碾压 / 加速成长 / 血脉天赋 / 知识碾压 / 剧情反转）
- `tier`：等级（T0 = 灵魂级 / T1 = 重要级 / T2 = 辅助级）
- `trigger`：触发条件
- `scaling_rule`：爽度规则（什么情况下爽感更强）
- `limitation`：使用限制
- `use_frequency`：建议使用频率

**T0 核心金手指（必须）**：KZ-001 信息差。这是凡尘纪的灵魂，不可替换。

### 2.3 爽点结构卡（SH-*）

**用途**：定义一个具体的"爽场景模板"。  
**核心字段**：
- `rhythm`：在全书节奏中的位置（如"开篇 1-3 章引爆"）
- `core_emotion`：核心情绪（屈辱 → 反杀 / 绝望 → 爆发）
- `trigger_event`：触发事件
- `structure`：结构分解（5 步详细流程）

**SH-007 文明抉择是凡尘纪最高级爽点**，对应"反血统论"理念公开的高潮时刻。每卷都必须埋线。

### 2.4 资源榜卡（ZY-*）

**用途**：定义可被主角获取的稀有资源。  
**核心字段**：
- `type`：类型（天地灵物 / 灵兽 / 遗宝 / 丹药 / 副本 / 功法）
- `count`：总数
- `design_intent`：设计意图
- `sample_top_N`：代表性资源列表

### 2.5 势力架构卡（SHI-*）

**用途**：定义故事中的组织/势力/地图层级。  
**核心字段**：
- `level_count`（如适用）：层级数
- `levels`：层级列表（level 1-7）
- `structure`：组织架构
- `design_intent`：设计意图

### 2.6 伙伴羁绊卡（HB-*）

**用途**：定义主角的伙伴/红颜组合。  
**核心字段**：
- `size`：规模
- `core_members`：成员槽位（每槽说明 archetype）
- `combo_template`：羁绊战技模板

### 2.7 副本地图卡（FB-*）

**用途**：定义可探索的副本/秘境。  
**核心字段**：
- `structure`：副本结构
- 列表（如 nine_trials / sample_dungeons）：每个副本的 theme/location/reward

---

## 三、调用方法（Python 示例）

### 3.1 基础调用：加载并查看卡片

```python
import json

# 加载卡库
with open('凡尘纪_爽点卡片库.json', 'r', encoding='utf-8') as f:
    card_db = json.load(f)

# 访问任意分类
protagonist_cards = card_db['cards']['主角人设卡']
for card in protagonist_cards:
    print(f"{card['id']}: {card['name']} (来源:{card['source']})")
```

### 3.2 按 id 查找单张卡

```python
def find_card_by_id(card_db, card_id):
    """根据 ID 查找任意分类的卡片"""
    for category, cards in card_db['cards'].items():
        for card in cards:
            if card['id'] == card_id:
                return card, category
    return None, None

# 示例：查找凡尘纪主角人设
card, cat = find_card_by_id(card_db, 'MS-001')
print(card['name'], card['open_hook'])
```

### 3.3 检查兼容性

```python
def check_compatibility(card_db, selected_ids):
    """检查所选卡片的兼容性"""
    selected_cards = []
    for cid in selected_ids:
        card, _ = find_card_by_id(card_db, cid)
        if card:
            selected_cards.append(card)
    
    score = 0
    for card in selected_cards:
        for compat in card.get('compatible_with', []):
            if compat in selected_ids:
                score += 1
    return score, len(selected_ids)

# 示例：检查凡尘纪原版配方
score, total = check_compatibility(card_db, [
    'MS-001', 'KZ-001', 'KZ-005', 
    'SH-002', 'SH-007', 'ZY-009', 
    'SHI-001', 'SHI-002', 'HB-001'
])
print(f"兼容性得分: {score}/{total}")  # 高分表示配方合理
```

### 3.4 随机抽卡生成新配方

```python
import random

def random_recipe(card_db):
    """随机抽卡生成新故事配方"""
    categories_min = {
        '主角人设卡': 1,
        '金手指机制卡': 2,
        '爽点结构卡': 4,
        '资源榜卡': 1,
        '势力架构卡': 1,
        '伙伴羁绊卡': 1,
        '副本地图卡': 1
    }
    
    recipe = {}
    for cat, min_n in categories_min.items():
        cards = card_db['cards'][cat]
        recipe[cat] = random.sample(cards, min(min_n, len(cards)))
    return recipe

# 生成 3 个新配方
for i in range(3):
    print(f"\n=== 新配方 {i+1} ===")
    recipe = random_recipe(card_db)
    for cat, cards in recipe.items():
        print(f"{cat}: {[c['id'] for c in cards]}")
```

### 3.5 七卷节奏排布生成器

```python
def generate_volume_plan(card_db, volume_count=7):
    """基于卡库生成七卷节奏"""
    volumes = []
    # 每卷至少 1 个爽点高潮 + 1 个资源获取
    sh_cards = card_db['cards']['爽点结构卡']
    zy_cards = card_db['cards']['资源榜卡']
    
    for vol in range(volume_count):
        # 每卷 3-4 个爽点卡
        sh_sample = random.sample(sh_cards, 4)
        # 每卷 1-2 个新资源
        zy_sample = random.sample(zy_cards, 2)
        volumes.append({
            'volume': vol + 1,
            'shuangdian': [c['id'] for c in sh_sample],
            'resources': [c['id'] for c in zy_sample]
        })
    return volumes

# 生成七卷规划
plan = generate_volume_plan(card_db)
for v in plan:
    print(f"第{v['volume']}卷: 爽点={v['shuangdian']}, 资源={v['resources']}")
```

### 3.6 凡尘纪灵魂校验

```python
def verify_fanchen_ji_soul(card_db, recipe_ids):
    """验证配方是否保留凡尘纪灵魂"""
    soul_required = ['KZ-001', 'SH-007', 'SHI-002']  # 三个必备
    missing = [r for r in soul_required if r not in recipe_ids]
    if missing:
        return False, f"缺失灵魂卡: {missing}"
    return True, "凡尘纪灵魂保留完整"

# 校验新配方
recipe = ['MS-001', 'KZ-001', 'KZ-005', 'SH-002', 'SH-007', 
          'ZY-009', 'SHI-001', 'SHI-002', 'HB-001', 'FB-003']
ok, msg = verify_fanchen_ji_soul(card_db, recipe)
print(msg)
```

---

## 四、四种标准配方（已写好）

卡库顶层 `调用示例` 字段内置四种配方：

### 配方 A：凡尘纪原版（反血统论）
- 主角：MS-001 矿奴之子
- 金手指：KZ-001 信息差 + KZ-005 有限回档
- 爽点主线：废灵根反转 → 隐藏身份 → 文明抉择 → 父爱如山 → 众望所归
- 适合：希望延续凡尘纪原作精神的写作

### 配方 B：斗破换皮
- 主角：MS-002 废柴退婚男
- 金手指：KZ-002 戒指老师 + KZ-004 可进化功法 + KZ-006 越级吸收
- 适合：经典斗破式爽文

### 配方 C：斗罗换皮
- 主角：MS-003 穿越少年
- 金手指：KZ-003 双生武魂 + KZ-007 前世记忆 + KZ-006 越级吸收
- 适合：穿越+学院+伙伴成长式

### 配方 D：随机抽卡
- 由代码自动从卡库中随机抽取组合
- 适合：灵感枯竭时的备选方案

---

## 五、克制原则（重要！）

为防止爽点透支 / 烂尾 / 主角人设崩坏，调用本卡库必须遵守：

1. **主角人设 1 个，金手指 ≤3 个**。金手指越多，读者越无感。
2. **每卷只用一个回档**（KZ-005）。回档必须付出可视化代价。
3. **资源榜元素不要一次用尽**。23 种灵火按 7 卷分布，每卷投放 3-4 种新资源。
4. **SH-007 文明抉择是灵魂**，每卷必须埋线（哪怕只一个伏笔），最终在第七卷公开。
5. **每 5 卷安排一次 SH-016 众望所归**，保持史诗感。
6. **伙伴数量稳定**。七人组写满就不要扩编；后期死亡的伙伴要早埋伏笔。

---

## 六、卡片调用禁忌

| 禁忌 | 后果 |
|------|------|
| 同时使用 ≥4 个金手指 | 主角力不从心，读者混乱 |
| 主角人设混用（如 MS-001 + MS-002） | 主角性格分裂 |
| 用 SH-007 不铺垫 | 公开真相显得突兀，读者不买账 |
| 用 KZ-005 不显化代价 | 回档变廉价，剧情张力消失 |
| 资源榜一次性投放 | 后期升级无资源可用，必须烂尾 |
| 伙伴超过 7 人 | 角色太多，读者记不住 |

---

## 七、卡库扩展指南

如需扩展卡库：

1. **新增卡片**：在对应分类的数组末尾添加，保持 id 前缀一致（MS-/KZ-/SH-/ZY-/SHI-/HB-/FB-）
2. **每张新卡必填字段**：id / name / source / compatible_with
3. **每张新卡选填字段**：根据卡片类型补全
4. **保持凡尘纪灵魂**：新增的反派势力建议挂到 SHI-002 天骄阁下
5. **更新校验区**：在 `质量校验` 字段中更新总数

---

## 八、配合凡尘纪的故事模板怎么用？

### 8.1 第一卷（矿区之子）调用方式

```python
# 第一卷核心卡
volume_1 = {
    'protagonist': 'MS-001',
    'golden_fingers': ['KZ-001'],  # 仅开篇引入信息差
    'shuangdian': ['SH-002', 'SH-013'],  # 废灵根反转+父爱如山伏笔
    'resources': [],  # 暂无资源获取
    'factions': ['SHI-001(仅 level 1)', 'SHI-002 引入反派'],
    'companions': ['HB-001 slot 3 铁子'],
    'dungeons': ['FB-003 slot 1 矿底凡尘诀封印地']
}
```

### 8.2 第三卷（宗门风云）调用方式

```python
# 第三卷核心卡（中段爽点爆发）
volume_3 = {
    'protagonist': 'MS-001',
    'golden_fingers': ['KZ-001', 'KZ-005', 'KZ-006 首次越级'],
    'shuangdian': ['SH-003', 'SH-006', 'SH-009', 'SH-008'],  # 4 爆点
    'resources': ['ZY-005 rank 3 轮回黑莲火'],
    'factions': ['SHI-001 level 3 地区大宗门'],
    'companions': ['HB-001 七人组全员'],
    'dungeons': ['FB-003 slot 2 凡尘派外门遗址']
}
```

### 8.3 第七卷（凡尘开元）调用方式

```python
# 第七卷核心卡（全书高潮）
volume_7 = {
    'protagonist': 'MS-001',
    'golden_fingers': ['KZ-001', 'KZ-005(最后一次)', 'KZ-004 终极进化', 'KZ-008 血脉终极觉醒'],
    'shuangdian': ['SH-007', 'SH-011', 'SH-016', 'SH-020'],  # 4 大终极爽点
    'resources': ['ZY-005 rank 1 凡源真火', 'ZY-009 rank 9 凡尘时代开元'],
    'factions': ['SHI-001 全 7 层', 'SHI-002 天骄阁覆灭'],
    'companions': ['HB-001 七人组', 'HB-002 红颜官宣'],
    'dungeons': ['FB-003 slot 5 凡尘时代开元地']
}
```

---

## 九、与其他产物联动

| 产物 | 联动方式 |
|------|----------|
| 02_题材研究/斗破苍穹拆书.md | 资源/爽点源头参考 |
| 02_题材研究/斗罗大陆拆书.md | 资源/爽点源头参考 |
| 03_世界观/ | 用 SHI-* 势力架构卡填充 |
| 04_人物/ | 用 HB-* 伙伴羁绊卡填充 |
| 05_总纲/故事雏形总纲.md | 用"调用示例"中配方 A 直接生成 |
| 06_卷纲/ | 用"七卷节奏排布生成器" |
| 08_钩子爽点反转/知乎爽点模板.md | 与 SH-* 爽点结构卡配合使用 |
| 99_模板/ | 可基于本卡库设计 AI 写作 prompt |

---

## 十、版本与维护

- **v1.0 (2026-07-22)**：首版生成，含 47 张卡（主角人设 4 + 金手指 8 + 爽点 20 + 资源榜 6 + 势力 4 + 伙伴 2 + 副本 3）
- **未来扩展方向**：
  - 增加更多 ZY-* 资源榜（丹药、符箓、阵法、傀儡等）
  - 增加更多 SHI-* 势力（修真家族、海外势力、魔门等）
  - 增加"轻喜剧向"SH-* 卡片（参照灵气逼人模式）
  - 增加"科幻修真"跨界变体
  - 增加"反英雄"向 SH-* 卡片

---

## 十一、一句话使用总结

> **加载 JSON → 选主角 → 配金手指 → 排爽点 → 加资源 → 排势力 → 排伙伴 → 排副本 → 校验凡尘纪灵魂 → 开写。**

---

*本卡库与凡尘纪所有产出物共享同一坐标系。如发现冲突或需要补充，请更新版本号并记录变更日志。*