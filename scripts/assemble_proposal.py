from pathlib import Path
import re,json
from build_deliverables import rect

ROOT=Path(__file__).resolve().parents[1]
domain=(ROOT/'research/domain_research.md').read_text(encoding='utf-8')
ai=(ROOT/'research/ai_research.md').read_text(encoding='utf-8')
design=(ROOT/'research/proposed_scheme.md').read_text(encoding='utf-8')
protocol=(ROOT/'research/evaluation_protocol.md').read_text(encoding='utf-8')

def section(s,start,end=None):
    out=s.split(start,1)[1]
    return out.split(end,1)[0].strip() if end else out.strip()

abstract='''# Energy Detective：建築用電異常調查 AI Agent
## DIC3 Project Proposal Refactor using OpenSpec
組別：第25組

課程：物聯網數據分析與應用｜階段：Proposal（占課程成績 10%）
日期：2026-11-12

組員（依學號排序）：

| 學號 | 姓名 |
|---|---|
| 7114056008 | 侯如蓁 |
| 7114056093 | 蔡奇勳 |
| 7114056126 | 施秉榕 |
| 7114056143 | 陳睿彪 |

## 1. Abstract 摘要
### A. Attention Getter — Motivation
IEA《Global Energy Review 2026》指出，2025 年全球用電需求增加約 3%，建築部門占用電增量近 45%。[D1] 建築能源管理需要把既有量測資料轉為可供追查的資訊；全球需求成長本身不代表個別建築存在浪費。
### B. But — Challenge
單純異常分數無法辨別天氣、營運變化與資料問題；總表資料也不足以確認設備根因。BDG2 cleaned 版本會移除部分離群與零值，且不提供本專題所需的現場根因真值。[D3][D6] 既有建築 LLM 工具研究亦出現查詢、分析與回答遺漏問題。[A4]
### C. Cure — Proposed Solution
為處理上述問題，本專題提出 Energy Detective 建築用電異常調查 AI Agent，讓管理者以自然語言指定建築與期間，取得附有數值、來源、適用規則及下一步查核事項的調查報告。
### D. Development — Method
系統擬使用 BDG2 歷史電表、天氣與建築中繼資料；由 Python 執行品質檢查、條件基準及異常事件分析，由受限規劃 Agent 選擇工具，並以明示領域規則約束推論。每項結論回連工具結果，資料不足時要求補充或回報無法判定。
### E. Experiments — Evaluation
以按時間切分的建築子集進行歷史重播，分開評估正常基準、合成事件與人工審閱案例；比較統計／預測方法及固定流程與 Agent。量測預測誤差、事件偵測、任務完成、證據正確性及成本。合成異常只驗證對指定擾動的敏感度，不代替真實故障標籤。
### F. Findings — Expected Outcomes
預期完成可重現的資料調查原型與附證據報告，並透過比較實驗確認 Agent 是否有助於調查完整度及限制過度推論。本階段尚未執行實驗；不宣稱提高準確率、證實設備故障或達成節電。

## 2. Introduction 緒論
'''
intro=section(domain,'## Introduction','## Deep Research：五項核心思維')
domain_table=section(domain,'## Related Work：領域 Article Summary Table','## 資料使用與授權查核')
ai_body=section(ai,'## Related Work','## 原始來源與查核範圍')
ai_body=ai_body.replace('## Article Summary Table','### AI Article Summary Table').replace('## 研究缺口與本專題定位','### Existing Research → Limitations → Research Gap → Our Project')
deep=section(domain,'## Deep Research：五項核心思維','## Related Work：領域 Article Summary Table')
deep='### Q1. 五個核心思維模式\n\n'+deep.replace('## Deep Research：三項關鍵爭論','### Q2. 三個重要專業爭論').replace('## Deep Research：十個深度研究問題','### Q3. 十個深度理解問題')
references=section(domain,'## 來源索引')+'\n\n'+section(ai,'## 原始來源與查核範圍').split('本次亦搜尋')[0]
proposal=abstract+intro+'\n\n## 3. Related Work 相關研究\n\n本章以五篇 AI 研究及五份領域研究／報告對照，兼顧 AI Technology 與 Domain Know-how。\n\n'+ai_body+'\n\n### 領域 Article Summary Table\n\n'+domain_table+'\n\n## 4. Deep Research\n\n'+deep+'\n\n## 5. Proposed Scheme / Proposed Design\n\n'+re.sub(r'^# .*\n','',design,count=1)+'\n\n'+re.sub(r'^# .*\n','',protocol,count=1)+'\n\n### 資料來源與授權\n\n'+section(domain,'## 資料使用與授權查核','## 來源索引')+'\n\n## 6. References\n\n'+references
(ROOT/'research/proposal_source.md').write_text(proposal,encoding='utf-8')

slides=[]
def add(title,items,source='',size=21):
    objs=[]
    count=len(items); gap=10; height=min(84,(400-gap*(count-1))/count)
    for i,t in enumerate(items): objs.append(rect(42,94+i*(height+gap),876,height,t,size,fill='FFFFFF'))
    slides.append(dict(title=title,objects=objs,source=source))
def two(title,left,right,source='',size=19):
    slides.append(dict(title=title,source=source,objects=[rect(42,98,430,390,left,size),rect(488,98,430,390,right,size)]))

add('Energy Detective｜建築用電異常調查 AI Agent',[
'第25組｜物聯網數據分析與應用 · Final Project Proposal',
'用公開電表與天氣資料，產出有依據的調查建議。',
'AI Agent ＋ Domain Knowledge ＋ Data Analytics',
'7114056008 侯如蓁　｜　7114056093 蔡奇勳\n7114056126 施秉榕　｜　7114056143 陳睿彪\n2026-11-11　｜　Proposal：系統與實驗尚未完成'],size=19)
add('研究動機｜為什麼值得做？',[
'2025 年全球用電需求約增 3%；建築占當年用電增量近 45%。',
'設施管理者需要從「曲線變高」判斷：要先查資料、天氣或營運排程？',
'公開總表可做初步調查，但不能直接確認某台設備故障。',
'目標：把異常訊號轉成可核對、能採取下一步行動的調查報告。'],source='[D1] IEA 2026；[D3] BDG2；[D8] DOE')
two('問題定義與專題範圍','使用情境\n\n使用者：校園／辦公建築設施管理者。\n\n輸入：建築 ID、期間與調查問題。\n\n輸出：異常事件、比較基準、證據、替代解釋與查核建議。','主要限制\n\n資料缺漏與尖峰未必是設備故障。\n\n夜間不一定無人使用。\n\n歷史偏離量不等於已實現節電。\n\nMVP：公開資料歷史重播；不接控制設備。',source='[D3][D6][D8]')

def table_slide(title,rows,source):
    widths=[48,52,115,127,115,112,165,142]
    heads=['Ref.','Year','Problem','AI Method','Domain','Dataset','Findings','Limitation']
    for start in range(0,len(rows),3):
        objects=[]; yy=94
        for j,row in enumerate([heads]+rows[start:start+3]):
            xx=42; hh=40 if j==0 else 110
            for ww,txt in zip(widths,row):
                objects.append(rect(xx,yy,ww,hh,txt,13 if j else 12,fill='DCEDEE' if j==0 else 'FFFFFF',line='CAD7DE'))
                xx+=ww
            yy+=hh
        slides.append(dict(title=title+f' {start//3+1}',objects=objects,source=source))
table_slide('Related Work｜AI Technology（完整表見提案）',[
['A1','2023','工具取得外部事實','ReAct\n推理＋動作','動作與觀察','QA／互動任務','多類任務有工具互動效益','可能重複動作；非建築'],
['A2','2025','可解釋異常偵測','Argos\n規則＋基礎模型','標註異常模式','KPI／Yahoo等','融合規則在文中比較中改善','依賴標註；非建築'],
['A3','2025','誤報人工複核','k-NN＋多模態LLM','曲線與背景','18個UCR子集','降低誤報伴隨漏報取捨','使用測試真值調參'],
['A4','2025','建築時序查詢','GPT-4o＋SPARQL／Python','Brick設備關係','FLEXLAB','氣流問題3/5成功','小案例；回答有遺漏'],
['A5','2025','異常類型與解釋','Time-RA\nLLM／微調','領域異常分類','RATs40K','展示分類與說明效益','AI說明非根因真值']], '[A1]–[A5]；2025 預印本按所讀版本引用')
table_slide('Related Work｜Domain Know-how',[
['D1','2026','需求為何成長','N/A\n統計分析','部門、天氣','2025全球統計','建築占新增用電近45%','不能推定單棟浪費'],
['D3','2020','公開建築基準','資料品質篩查','總表、場址、天氣','BDG2','1636建築、3053各類表','缺少設備根因標籤'],
['D7','2020','分析的實務價值','多種EIS／FDD','監測與營運改善','104組織、6500建築','EIS/FDD節能中位3%/9%','不可外推本專題'],
['D9','2025','建築模型適應','Chronos／LoRA','占用、負載、季節','SUSTIE','長上下文與微調影響表現','同棟；非故障驗證'],
['D8','未標年','如何驗證節能','N/A\n量測／回歸','基準與量測邊界','DOE指南','定義A–D量測驗證選項','非異常偵測實驗']], '[D1][D3][D7][D8][D9]；網頁查核 2026-11-11')
add('Research Gap → Our Project',[
'Existing Research：工具 Agent、建築查詢、異常偵測及文字解釋已有先例。',
'Limitations：資料品質、數值引用、條件假設與根因邊界仍須逐案檢查。',
'Research Gap：資訊有限時，如何形成完整且不過度推論的可追溯調查？',
'Our Project：Python 可重現分析＋受限工具規劃＋領域規則＋證據檢查。',
'預期貢獻：調查流程、證據格式與公平比較；是否改善由實驗回答。'],source='[A1]–[A5]；[D3][D8]',size=19)
add('Deep Research Q1｜五個核心思維',[
'① 正常必須有條件 → 同建築、星期／時段與天氣的可比較基準。[D1][D8]',
'② 先查資料品質 → 保留 raw 與品質旗標，避免把缺值當故障。[D6]',
'③ 統計偏離不等於根因 → 區分觀察、假說與還缺的現場證據。[D8]',
'④ 分析要能支援行動 → 合併事件，列優先調查事項與可核對證據。[D7]',
'⑤ 公開基準不保證泛化 → 最低版本按時間切分；跨建築為擴充。[D3]'],size=18)
two('Deep Research Q2｜三項專業取捨','1. 積極清理 ↔ 保留可疑讀值\n雙方依據：cleaned減少污染，但也移除離群與零值。[D6]\n共同原則：保留版本及品質旗標。\n未解：沒有現場紀錄時如何區分真異常？\n\n2. 零樣本模型 ↔ 本地調整\n依據：長上下文可改善零樣本；本地微調也有幫助。[D9]\n共同原則：同條件比較效果與成本。\n未解：多少資料值得調整？','3. 快速篩選機會 ↔ 完成節能驗證\n\n量化依據：實務分析支援營運改善。[D7]\n保留依據：節電需要介入後量測與調整基準。[D8]\n\n共同原則：區分偏離、機會與實際節電。\n未解：多少異常負載可不影響服務而消除？\n\n本專題：只報相對基準偏離量。',size=16)
two('Deep Research Q3｜十個深度理解問題','01 缺少故障標籤，如何評估事件？\n\n02 天氣與季節改變後，異常還成立嗎？\n\n03 raw／cleaned 會如何改變結論？\n\n04 如何區分停館、缺值與量測故障？\n\n05 何時應停止推論並要求補證據？','06 何時需逐棟／跨建築參照？\n\n07 工具證據是否真正支持文字主張？\n\n08 告警合併如何影響召回與查核負擔？\n\n09 Agent 增益來自規劃、規則或表達？\n\n10 確認根因與節電還需要哪些證據？',size=18)
add('Agent 使用情境｜從提問到調查',[
'使用者：「請調查指定建築在測試期間的夜間用電是否異常。」',
'Agent 確認建築、日期及時段；不清楚的必要欄位先補問。',
'工具依序查資料品質與同類時段基準，必要時比較天氣與事件持續時間。',
'報告列出觀測值、基準、時間窗、工具證據 ID、適用規則與替代解釋。',
'下一步：「核對排程與使用變化」；無設備資料就不宣告空調故障。'],size=19)

# Architecture will use the same numbered module contract as DESIGN.md.
objs=[]
labels=['① 需求解析\n與範圍驗證','② 受限規劃\n與工具控制','③ CSV取得\n與歷史重播','④ 時序資料\n品質檢查','⑤ 基準\n與異常分析','⑥ 領域規則\n與假說','⑦ 證據整合\n與報告','⑧ 離線評估']
for idx,label in enumerate(labels):
    row=idx//4; col=idx%4 if idx<4 else 7-idx; xx=42+col*225; yy=114+row*146
    objs.append(rect(xx,yy,201,80,label,18,fill='DCEDEE' if idx in [2,5] else 'FFFFFF',line='087E8B'))
    if row==0 and col<3: objs.append(rect(xx+202,yy+20,24,45,'→',18,fill=None))
    if row==1 and col>0: objs.append(rect(xx-23,yy+20,24,45,'←',18,fill=None))
objs.extend([rect(806,209,46,40,'↓',18,fill=None),rect(42,209,740,40,'② 依觀察選工具；④／⑤ 提供證據給 ⑦',16,fill=None),rect(42,369,876,100,'輸入：使用者指定建築與期間；資料：BDG2 電表＋天氣＋建築資訊\n⑦ 輸出可追溯報告；② 執行紀錄與 ⑦ 報告交給 ⑧ 離線評估。\n各工具將結果回傳 ②，查核不足時補問使用者或停止。',17)])
slides.append(dict(title='System Architecture｜八個主要模組',objects=objs,source='各模組責任與介面見 DESIGN.md',diagram='architecture'))
add('資料來源與前處理',[
'BDG2：2016–2017 每小時；1,636 建築、3,053 各類表；只取電力子集。',
'電表 raw/electricity.csv＋weather/weather.csv＋metadata/metadata.csv。',
'電量 kWh；依場址與時間對齊。檢查缺值、重複、零值及時間順序。',
'raw 也經初步整理；cleaned 已移除部分離群／零值，其敏感度比較列為擴充。',
'沒有已確認故障根因標籤；固定時間切分、保留資料版本及授權。'],source='[D3]–[D6]；完整資料路徑見提案',size=19)
two('AI / Analytics / Domain Knowledge','Python：數值分析\n\n品質檢查、條件基準、殘差、事件合併。\n\nLLM：受限工具選擇\n\n輸出結構化任務，只能呼叫已定義工具；不執行任意生成程式。\n\n所有數值由工具結果帶入。','Domain Knowledge：明示規則\n\n同類日／時段才比較。\n夜間不直接等於非營運。\n資料異常先分流。\n總表結論不得超出量測範圍。\n\nReport：觀察→基準→假說→缺少證據→下一步。',source='[A1][A4]；[D6][D8]',size=18)

# Remaining technical slides assembled from the actual finalized design in main.
(ROOT/'scripts/slides_base.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2),encoding='utf-8')
print('Assembled proposal source and first',len(slides),'slides.')
