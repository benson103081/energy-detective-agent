## ADDED Requirements

### Requirement: Request scope
系統 SHALL 驗證建築 ID、起訖日期及資料可用範圍，缺少資訊時要求補充。

#### Scenario: Missing building
- **WHEN** 提問未提供建築 ID
- **THEN** 回傳待補欄位，不自行選擇建築或開始分析

### Requirement: Replay boundary
系統 SHALL 僅讀取重播截止點以前的資料，並記錄資料版本與原始定位。

#### Scenario: Future data excluded
- **WHEN** 指定 replay_until 早於資料最後日期
- **THEN** 所有可見資料時間均不晚於 replay_until

### Requirement: Quality gate
系統 SHALL 在分析前核對單位、時間、重複、缺值、負值及有效率；未知單位或品質不足時停止數值分析。

#### Scenario: Insufficient electricity data
- **WHEN** 任一分割的有效率低於固定設定的 90%
- **THEN** 回傳 insufficient_data 與品質證據，不補零產生異常

### Requirement: Temporal evaluation
系統 SHALL 依固定時間切分訓練、校準與測試，僅使用訓練期擬合基準、校準期決定門檻。

#### Scenario: Test data isolated
- **WHEN** 修改保留測試期的觀測值
- **THEN** 已固定的基準參數與門檻保持相同，測試事件可改變

### Requirement: Deterministic analytics
系統 SHALL 由 Python 計算基準、殘差、事件及單位，禁止 LLM 生成未經工具計算的數值。

#### Scenario: Event merging
- **WHEN** 相鄰有效觀測均超過固定門檻且方向相同
- **THEN** 合併為同一事件；遇缺測或方向變化則分開

### Requirement: Conditional domain rules
系統 SHALL 依資料前置條件選擇規則，缺天氣、作息或可靠當地時間時停用相應解釋。

#### Scenario: Weather unavailable
- **WHEN** 電量合格但天氣無法對齊
- **THEN** 繼續用電分析、停用 weather_context 並記錄限制

### Requirement: Tool control
系統 SHALL 僅執行白名單工具及有效參數，每次調查最多 10 次工具呼叫且暫時性 I/O 最多重試一次。

#### Scenario: Unknown tool rejected
- **WHEN** 計畫包含任意 Shell、程式碼或未知工具
- **THEN** 拒絕執行並保存驗證錯誤，不執行生成程式

### Requirement: Evidence report
系統 SHALL 為每個數值結論提供 evidence_id、來源、期間、單位與假設；引用或數值驗證失敗時使用固定模板。

#### Scenario: Unsupported claim
- **WHEN** 報告草稿包含不存在的 evidence_id 或不一致數值
- **THEN** 驗證失敗，改以已登錄工具結果輸出模板

### Requirement: Inference boundary
系統 SHALL 區分觀察、待查假說、缺少證據及下一步，不由總表直接宣告設備根因或已實現節電。

#### Scenario: High night load
- **WHEN** 夜間用電高於基準但沒有設備狀態或維修紀錄
- **THEN** 列出排程及使用變化等替代解釋與查核需求，不確診設備故障

### Requirement: Comparable evaluation
評估 SHALL 使用相同資料與工具比較固定報表、固定流程搭配 LLM 與 Agent，分開報告合成事件及人工審閱結果。

#### Scenario: No real fault labels
- **WHEN** 資料沒有現場確認的根因標籤
- **THEN** 合成事件只評估指定擾動，不報告真實設備診斷準確率

### Requirement: Report field contract
系統 SHALL 以 evidence_id 與 field 指向原始數值，核對建築、期間、單位及值；日期 SHALL 採半開區間 [start, end)。

#### Scenario: Existing evidence with wrong unit
- **WHEN** evidence_id 存在但報告將 kWh 誤寫為 kW
- **THEN** 驗證失敗並以正確單位的工具證據模板取代

### Requirement: Registered evaluation cases
評估 SHALL 依 research/evaluation_protocol.md 固定 C01–C10，三組各重跑三次共90次，原始草稿與模板降級後結果分開保存。

#### Scenario: Repeated case evaluation
- **WHEN** 對相同案例進行三次重跑
- **THEN** 保存三次結果及失敗紀錄，不把重跑解讀為三名獨立使用者
