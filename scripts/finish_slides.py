from pathlib import Path
import json,re
from build_deliverables import rect
ROOT=Path(__file__).resolve().parents[1]
slides=json.loads((ROOT/'scripts/slides_base.json').read_text(encoding='utf-8'))
design=(ROOT/'research/proposed_scheme.md').read_text(encoding='utf-8')
objects=[]
nodes=[
('需求與資料範圍明確？','否 → 補問必要資訊／結束'),
('規劃 → 檢查工具與參數','不合法 → 修正一次；仍錯即停止'),
('載入資料 → 品質足夠？','I/O僅重試一次；品質不足即報告'),
('分析基準、殘差與事件','失敗 → 保存證據與限制後停止'),
('依觀察選用領域規則？','是 → 查核適用規則；否 → 記錄省略原因'),
('領域規則 → 引用與數值檢查','不通過 → 固定模板；不捏造原因'),
('保存報告與證據 → 離線評估','輸出／結束；所有失敗保留紀錄')]
for i,(a,b) in enumerate(nodes):
    y=94+i*56
    objects.append(rect(42,y,388,42,a,16,fill='DCEDEE' if '?' in a or '？' in a else 'FFFFFF',line='087E8B'))
    objects.append(rect(438,y,42,42,'→',18,fill=None))
    objects.append(rect(484,y,434,42,b,15,fill='FFFFFF'))
    if i<6: objects.append(rect(210,y+39,50,22,'↓',13,fill=None))
slides.append(dict(title='Flowchart｜包含分支、重試與終止條件',objects=objects,source='天氣／作息資料不足則停用對應規則；完整 Mermaid 見 DESIGN.md',diagram='flowchart'))

code=re.search(r'```text\n(.*?)\n```',design,re.S)[1].splitlines()
# The full numbered algorithm is shown, split at line boundaries.
for start in range(0,len(code),23):
    lines=code[start:start+23]
    slides.append(dict(title=f'Pseudocode｜Algorithm 1（{start+1}–{start+len(lines)}）',source='Input：問題、設定、重播截止時間；Output：可追溯報告／待補資訊／失敗紀錄',objects=[rect(38,94,886,400,'\n'.join(lines),12,fill='FFFFFF')]))

def add(title,items,source='',size=19):
    hh=(395-10*(len(items)-1))/len(items)
    slides.append(dict(title=title,source=source,objects=[rect(42,94+i*(hh+10),876,hh,t,size) for i,t in enumerate(items)]))
add('Experiments｜資料切分與分析 Baseline',[
'最低版本：一棟建築、固定 12 週；8 週訓練 → 2 週校準 → 2 週測試。',
'B0：訓練期全域中位數；B1：訓練期同星期／小時中位數。',
'校準期絕對殘差第99百分位為暫定門檻；測試期禁止調參或重訓。',
'比較 MAE、資料覆蓋率及警示事件；警示數量不等於偵測準確率。',
'測試副本注入尖峰／持續增加／零值各10件；報命中率、漏失與延遲。'],source='所有期間、門檻與件數為預定設定；合成擾動不等於真實故障標籤')
add('Evaluation｜Agent 與公平比較',[
'10個案例各執行3次：一般需求、資訊不足、資料缺漏、I/O失敗及無根據診斷要求。',
'相同案例比較：固定Python報表、固定流程＋LLM、受限工具Agent。',
'記錄共同資料、設定及提示詞；分開看數值分析與工具規劃的效果。',
'指標：任務／工具成功率、事實可追溯率、正確停止率、預算遵守與無依據根因數。',
'人工核對引用是否支持語意；同時記錄延遲與用量，不只看答案流暢度。'],source='固定案例與評分分母詳見 DESIGN.md')
add('可行性、預期成果與交付',[
'第1週：資料核對與品質；第2週：基準、殘差與事件分析。',
'第3週：Agent、規則與證據報告；第4週：比較評估與展示。',
'工具：Python、pandas、numpy、pydantic、單一LLM SDK；本機CSV／JSON。',
'Expected Outcomes：可重現原型、可核對報告與真實比較結果；本階段尚未實驗。',
'Proposal交付：提案、PPT、Repository、DESIGN.md。期末再完成系統與驗證。'],source='4週為未提供時程下的暫定規劃；模型與依賴版本於實作時鎖定')
refs=[
'[A1] Yao et al. (2023), ReAct. arxiv.org/html/2210.03629v3',
'[A2] Gu et al. (2025), Argos. arxiv.org/html/2501.14170v1',
'[A3] Yang et al. (2025), Refining Time Series Anomaly Detectors using LLMs. arxiv.org/html/2503.21833v1',
'[A4] Mulayim et al. (2025), Extraction and Analysis of Time Series Data from BAS Using LLMs. DOI: 10.20357/B73W4C',
'[A5] Yang et al. (2025), Time-RA. arxiv.org/html/2507.15066v1',
'[D1] IEA (2026), Global Energy Review 2026 — Electricity demand.',
'[D2] IEA (2026), Electricity 2026 — Demand.',
'[D3] Miller et al. (2020), The Building Data Genome Project 2. DOI: 10.1038/s41597-020-00712-x',
'[D4–D6] BUDS Lab, BDG2 repository, LICENSE, Meters data features.',
'[D7] Kramer et al. (2020), Proving the Business Case for Building Analytics. LBNL.',
'[D8] U.S. DOE FEMP, Measurement and Verification Options for Federal Energy- and Water-Saving Projects.'
]
slides.append(dict(title='References｜原始來源',source='查核日期：2026-11-03；完整可點擊網址及查核範圍見提案 References',objects=[rect(42,94,876,400,'\n\n'.join(refs),12)]))
(ROOT/'scripts/slides.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2),encoding='utf-8')
print('Final slide count:',len(slides))
