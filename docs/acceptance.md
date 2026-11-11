# 作業規範與交付核對

狀態分為「文件已提供」「規劃待執行」「待組員填寫」。Proposal 與 Final Handover 是不同階段；沒有實驗結果不應填上虛構數字，也不應把期末影片要求誤當 Proposal 已完成項目。

## Proposal 評分對照

| 評分項目 | 比例 | 可檢查內容 | 位置 |
|---|---|---|---|
| Introduction | 20% | A–F、2026 IEA 動機、使用者、問題、創新與可否證研究問題 | Proposal 第 1、2 章及第 5 章實驗協議 |
| Related Work | 20% | 5 篇 AI＋5 份領域來源；各表含 Ref/Year/Problem/AI Method/Domain Knowledge/Dataset/Findings/Limitation；研究缺口 | Proposal 第 3、6 章 |
| Deep Research | 20% | 五種思維的意義／證據／設計；三個爭論的正反證據／共識邊界／未解問題；十題與判讀要點 | Proposal 第 4 章 |
| Agent 與 Architecture | 20% | ①–⑧、模組責任、工具契約、觀察後決策、輸入輸出例 | Proposal 第 5 章、DESIGN.md |
| Flowchart＋Pseudocode＋可行性 | 15% | 分支、循環、失敗與補問；有行號演算法；資料切分、三組對照、成本與時程 | Proposal 第 5 章 |
| GitHub＋DESIGN.md＋完整度 | 5% | 正式 repo、可重建文件、設計／程式對應、提交檔案 | README、DESIGN、scripts、deliverables |

上述是內容對照，不是教師評分或滿分保證。組員仍須能口頭說明來源、設計及驗證方式。

## Proposal 繳交前

- [x] Proposal 文件：Abstract、Introduction、Related Work、Deep Research、Proposed Scheme、References。
- [x] 可編輯 DOCX 與 PPTX、HTML 與簡報 PDF 閱讀版。
- [x] 建立正式 GitHub Repository 與 DESIGN.md。
- [x] 區分實際來源結果、設計假設、教學合成例及預期成果。
- [x] 提供文獻原始連結、來源到設計的對應、人工評分與失敗案例規格。
- [ ] 由組員填寫姓名、學號、分工、實際截止日期；目前未提供，不能代填。
- [ ] 在繳交電腦以 Word／PowerPoint 開啟檢查分頁及字型，試講並確認教師要求的命名方式。

## Final Handover 待完成

| 項目 | 必須提供的實物／證據 | 目前狀態 |
|---|---|---|
| Source Code | 真正執行的工具、Agent、CLI、鎖定依賴與測試 | 規劃待執行 |
| Data | 固定上游 commit、下載程序、授權、hash、欄位字典、選樣紀錄 | 來源已提供；資料處理待執行 |
| README | 全新環境可照做的安裝、執行、Demo、故障排除 | 文件建置可執行；Agent 指令仍為預定 |
| DESIGN | 已實作模組、真實資料流、模型設定、結果、限制及程式位置 | Proposal 設計已提供，須隨實作更新 |
| Experiments | 原始輸出、評分表、比較圖表、失敗案例及可重現命令 | 協議已提供；實驗待執行 |
| Final PPT | 超過 20 頁，含真實方法、結果、比較、結論 | Proposal PPT 不等於 Final PPT |
| Final Video | YouTube 簡報＋可運作 Demo，實際片長超過 10 分鐘 | 尚未錄製／上傳 |
| Conclusion | 貢獻、限制、Future Work；結論受結果支持 | 預期貢獻已提供；實證結論待執行 |

## 四週工作與交接

| 週次 | 工作 | 驗收實物 | 建議角色（待組員認領） |
|---|---|---|---|
| 1 | 資料版本、欄位、品質、時區與選樣 | manifest＋品質報告＋固定時間切分 | 資料負責人 |
| 2 | B0/B1、校準、事件、合成注入 | 分析測試＋可重跑數值結果 | 分析負責人 |
| 3 | LLM 需求／計畫、規則、證據驗證與模板 | 十個案例 fixture＋執行紀錄 | Agent 負責人 |
| 4 | 三組比較、雙人審閱、結果整理、錄影 | metrics＋評分表＋Final PPT＋YouTube 連結 | 驗證與整合負責人 |

角色可由同一人兼任；人工審閱若無法安排兩人，應如實揭露。外部 API 不可用時先完成確定性工具與模板，LLM 指標保留待測，不用 mock 回應冒充真實 Agent 實驗。

## AI 使用揭露與口試準備

本次文件修訂使用 AI 協助整理作業對照、研究問題、文獻摘要、設計契約、實驗協議及文件建置程式。正式提交前，組員應逐項查原始來源、能重算合成例、說明每個工具與停止條件，並記錄實際使用工具及人工查核工作。不可把 AI 草稿直接當成實驗結果或親自執行的使用者訪談。

建議準備三段口頭操作：解釋同星期／小時基準；展示天氣缺漏時為何仍能分析用電；從報告中的數字回查證據、原始資料位置與程式計算。十個深度問題的判讀要點見 Proposal 第 4 章。
