# Energy Detective：AI Related Work 與文獻比較

查核日期：2026-11-03。以下為可併入提案的文獻章節；「作者結果」指原文所報告的觀察，「本專題解讀／設計」則是本提案據此提出的選擇，並非既有實驗結果。主表收錄五篇已閱讀原始全文的研究，其中四篇為 2025 年研究；預印本不視為已通過同儕審查的期刊或會議成果。

## Related Work

### M. Methods：方法分類與比較

以下依工具推理、時序異常與建築資料分析分類，比較能力、證據與適用限制。

### 從回答問題到執行調查工具

ReAct 將語言模型的任務規劃、外部動作與觀察結果交替串接。作者在問答、查證及互動環境中顯示此流程的價值，但也觀察到重複動作及無效檢索造成的失敗。因此，Agent 的關鍵是根據工具回傳的證據調整行動；僅把電表摘要交給 LLM 改寫，尚不足以構成此類調查流程。[A1](https://arxiv.org/html/2210.03629v3)

在建築領域，Mulayim 等人已示範 GPT-4o 透過 Brick 語意模型查找資料，再產生 Python 程式分析 BAS 時序。其實驗也出現查詢錯誤、程式索引錯誤及回答遺漏感測器的情形。**本專題解讀：**建築資料分析 Agent 已有先例，本提案應強調異常調查流程與證據驗證，而非宣稱首次將 LLM 用於建築分析。[A4](https://eta-publications.lbl.gov/sites/default/files/2025-07/extraction_and_analysis_of_time_series_data.pdf)

### 數值偵測、領域知識與 LLM 的分工

Argos 使用 LLM 產生可執行規則，透過修復、審查及與既有偵測器融合來辨識雲端監控異常；它說明了可重現計算與語言模型協作的可行性。不過，規則學習需要已標註案例，且其驗證領域不是建築。**本專題解讀：**可借用「規則作為可檢查中介」的思想，但不能把其結果或 accuracy guarantee 當成 Energy Detective 的保證。[A2](https://arxiv.org/html/2501.14170v1)

Yang 等人讓多模態 LLM 複核傳統偵測器提出的候選異常，使用曲線圖與資料產生背景判斷誤報。全文結果呈現誤報降低與真異常保留率之間的取捨，並非普遍維持召回率。**本專題解讀：**應同時評估誤報與漏報，保留原始偵測結果及 LLM 的複核紀錄；不可只以回答流暢或告警減少認定系統改善。[A3](https://arxiv.org/html/2503.21833v1)

### 從異常標籤走向有證據的說明

Time-RA 將異常類別與文字說明納入時序任務，提出 RATs40K 與模型微調評估。這支持本專題將「異常在哪裡、屬於何種模式、憑什麼判斷」分開呈現。不過，該資料的說明包含 AI 輔助標註；能產生符合標註的解釋，不等於證實物理因果。**本專題解讀：**建築總表的高負載只能構成進一步調查線索，不能直接證明某設備故障。[A5](https://arxiv.org/html/2507.15066v1)

## Article Summary Table

### O. Organize：文獻比較表

表中的 Findings 均為作者結果；Limitation 若標示「外推限制」，代表本提案對研究適用範圍的判斷。

| Ref | Year | Problem | AI Method | Domain Knowledge | Dataset | Findings | Limitation |
|---|---|---|---|---|---|---|---|
| [A1](https://arxiv.org/html/2210.03629v3) ReAct | 2023；初稿 2022 | 單靠內部推理難以取得外部事實及更新行動 | 少量示例提示；交替進行任務推理、動作與觀察 | 任務動作定義、示例、檢索所得事實 | HotpotQA、FEVER、ALFWorld、WebShop | 多類任務展現工具互動效益；並非每項比較都勝過 CoT | 會陷入重複動作或受檢索失敗影響；外推限制：未驗證建築用電 |
| [A2](https://arxiv.org/html/2501.14170v1) Argos | 2025，預印本 v1 | 雲端異常偵測須兼顧解釋與重現 | GPT-4o 產生 Python 規則；修復與審查；融合基礎偵測器 | 標註案例、異常模式及既有偵測器輸出 | KPI、Yahoo、Microsoft 內部監控資料 | 文中評估顯示融合規則後優於所比較基準 | 依賴標註；使用 Event-F1 PA；報告多次試驗中的最佳結果；外推限制：不是未標註建築資料的效能保證 |
| [A3](https://arxiv.org/html/2503.21833v1) Refining Time Series Anomaly Detectors using Large Language Models | 2025，預印本 v1 | 傳統偵測器誤報需要人工複核 | k-NN 候選偵測＋Llama 多模態複核與多次投票 | 資料產生背景文字、候選與參照曲線 | Hexagon ML/UCR 異常資料庫的 18 個單變量資料集 | 多模態設定可降低誤報，但不同設定有不同漏報代價 | 以真異常長度及測試真值選近最佳偵測參數；每個測試序列只有一段真異常；外推限制：不等於部署成效 |
| [A4](https://eta-publications.lbl.gov/sites/default/files/2025-07/extraction_and_analysis_of_time_series_data.pdf) Extraction and Analysis of Time Series Data from Building Automation Systems Using Large Language Models | 2025，會議論文／LBNL 公開稿 | 建築使用者難以查詢語意模型與分析時序 | GPT-4o；相似查詢範例檢索；SPARQL 與 Python 生成；錯誤重試 | 既有 Brick 模型、設備關係、專家查詢範例 | LBNL FLEXLAB 兩個測試空間的 BAS 與 Brick 模型 | 三個問題各測五次；氣流下降問題成功 3/5；部分回答遺漏感測器 | 小規模案例；依賴預先建好的語意模型；模型自行假設異常閾值可能不符使用者需求 |
| [A5](https://arxiv.org/html/2507.15066v1) Time-RA | 2025，預印本 v1 | 二元異常標籤缺少細分類與解釋 | LLM／多模態模型評估、LoRA 微調、AI 回饋輔助標註 | 領域背景、專家定義異常類型、文字與圖像 | RATs40K：跨領域數值、文字與視覺樣本 | 作者展示微調對異常分類與說明任務的效益 | 作者指出同段多類異常可能只輸出主要類型；外推限制：AI 輔助說明不是設備根因的獨立真值 |

## 研究缺口與本專題定位

### N. New proposed：研究缺口與本專題定位

上述研究已涵蓋 Agent 工具使用、規則生成、異常複核與建築資料查詢。本專題的切入點是：**在建築總表與天氣時序、設備資訊不足的條件下，如何把可重現的數值異常轉成有證據、可追查且不超出資料能力的調查建議？**這是本提案選定的實作與驗證問題，不是宣稱所有文獻都未處理過此組合，也不主張演算法首創。

Energy Detective 擬以 Building Data Genome 2 的電表與天氣時序為基礎，先由 Python 執行品質檢查、統計基準或預測殘差計算，產生候選事件；再由 LLM 選擇已定義的工具，查詢同星期／同時段基準、天氣關係、持續時間與資料缺漏，並根據工具結果提出下一步調查。這項分工保留可重跑的數值證據，也提供可觀察的工具選擇與流程調整，形成超出單輪聊天摘要的 Agent 功能。

領域規則應以明確條件保存，例如「相對歷史同類日的夜間基載偏高」或「高殘差同時伴隨資料缺漏」。夜間不直接等於無人使用；假日或營運時段若無可靠來源，只能標為分析假設。事件報告應逐項列出時間窗、觀測值、基準、殘差、規則版本、工具結果、尚缺資料及建議查核事項。可提出「請確認排程或占用變化」，不能從總表直接宣告「某台空調未關閉」。

預期貢獻是可驗證的調查流程與報告品質，並須經實驗確認。建議至少比較「固定偵測器＋固定報告」、「固定流程＋LLM 摘要」與「可選擇工具的 Agent」；以相同候選案例評估證據引用正確率、必要查核完成率、無根據根因斷言率、工具失敗率與成本，分離 Agent 的額外效益。如果測試 LLM 改判異常，另計誤報與漏報。人工複核或注入異常所得標籤須清楚標示，不得包裝為真實設備故障紀錄。預測基準與觀測用電的差額只屬分析差額；沒有實際介入及反事實驗證，就不能宣稱已達成節電。

## 原始來源與查核範圍

- **[A1]** Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023；初稿於 2022 年公開。[原始全文 v3](https://arxiv.org/html/2210.03629v3)。查閱方法、資料集、結果及失敗分析。
- **[A2]** Gu, Y., et al. (2025). *Argos: Agentic Time-Series Anomaly Detection with Autonomous Rule Generation via Large Language Models*. arXiv:2501.14170v1。[原始全文](https://arxiv.org/html/2501.14170v1)。查閱規則訓練、融合設計、資料集與評估設定。本文未轉用其提升百分比作為專題預期績效。
- **[A3]** Yang, A., Chen, Y., Lee, S., & Montes, V. (2025). *Refining Time Series Anomaly Detectors using Large Language Models*. arXiv:2503.21833v1。[原始全文](https://arxiv.org/html/2503.21833v1)。查閱方法、參數設定、Table 1 與附錄；採全文結果判讀誤報／漏報取捨。
- **[A4]** Mulayim, O. B., Prakash, A. K., Paul, L., & Pritoni, M. (2025). *Extraction and Analysis of Time Series Data from Building Automation Systems Using Large Language Models*. DOI: 10.20357/B73W4C。[LBNL 官方書目](https://eta.lbl.gov/publications/extraction-and-analysis-time-series)、[公開全文 PDF](https://eta-publications.lbl.gov/sites/default/files/2025-07/extraction_and_analysis_of_time_series_data.pdf)。查閱方法、FLEXLAB 設定、Table 1、個案結果與討論；成功次數不等於每次文字回答均完整。
- **[A5]** Yang, Y., et al. (2025). *Time-RA: Towards Time Series Reasoning for Anomaly with LLM Feedback*. arXiv:2507.15066v1。[原始全文](https://arxiv.org/html/2507.15066v1)。查閱任務、資料建構、評估及限制。所讀版本含尚未完成的會議 DOI 模板，故只按可確認的 arXiv 版本引用，不推定正式會議出版狀態。

本次亦搜尋 2026 年建築能耗異常研究，但部分出版社原始全文無法取得；未以搜尋摘要替代全文查核，也未為增加年份而納入主比較表。
