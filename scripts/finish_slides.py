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
add('研究問題｜每項假設都可以被否證',[
'RQ1：同星期／小時基準 B1 是否比全域中位數 B0 更符合保留期用電型態？',
'RQ2：Agent 能否維持資訊完整與證據正確，同時省下不必要的規則評估？',
'RQ3：錯 ID、錯值、錯單位、錯對象等主張，是否被驗證器拒絕或模板取代？',
'若固定流程相同或較佳，就照實報告；不把文字流暢當成準確或節能。'],source='預定研究假設與驗收方式；沒有實驗結果')
add('Scope｜最低版本與擴充範圍',[
'必做：單棟 raw 資料、固定12週、B0/B1、事件、證據、十個案例。',
'天氣：只作同時背景；不宣稱已完成天氣校正或排除空調因素。',
'擴充：跨建築、cleaned敏感度、天氣預測模型、現場工單。',
'不在本次最低版本：實體感測器、設備控制、故障確診與已實現節電。'],source='Proposal、DESIGN.md、實驗協議使用相同邊界')
add('案例矩陣｜成功與正確停止都要驗證',[
'C01–C03：偏高、連續零值、無警示；有證據才形成相應報告。',
'C04–C06：缺建築、缺期間、用電不足；補問或停止，不猜資料。',
'C07–C08：缺天氣仍分析用電；暫時 I/O 最多重試一次。',
'C09–C10：非法工具／越界一律拒絕；無設備證據不確診空調。',
'三組 × 十案例 × 三次＝90次；合成案例明確標示，保存失敗紀錄。'],source='每例的必要條件與分母見 research/evaluation_protocol.md',size=18)
add('證據報告｜說明用合成例',[
'假設：4小時各觀測180 kWh，歷史基準各120 kWh，門檻30 kWh。',
'每點偏離60 kWh，超過門檻；合併事件的偏離總和為240 kWh。',
'報告：需查排程、活動與設備狀態；不能宣稱空調故障或節省240 kWh。',
'若中間一小時缺測：不補零、不跨缺口合併，重新計算有效事件。'],source='illustrative_only：教學假設，非 BDG2 實測結果')
add('人工審閱｜避免只有引用卻沒有支持',[
'兩人獨立審閱匿名報告；先保存分歧，再討論共同判定。',
'逐項核對數值、單位、建築、期間、語意，不能只檢查證據 ID 存在。',
'完整度與追溯率一起看；沒有事實的空報告不能拿100%。',
'原始草稿與模板補救後結果分開；三次重跑不當成三個獨立使用者。'],source='未安排兩位審閱者時明示限制；學生審閱不等於故障真值')
add('Final Handover｜從設計到可交接',[
'現在：Proposal文件、簡報、DESIGN、評估協議及可重建文件流程。',
'期末：可執行Agent、資料版本與授權、測試、實驗結果、比較與結論。',
'Final PPT超過20頁；YouTube簡報與Demo超過10分鐘。',
'繳交前填姓名／學號與分工，重跑README步驟，確認其他人能接手。'],source='完整作業對照見 docs/acceptance.md')
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
'[D8] U.S. DOE FEMP, Measurement and Verification Options for Federal Energy- and Water-Saving Projects.',
'[D9] Park et al. (2025), Probabilistic Forecasting for Building Energy Systems using TSFMs. arxiv.org/html/2506.00630v1'
]
for start in range(0,len(refs),6):
    slides.append(dict(title=f'References｜原始來源 {start//6+1}',source='新增來源及核心資料說明查核：2026-11-11；完整連結見 Proposal References',objects=[rect(42,94,876,400,'\n\n'.join(refs[start:start+6]),16)]))
(ROOT/'scripts/slides.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2),encoding='utf-8')
print('Final slide count:',len(slides))
