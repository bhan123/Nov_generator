#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
novel-factory 抽卡脚本
基于凡尘纪爽点金手指库，分配 3 个不重叠的故事骨架卡组。
设计原则：
  1) 3 本书的 主角人设 / 金手指 / 资源榜 / 核心爽点 / 副本 / 伙伴 全部不重叠
  2) SHI-001 七层升级地图作为通用结构卡允许共享（结构性而非主题性）
  3) 严格遵守克制原则（主角 1 个、金手指 ≤3、每卷 1 次回档）
  4) 每张卡都有 reason 字段
"""

import json

DECK_PATH = '/srv/novel-factory/Novel_Project/02_题材研究/爽点金手指库/凡尘纪_爽点卡片库.json'

with open(DECK_PATH, 'r', encoding='utf-8') as f:
    DECK = json.load(f)


def find_card(card_id):
    for cat, cards in DECK['cards'].items():
        for c in cards:
            if c['id'] == card_id:
                return c, cat
    return None, None


def check_compat(selected_ids):
    """兼容性：selected 卡之间出现在 compatible_with 的对数"""
    score = 0
    pairs = 0
    for cid in selected_ids:
        c, _ = find_card(cid)
        if not c:
            continue
        for x in c.get('compatible_with', []):
            tail = x.split('_')[-1]
            if tail in selected_ids and tail != cid:
                score += 1
                pairs += 1
    return score, pairs


# ============================================================
# 3 套组合（手工设计 + 兼容性过滤）
# 严格不重叠分配：
#   主角: MS-002 / MS-003 / MS-004
#   金手指: KZ-002/004/006  /  KZ-003/007/005  /  KZ-008/001
#   资源榜: ZY-005/010      /  ZY-006/009      /  ZY-007/008
#   爽点  : SH-001/004/005/008/014/019
#          / SH-002/006/010/011/012/016
#          / SH-003/007/013/017/018/020
#   势力  : SHI-001/004      /  SHI-001         /  SHI-002/003
#   伙伴  : HB-002           /  HB-001          /  无（孤狼反英雄）
#   副本  : FB-002           /  FB-001          /  FB-003
# ============================================================

RECIPES = {
    'D1_焚炎九重天': {
        'book_title': '焚炎九重天',
        'tagline': '三年之约的少年，怀揣一枚藏魂古戒，一路焚尽九重天的不公。',
        'theme': '退婚流 / 玄幻 / 戒指老师+异火 / 斗破换皮变体',
        'total_chars_target': '260万',
        'volumes': 7,
        'protagonist': {
            'id': 'MS-002',
            'name': '陆劫尘',
            'reason': 'MS-002 废柴退婚男是 D1 主线发动机的完美人选——三年之约提供刚性时间锁，'
                       '家族落魄提供开篇爽点张力，且与 MS-001/MS-003/MS-004 完全不同调性。',
        },
        'golden_fingers': [
            {'id': 'KZ-002', 'name': '戒指老师',
             'reason': '斗破同款核心，绑定 MS-002，老师残魂 + 功法传承 + 关键时出体护主，'
                       '完美服务 SH-005 师徒情深。'},
            {'id': 'KZ-004', 'name': '可进化功法',
             'reason': '异火吞噬式升级是 D1 资源榜 ZY-005 的承接器；每卷 1-2 次进化，'
                       '共可设 10-14 个进化节点，给出 260 万字的可写长度。'},
            {'id': 'KZ-006', 'name': '越级吸收',
             'reason': 'D1 的战术爽点放大器；与 ZY-005 异火、KZ-004 进化联动，'
                       '实现"低阶吞高阶→全场震惊"的经典套路（服务 SH-004 越级反杀）。'},
        ],
        'shuangdian': [
            {'id': 'SH-001', 'name': '退婚打脸', 'position': '卷一开局 1-3 章引爆',
             'note': '三年之约期限：三年后宗门大比'},
            {'id': 'SH-004', 'name': '越级反杀', 'position': '每 20-30 章爆发一次',
             'note': '配合 KZ-006 越级吸收'},
            {'id': 'SH-005', 'name': '师徒情深/护主牺牲', 'position': '卷三一次、卷六一次',
             'note': '老师药老残魂 vs 主角修至大圆满'},
            {'id': 'SH-008', 'name': '命运回档', 'position': '卷四（不在本配方里——改用剧情反转）',
             'note': 'D1 不强行使用 KZ-005 回档金手指，回档效果通过剧情反转实现'},
            {'id': 'SH-014', 'name': '认知反差打脸', 'position': '中段高频',
             'note': '打脸斗破风的视觉快感来源'},
            {'id': 'SH-019', 'name': '一皇 N 后', 'position': '卷五开始密集',
             'note': '配合 HB-002 情缘矩阵'},
        ],
        'resources': [
            {'id': 'ZY-005', 'name': '天地灵火榜',
             'reason': '23 种灵火 + 7 卷分布 = 每卷投放 3-4 种新资源，260 万字的硬度支撑。'},
            {'id': 'ZY-010', 'name': '心法流派榜',
             'reason': '12 大流派给主角/反派/盟友各派系做功法分门别类，与 ZY-005 灵火榜联动。'},
        ],
        'factions': [
            {'id': 'SHI-001', 'name': '七层升级地图',
             'reason': '通用 7 层地图，卷一 → 卷七 = 7 层升级路径。'},
            {'id': 'SHI-004', 'name': '远古遗族八大古族',
             'reason': 'D1 不走"凡尘派被剿灭"的真相线，改走"古族内部派系倾轧"，'
                       '区别于凡尘纪的灵魂设计，避免与 D3 主题冲突。'},
        ],
        'companions': {
            'id': 'HB-002', 'name': '一皇 N 后情缘',
            'reason': '退婚流的核心爽点之一是后宫与红颜，D1 用 HB-002 而不是 HB-001 七人组，'
                       '避开与 D2 的伙伴体系重叠。',
        },
        'dungeons': [
            {'id': 'FB-002', 'name': '远古遗族秘境',
             'reason': 'D1 主副本推进器；8 个远古秘境分 7 卷投放，与 KZ-004 进化、KZ-006 越级联动。'},
        ],
        'replaced_from_fanchen': '【明确替换凡尘纪默认】'
                                   '主角人设: MS-001 矿奴之子 → MS-002 废柴退婚男'
                                   '金手指: 移除 KZ-001 信息差 (改走纯战斗进化路线)'
                                   '金手指: 移除 KZ-005 有限回档 (改用剧情反转)'
                                   '爽点主线: 移除 SH-007 文明抉择 (D1 不打文明级叙事)'
                                   '势力: 移除 SHI-002/003 凡尘派系 (改为 SHI-004 古族派系)'
                                   '副本: 移除 FB-001/FB-003 (改用 FB-002 远古遗族秘境)',
    },

    'D2_双生纪元': {
        'book_title': '双生纪元',
        'tagline': '前世唐门外门弟子，今世废武魂少年——两道魂，一颗心，开一个时代。',
        'theme': '学院流 / 魂穿 / 双生武魂+前世记忆 / 斗罗换皮变体',
        'total_chars_target': '280万',
        'volumes': 7,
        'protagonist': {
            'id': 'MS-003',
            'name': '沈夜星',
            'reason': 'MS-003 穿越少年 + 废武魂蓝银草是 D2 开局标准开局；'
                       '前世记忆 + 双生武魂的双线设计天然适配"学院派"。',
        },
        'golden_fingers': [
            {'id': 'KZ-003', 'name': '双生武魂',
             'reason': 'D2 主角的核心天赋；前 1/3 卷隐藏，第二/第五卷两次觉醒。'},
            {'id': 'KZ-007', 'name': '前世记忆',
             'reason': '前世唐门外门弟子是 D2 商业/技术碾压的源头；'
                       '但严格克制——前世涉猎越广，本世规则差异越大。'},
            {'id': 'KZ-005', 'name': '有限回档',
             'reason': 'D2 用 KZ-005 而非 KZ-006（已在 D1 用了）。'
                       '每卷 1 次回档 + 永久可视代价，配合 SH-008 命运回档。'},
        ],
        'shuangdian': [
            {'id': 'SH-002', 'name': '废武魂反转', 'position': '卷一末觉醒',
             'note': '蓝银草 → 蓝银皇的惊天反转'},
            {'id': 'SH-006', 'name': '反派真相反转', 'position': '每卷 1 次',
             'note': '武魂殿（对应势力）伪善揭露'},
            {'id': 'SH-010', 'name': '以命换命/极限爆发', 'position': '卷四献祭一次',
             'note': '七怪某位为救主角献祭魂环'},
            {'id': 'SH-011', 'name': '重建/师承时刻', 'position': '每卷 1 次',
             'note': '前世暗器工艺在今世重建唐门'},
            {'id': 'SH-012', 'name': '战友重逢', 'position': '中段开始每卷 1 次',
             'note': '七怪羁绊战技的高光时刻'},
            {'id': 'SH-016', 'name': '众望所归', 'position': '卷六/卷七史诗高光',
             'note': '主角继承海神/武魂共主'},
        ],
        'resources': [
            {'id': 'ZY-006', 'name': '禁兽谱',
             'reason': '斗罗魂兽系升级；30 种灵兽分 7 卷投放，与 HB-001 七人固定伙伴深度联动。'},
            {'id': 'ZY-009', 'name': '神祇九考副本榜',
             'reason': 'D2 主线副本推进器；与 FB-001 九考副本地图一一对应。'},
        ],
        'factions': [
            # D2 不使用 SHI-* 卡——学院自身就是势力架构
            # 七层升级通过 七人组各自成长 + 九考副本的剧情推进来实现
            # 这是 D2 的"反势力架构"创新点：不靠外部大势力，靠学院+师承+同行者
        ],
        'companions': {
            'id': 'HB-001', 'name': '七人固定伙伴',
            'reason': '斗罗史莱克七怪模式的直接映射；'
                       'D2 学院派灵魂需要密集的同伴互动与羁绊战技。',
        },
        'dungeons': [
            {'id': 'FB-001', 'name': '九考副本式地图',
             'reason': 'D2 主副本推进器；9 考 = 7 卷中每卷至少 1 考 + 卷三卷六加倍。'},
        ],
        'replaced_from_fanchen': '【明确替换凡尘纪默认】'
                                   '主角人设: MS-001 矿奴之子 → MS-003 穿越少年'
                                   '金手指: KZ-001 信息差 → KZ-007 前世记忆 (去掉反血统论内核)'
                                   '金手指: KZ-005 保留 (回档机制)'
                                   '爽点主线: 废灵根反转 → 废武魂反转 (SH-002)'
                                   '势力: 移除 SHI-002/003/004 (只用 SHI-001 简化)'
                                   '伙伴: HB-001 七人组 (凡尘纪原作同理但角色名换)',
    },

    'D3_逆鳞问仙': {
        'book_title': '逆鳞问仙',
        'tagline': '被冤枉的叛门弟子，藏一脉凡尘遗血，撬动整个修真文明的真相。',
        'theme': '反英雄 / 弃徒暗线 / 血脉觉醒+信息差 / 凡尘纪灵魂变体',
        'total_chars_target': '300万',
        'volumes': 7,
        'protagonist': {
            'id': 'MS-004',
            'name': '裴去病',
            'reason': 'MS-004 叛门弃徒是 D3 反英雄叙事的唯一解；'
                       '主角开场就被冤枉除名，全书以"洗冤+复仇"为暗线推进，'
                       '区别于 D1 的"立志三年之约"和 D2 的"穿越开挂"。',
        },
        'golden_fingers': [
            {'id': 'KZ-008', 'name': '血脉觉醒',
             'reason': 'D3 主角父母之一来自被灭的凡尘派遗脉，血脉沉睡 → 觉醒分三次。'
                       '与凡尘纪的 KZ-008 用法一致，但是放在反英雄主角身上。'},
            {'id': 'KZ-001', 'name': '信息差(凡尘真源)',
             'reason': 'T0 级核心金手指——D3 不走"退婚打脸"，改走"修真真相公开"路线，'
                       'KZ-001 是这条线的发动机。每卷爆发 3 次以上。'},
        ],
        'shuangdian': [
            {'id': 'SH-003', 'name': '隐藏身份揭露', 'position': '每卷 1-2 次',
             'note': '主角凡尘派遗脉身份逐步揭露'},
            {'id': 'SH-007', 'name': '文明抉择/阶层批判', 'position': '卷六预爆、卷七终极爆发',
             'note': '本书灵魂爽点——修真文明始于凡人的真相公开'},
            {'id': 'SH-013', 'name': '父爱如山反转', 'position': '卷三揭示、卷六深揭',
             'note': '父亲为保护主角而背负叛徒骂名'},
            {'id': 'SH-017', 'name': '父债子还/血脉诅咒', 'position': '卷四展开',
             'note': '凡尘派血脉使命落到主角肩上'},
            {'id': 'SH-018', 'name': '以德报怨', 'position': '卷五感化对手',
             'note': '对曾经的告密者/陷害者反向救治'},
            {'id': 'SH-020', 'name': '真相雪冤', 'position': '卷七终极昭雪',
             'note': '凡尘派被冤枉的历史得到公开昭雪'},
        ],
        'resources': [
            {'id': 'ZY-007', 'name': '古器遗宝榜',
             'reason': '20 件遗宝支撑 D3 主线推进；与 KZ-008 血脉觉醒、KZ-001 信息差联动。'},
            {'id': 'ZY-008', 'name': '丹药秘方榜',
             'reason': '"凡尘开灵丹"等反血统论具象丹药是 D3 的招牌资源。'},
        ],
        'factions': [
            {'id': 'SHI-002', 'name': '天骄阁(终极反派组织)',
             'reason': 'D3 的终极反派；通过 KZ-001 信息差揭露其"窃取凡人修真成果"真相。'},
            {'id': 'SHI-003', 'name': '凡尘派(被剿灭的真相派)',
             'reason': '主角父辈的师承；中后期发现自己是凡尘派遗脉——主线反转的核心。'},
        ],
        'companions': {
            'id': None,
            'note': 'D3 是反英雄孤狼路线——主角被冤枉独自上路，中前期不建立固定伙伴；'
                    '中段逐步回收父亲旧部、感化告密者；卷六开始形成"七人重组"但成员多半'
                    '是背叛者/仇敌/陌生人，与 D2 学院派 HB-001 是两种完全不同的羁绊结构。',
        },
        'dungeons': [
            {'id': 'FB-003', 'name': '凡尘派故地群',
             'reason': '5 个凡尘派秘境 = 5 次身世揭秘；这是 D3 文明级真相的副本骨架。'},
        ],
        'replaced_from_fanchen': '【凡尘纪变体——继承灵魂，但调性暗黑】'
                                   '主角人设: MS-001 矿奴之子 → MS-004 叛门弃徒'
                                   '金手指: KZ-001 保留 (灵魂金手指不可丢)'
                                   '金手指: KZ-005 → KZ-008 (回档 → 血脉觉醒，更适合反英雄)'
                                   '爽点主线: SH-007 + SH-013 + SH-020 (文明抉择+父爱如山+真相雪冤)'
                                   '势力: SHI-002 + SHI-003 保留 (凡尘派真相)'
                                   '调性变体: 凡尘纪是"觉醒→立志→破迷"; D3 是"被冤枉→自证→反杀"',
    },
}


# ============================================================
# 不重叠检查
# ============================================================
def check_no_overlap(recipes):
    used = {
        'protagonist': set(),
        'golden_fingers': set(),
        'shuangdian': set(),
        'resources': set(),
        'factions': set(),
        'companions': set(),
        'dungeons': set(),
    }
    issues = []
    for name, r in recipes.items():
        if r['protagonist']['id'] in used['protagonist']:
            issues.append(f"主角人设重叠: {r['protagonist']['id']}")
        used['protagonist'].add(r['protagonist']['id'])

        for x in r['golden_fingers']:
            if x['id'] in used['golden_fingers']:
                issues.append(f"金手指重叠: {x['id']}")
            used['golden_fingers'].add(x['id'])

        for x in r['shuangdian']:
            if x['id'] in used['shuangdian']:
                issues.append(f"爽点重叠: {x['id']}")
            used['shuangdian'].add(x['id'])

        for x in r['resources']:
            if x['id'] in used['resources']:
                issues.append(f"资源榜重叠: {x['id']}")
            used['resources'].add(x['id'])

        for x in r['factions']:
            if x['id'] in used['factions']:
                issues.append(f"势力重叠: {x['id']}")
            used['factions'].add(x['id'])

        cid = r['companions'].get('id')
        if cid:
            if cid in used['companions']:
                issues.append(f"伙伴体系重叠: {cid}")
            used['companions'].add(cid)

        for x in r['dungeons']:
            if x['id'] in used['dungeons']:
                issues.append(f"副本重叠: {x['id']}")
            used['dungeons'].add(x['id'])

    return issues


def verify_compatibility(recipe):
    all_ids = [recipe['protagonist']['id']]
    for x in recipe['golden_fingers']:
        all_ids.append(x['id'])
    for x in recipe['shuangdian']:
        all_ids.append(x['id'])
    for x in recipe['resources']:
        all_ids.append(x['id'])
    for x in recipe['factions']:
        all_ids.append(x['id'])
    if recipe['companions'].get('id'):
        all_ids.append(recipe['companions']['id'])
    for x in recipe['dungeons']:
        all_ids.append(x['id'])
    score, pairs = check_compat(all_ids)
    return score, pairs, len(all_ids)


# ============================================================
# 主入口
# ============================================================
if __name__ == '__main__':
    print("=" * 70)
    print("novel-factory D 产物抽卡结果（3 套故事骨架）")
    print("=" * 70)

    overlap_issues = check_no_overlap(RECIPES)
    if overlap_issues:
        print("\n⚠️  检测到重叠:")
        for issue in overlap_issues:
            print(f"  - {issue}")
    else:
        print("\n✅ 3 套组合主角/金手指/爽点/资源/伙伴/副本 零重叠（SHI-001 通用地图共享）")

    for name, r in RECIPES.items():
        score, pairs, total = verify_compatibility(r)
        print(f"\n=== {name} ({r['theme']}) ===")
        print(f"  书名: {r['book_title']}")
        print(f"  字数: {r['total_chars_target']} ({r['volumes']} 卷)")
        print(f"  兼容性: {pairs} 对兼容关系 / 共 {total} 张卡")
        print(f"  主角: {r['protagonist']['id']} {r['protagonist']['name']}")
        print(f"  金手指: {[x['id'] for x in r['golden_fingers']]}")
        print(f"  资源榜: {[x['id'] for x in r['resources']]}")
        print(f"  势力: {[x['id'] for x in r['factions']]}")
        print(f"  爽点: {[x['id'] for x in r['shuangdian']]}")
        print(f"  伙伴: {r['companions'].get('id') or '孤狼反英雄（无固定卡）'}")
        print(f"  副本: {[x['id'] for x in r['dungeons']]}")

    print("\n" + "=" * 70)
    print("输出目录:")
    print("  /srv/novel-factory/Novel_Project/04_人物/D1_焚炎九重天/")
    print("  /srv/novel-factory/Novel_Project/04_人物/D2_双生纪元/")
    print("  /srv/novel-factory/Novel_Project/04_人物/D3_逆鳞问仙/")
    print("=" * 70)
