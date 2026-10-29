#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行式数据核算器：把「日期 × 类别 × 数量指标 × 金额指标」行表算成日报所需的全部派生指标。

用法:
  python3 analyze.py --input data.tsv --weekend "09-06,09-07" --json /tmp/report_data.json
  cat data.md | python3 analyze.py --weekend "10-06,10-07"

输入: CSV / TSV / Markdown 表格（自动识别分隔符）。
表头别名自动匹配: 日期(date) / 类别·档位·门店·品类(cat) / 销量·数量·订单量(units) / 销售额·金额·GMV(amount)。
输出: 可读文本（报告引用的每个数字都从这里取）+ 可选 JSON（喂给图表）。
"""
import argparse
import json
import re
import statistics
import sys
from collections import OrderedDict

ALIASES = {
    'date':   ['日期', 'date', 'day', '天', '日'],
    'cat':    ['类别', '档位', '品类', '系列', '门店', '产品', '商品', '渠道', '组',
               'category', 'item', 'type', 'sku', 'group'],
    'units':  ['销量', '数量', '单量', '订单量', '单数', '件数', '张数', '访问', '流量',
               'units', 'qty', 'orders', 'count', 'volume'],
    'amount': ['销售额', '金额', '流水', '营业额', '收入', 'gmv', 'revenue', 'amount', 'sales'],
}
REQ = ['date', 'cat', 'units', 'amount']


def norm(s):
    return re.sub(r'[\s：:_]', '', str(s)).lower()


def match_col(h):
    n = norm(h)
    for key, alts in ALIASES.items():
        for a in alts:
            if n == norm(a):
                return key
    # 包含式兜底（如"销量（张）"）
    for key, alts in ALIASES.items():
        for a in alts:
            if norm(a) and norm(a) in n:
                return key
    return None


def parse_num(s):
    s = re.sub(r'[¥$€£%\s,，]', '', str(s))
    if s in ('', '-', '—', '–', 'nan', 'None', 'null'):
        return None
    return float(s)


def read_table(text):
    lines = [l.rstrip('\n') for l in text.splitlines() if l.strip()]
    md = [l for l in lines if l.strip().startswith('|')]
    if len(md) >= 2:  # markdown 表
        rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in md]
        rows = [r for r in rows if not all(re.fullmatch(r':?-+:?', c or '-') for c in r)]
    else:
        rows = None
        for sep in ['\t', ',', ';', '|']:
            if sep in lines[0]:
                rows = [[c.strip() for c in l.split(sep)] for l in lines]
                break
        if rows is None:
            rows = [l.split() for l in lines]
    header, mapping = rows[0], {}
    for i, h in enumerate(header):
        k = match_col(h)
        if k and k not in mapping:
            mapping[k] = i
    missing = [k for k in REQ if k not in mapping]
    if missing:
        sys.exit(f'[analyze] 无法识别表头，缺 {missing}。原始表头: {header}\n'
                 f'          支持的别名: {ALIASES}')
    out = []
    for r in rows[1:]:
        if len(r) <= max(mapping.values()):
            continue
        try:
            rec = {'date': str(r[mapping['date']]).strip(),
                   'cat': str(r[mapping['cat']]).strip(),
                   'units': parse_num(r[mapping['units']]),
                   'amount': parse_num(r[mapping['amount']])}
        except (ValueError, IndexError):
            continue
        if rec['units'] is None or rec['amount'] is None:
            continue
        out.append(rec)
    if not out:
        sys.exit('[analyze] 没有解析到有效数据行。')
    return out


def f1(x):
    return f'{x:.1f}'


def money(x):
    return f'{int(x + 0.5):,}'


def shares_flat(vals, total):
    """1 位小数占比 + 最大余数法调平，保证合计恰为 100.0。"""
    raw = [v / total * 100 for v in vals]
    base = [int(x * 10) / 10 for x in raw]           # 向下取到 0.1
    resid = int(round((100.0 - sum(base)) * 10))      # 需要补 0.1 的份数
    order = sorted(range(len(raw)), key=lambda i: raw[i] * 10 - int(raw[i] * 10), reverse=True)
    for i in order[:max(0, resid)]:
        base[i] += 0.1
    for i in order[len(order) + min(0, resid):]:
        base[i] -= 0.1
    assert abs(sum(base) - 100.0) < 1e-9
    return [round(x, 1) for x in base]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', help='数据文件（缺省读 stdin）')
    ap.add_argument('--weekend', help='周末日期，逗号分隔，如 "09-06,09-07"（可省略）')
    ap.add_argument('--json', dest='json_out', help='同时输出 JSON 到该路径（图表数据源）')
    args = ap.parse_args()

    text = open(args.input, encoding='utf-8').read() if args.input else sys.stdin.read()
    rows = read_table(text)

    # 日期顺序：形如 09-01 / 2025-09-01 的零填充日期按字典序，否则按首次出现
    dates = list(OrderedDict.fromkeys(r['date'] for r in rows))
    if all(re.fullmatch(r'(\d{4}-)?\d{2}-\d{2}', d) for d in dates):
        dates.sort()
    cats = list(OrderedDict.fromkeys(r['cat'] for r in rows))
    cell = {(r['date'], r['cat']): r for r in rows}
    agg = {}
    for r in rows:
        k = (r['date'], r['cat'])
        if k in agg:
            agg[k]['units'] += r['units']
            agg[k]['amount'] += r['amount']
        else:
            agg[k] = r

    W = print

    # ---------- 0) 单价校验：金额 ≈ 数量 × 类目中位单价 ----------
    W('=' * 62)
    W('【0) 单价校验】金额 vs 数量×类目中位单价（偏离>1% 即列出，多为折扣/退款/大单线索）')
    price = {c: statistics.median(cell[(d, c)]['amount'] / cell[(d, c)]['units']
                                   for d in dates if (d, c) in agg) for c in cats}
    flags = []
    for c in cats:
        for d in dates:
            if (d, c) not in agg:
                continue
            r = agg[(d, c)]
            exp = r['units'] * price[c]
            dev = (r['amount'] - exp) / exp if exp else 0
            if abs(dev) > 0.01:
                flags.append((d, c, r['units'], r['amount'], price[c], dev))
    if flags:
        for d, c, u, a, p, dev in flags:
            W(f'  ⚠ {d} {c}: 金额{money(a)} ≠ {u:.0f}×中位单价{p:.2f}={money(u * p)}（偏离 {dev * 100:+.1f}%）——写进第二章异常定位')
    else:
        W('  全部通过：金额=数量×恒定单价，无折扣/退款/异常大单干扰。')

    # ---------- 1) 每日汇总 ----------
    W('=' * 62)
    W('【1) 每日汇总】(销量 / 销售额 / 客单价=额÷量)')
    day_u, day_a = OrderedDict(), OrderedDict()
    for d in dates:
        u = sum(agg[(d, c)]['units'] for c in cats if (d, c) in agg)
        a = sum(agg[(d, c)]['amount'] for c in cats if (d, c) in agg)
        day_u[d], day_a[d] = u, a
        W(f'  {d}: {u:>8.0f} / {money(a):>12} / {f1(a / u)}')
    tu, ta = sum(day_u.values()), sum(day_a.values())
    W(f'  合计: {tu:,.0f} / {money(ta)}  日均 {f1(tu / len(dates))} / {money(ta / len(dates))}  平均客单价 {f1(ta / tu)}')

    # ---------- 2) 类目结构与占比 ----------
    W('=' * 62)
    W('【2) 类目首周汇总与结构占比】(销量占比 / 销售额占比，均为 1 位小数、已按最大余数法调平至合计 100.0%)')
    cat_u, cat_a = OrderedDict(), OrderedDict()
    for c in cats:
        cat_u[c] = sum(agg[(d, c)]['units'] for d in dates if (d, c) in agg)
        cat_a[c] = sum(agg[(d, c)]['amount'] for d in dates if (d, c) in agg)
    sh_u = shares_flat([cat_u[c] for c in cats], tu)
    sh_a = shares_flat([cat_a[c] for c in cats], ta)
    for c, su, sa in zip(cats, sh_u, sh_a):
        W(f'  {c}: 量 {cat_u[c]:>10,.0f} ({su:5.1f}%)  额 {money(cat_a[c]):>12} ({sa:5.1f}%)  中位单价 {price[c]:.2f}')

    # ---------- 3) 首日→末日增速 ----------
    W('=' * 62)
    W('【3) 首日→末日增速】(价格恒定时各档量额增速相同)')
    d0, d1 = dates[0], dates[-1]
    u0 = sum(agg[(d0, c)]['units'] for c in cats if (d0, c) in agg)
    u1 = sum(agg[(d1, c)]['units'] for c in cats if (d1, c) in agg)
    a0 = sum(agg[(d0, c)]['amount'] for c in cats if (d0, c) in agg)
    a1 = sum(agg[(d1, c)]['amount'] for c in cats if (d1, c) in agg)
    W(f'  总量: {u0:,.0f}→{u1:,.0f}  {((u1 / u0) - 1) * 100:+.1f}%    总额: {money(a0)}→{money(a1)}  {((a1 / a0) - 1) * 100:+.1f}%')
    for c in cats:
        v0, v1 = agg[(d0, c)]['units'], agg[(d1, c)]['units']
        W(f'  {c}: {v0:,.0f}→{v1:,.0f}  {((v1 / v0) - 1) * 100:+.1f}%   指数化(D1=100) {["%s:%.1f" % (dates[i], agg[(d, c)]["units"] / v0 * 100) for i, d in enumerate(dates)]}')
    av0, av1 = a0 / u0, a1 / u1
    W(f'  客单价: {f1(av0)}→{f1(av1)}  {((av1 / av0) - 1) * 100:+.1f}%')

    # ---------- 4) 环比 ----------
    W('=' * 62)
    W('【4) 逐日环比】(找全周唯一/连续的下滑日)')
    for i in range(1, len(dates)):
        p, q = dates[i - 1], dates[i]
        W(f'  {p}→{q}: 量 {(day_u[q] / day_u[p] - 1) * 100:+6.1f}%  额 {(day_a[q] / day_a[p] - 1) * 100:+6.1f}%')

    # ---------- 5) 最值 ----------
    W('=' * 62)
    W('【5) 最值】(异常定位素材)')
    W(f'  量最低日 {min(day_u, key=day_u.get)} {min(day_u.values()):,.0f}（较日均值 {(min(day_u.values()) / (tu / len(dates)) - 1) * 100:+.1f}%）'
      f'  最高日 {max(day_u, key=day_u.get)} {max(day_u.values()):,.0f}')
    W(f'  额最低日 {min(day_a, key=day_a.get)} {money(min(day_a.values()))}  最高日 {max(day_a, key=day_a.get)} {money(max(day_a.values()))}')
    for c in cats:
        seq = {d: agg[(d, c)]['units'] for d in dates if (d, c) in agg}
        W(f'  {c} 逐日: {[f"{seq[d]:.0f}" for d in dates]}  最低 {min(seq, key=seq.get)}({min(seq.values()):,.0f})')
    for i in range(1, len(dates)):
        p, q = dates[i - 1], dates[i]
        for c in cats:
            if (p, c) in agg and (q, c) in agg:
                va, vb = agg[(p, c)]['amount'], agg[(q, c)]['amount']
                if (vb / va - 1) < -0.05:
                    W(f'  ⚠ {q} {c} 额环比 {((vb / va) - 1) * 100:+.1f}%（{money(va)}→{money(vb)}）——下滑明显，进第二章候选')

    # ---------- 6) 前后半程 ----------
    if len(dates) >= 4:
        W('=' * 62)
        W('【6) 前后半程日均对比】(前 ⌈n/2⌉ 天 vs 其余)')
        h = (len(dates) + 1) // 2
        fu, lu = dates[:h], dates[h:]
        fu_avg_u = sum(day_u[d] for d in fu) / len(fu)
        lu_avg_u = sum(day_u[d] for d in lu) / len(lu)
        fu_avg_a = sum(day_a[d] for d in fu) / len(fu)
        lu_avg_a = sum(day_a[d] for d in lu) / len(lu)
        W(f'  {fu[0]}~{fu[-1]} 日均 {f1(fu_avg_u)} / {money(fu_avg_a)}  vs  {lu[0]}~{lu[-1]} 日均 {f1(lu_avg_u)} / {money(lu_avg_a)}'
          f'  → 量 {(lu_avg_u / fu_avg_u - 1) * 100:+.1f}%  额 {(lu_avg_a / fu_avg_a - 1) * 100:+.1f}%')

    # ---------- 7) 周末效应 ----------
    weekend = None
    if args.weekend:
        weekend = [d.strip() for d in re.split('[,,]', args.weekend) if d.strip()]
        unknown = [d for d in weekend if d not in dates]
        if unknown:
            sys.exit(f'[analyze] --weekend 里的日期不在数据中: {unknown}')
        W('=' * 62)
        W(f'【7) 周末效应】周末={weekend}（工作日=其余；提升%=周末日均÷工作日日均-1；集中度=周末量÷该类全周量）')
        wd = [d for d in dates if d not in weekend]
        n_wd, n_we = len(wd), len(weekend)
        for c in cats + ['ALL']:
            if c == 'ALL':
                wv = sum(day_u[d] for d in wd); wkv = sum(day_u[d] for d in weekend)
                wr = sum(day_a[d] for d in wd); wkr = sum(day_a[d] for d in weekend)
                cu, ca = tu, ta
            else:
                wv = sum(agg[(d, c)]['units'] for d in wd); wkv = sum(agg[(d, c)]['units'] for d in weekend)
                wr = sum(agg[(d, c)]['amount'] for d in wd); wkr = sum(agg[(d, c)]['amount'] for d in weekend)
                cu, ca = cat_u[c], cat_a[c]
            W(f'  {c}: 工作日日均 {f1(wv / n_wd)} / {money(wr / n_wd)}  周末日均 {f1(wkv / n_we)} / {money(wkr / n_we)}'
              f'  量提升 {(wkv / n_we) / (wv / n_wd) * 100 - 100:+.1f}%  额提升 {(wkr / n_we) / (wr / n_wd) * 100 - 100:+.1f}%'
              f'  周末集中度(量) {wkv / cu * 100:.1f}%')

    # ---------- JSON ----------
    if args.json_out:
        data = {
            'dates': dates, 'cats': cats,
            'units': {c: [agg[(d, c)]['units'] if (d, c) in agg else None for d in dates] for c in cats},
            'amount': {c: [agg[(d, c)]['amount'] if (d, c) in agg else None for d in dates] for c in cats},
            'daily_units': [day_u[d] for d in dates], 'daily_amount': [day_a[d] for d in dates],
            'cat_units': cat_u, 'cat_amount': cat_a,
            'cat_units_share': dict(zip(cats, sh_u)), 'cat_amount_share': dict(zip(cats, sh_a)),
            'total_units': tu, 'total_amount': ta,
            'price_flags': [{'date': d, 'cat': c, 'units': u, 'amount': a, 'median_price': p, 'dev': dev}
                            for d, c, u, a, p, dev in flags],
            'weekend': weekend,
        }
        with open(args.json_out, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        W('=' * 62)
        W(f'JSON 已写入 {args.json_out}（图表数据直接引用）')


if __name__ == '__main__':
    main()
