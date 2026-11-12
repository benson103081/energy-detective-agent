# Energy Detective：建築用電異常調查 AI Agent

組別：第25組

「物聯網數據分析與應用」期末專題提案。本階段交付研究、系統設計與簡報，系統程式與實驗尚未完成。

Repository：<https://github.com/benson103081/energy-detective-agent>。

## 組員（依學號排序）

| 學號 | 姓名 |
|---|---|
| 7114056008 | 侯如蓁 |
| 7114056093 | 蔡奇勳 |
| 7114056126 | 施秉榕 |
| 7114056143 | 陳睿彪 |

## 提案交付

- [Proposal.docx](deliverables/Proposal.docx)：提案文件（可編輯）。
- [Proposal.html](deliverables/Proposal.html)：下載後可在瀏覽器閱讀與列印的提案文件；請連同 `assets/` 圖檔下載。
- [Proposal.pptx](deliverables/Proposal.pptx)：Proposal 簡報（可編輯）。
- [Proposal-slides.pdf](deliverables/Proposal-slides.pdf)：簡報閱讀版。
- [DESIGN.md](DESIGN.md)：架構、元件、資料流、演算法、實作對應與預定驗證方式。
- [research/](research/)：查核來源與整合前研究稿。
- [完整提案 Markdown](research/proposal_source.md)：可直接在 GitHub 閱讀。
- [實驗協議](research/evaluation_protocol.md)：研究問題、選樣、十個案例、指標、三組對照與結果表。
- [作業與交付核對](docs/acceptance.md)：Proposal 評分對照及 Final Handover 待完成事項。

本版修訂補入建築模型適應的 2025 研究，形成 5 篇 AI＋5 份領域來源；十個深度問題另附判讀要點。Proposal PPT 為 30 頁，仍是提案簡報，不能代替包含實測結果的 Final PPT。

## 專題介紹

以 Building Data Genome 2 公開歷史建築電表及天氣資料，設計能選用分析工具、檢查資料品質、辨識異常用電時段並提供附帶證據調查建議的領域 Agent。透過歷史資料重播示範 IoT 資料分析流程；不需要購買感測器。

Agent 的輸出是待查假說與下一步檢查建議，不能僅憑總表證明設備故障，也不能把異常用電估計當成已驗證的節能量。

## 資料來源

- Building Data Genome 2：<https://github.com/buds-lab/building-data-genome-project-2>
- 資料論文：<https://doi.org/10.1038/s41597-020-00712-x>
- 下載與再散布前應遵守原資料庫授權、保留來源及必要聲明。本 Repository 目前不包含原始資料。

## Installation / How to Run / Demo

Proposal 文件可直接開啟，不需要安裝應用程式。系統尚在設計階段，目前沒有可執行的 Agent 或 Demo；預定環境、入口及資料準備步驟詳見 `DESIGN.md`，其中標為規劃中的指令尚不能執行。

正式實作時須補上鎖定版本的依賴、資料下載與前處理、啟動指令、測試方式及 Demo。不得把規劃指令視為已通過驗證。

## 重建 Proposal 文件（現在可執行）

需要 Python 3.9 或以上。從專案根目錄執行，依作業系統選一組；這些指令只重建文件，不會呼叫 LLM API 或執行用電實驗。

Linux／macOS：

```bash
python3 -m venv .build-deps
.build-deps/bin/python -m pip install -r requirements-docs.txt
.build-deps/bin/python scripts/build_all.py
```

Windows PowerShell：

```powershell
py -m venv .build-deps
.build-deps\Scripts\python.exe -m pip install -r requirements-docs.txt
.build-deps\Scripts\python.exe scripts/build_all.py
```

產物為 `deliverables/Proposal.docx`、`Proposal.html`、`Proposal.pptx`、`Proposal-slides.pdf` 及兩張 `assets/` 圖。預覽 PDF 使用 PyMuPDF 內建中文字型，不再依賴 Windows 路徑；可透過 `ENERGY_DOC_FONT` 指定本機字型檔。PPTX 使用可編輯文字與圖形，Office 顯示結果可能受字型替代影響，繳交前仍須開啟檢查。

文件來源與建置順序：

1. 編輯 `research/domain_research.md`、`ai_research.md`、`proposed_scheme.md` 與 `evaluation_protocol.md`。
2. `assemble_proposal.py` 合成 `research/proposal_source.md` 及簡報前半部；摘要與前半部簡報內容在該腳本中。
3. `finish_slides.py` 加入技術、驗證與交付簡報；`build_deliverables.py` 產生各格式。
4. `verify_deliverables.py` 驗證 Office XML、頁數一致、PDF 邊界、文獻／問題數量、偽碼行號與本機連結。

`proposal_source.md`、`slides_base.json`、`slides.json` 與交付檔是產生檔，直接修改後會在重建時被覆寫。若修改系統方法，也須同步更新 `DESIGN.md`；請以實驗協議作為案例與指標定義的共同依據。

常見問題：找不到 `fitz` 或 `markdown` 時，確認使用上面虛擬環境的 Python；產生程式若報文字溢出，拆頁或縮短文字後重新建置；HTML 圖片無法顯示時，確認保留 `assets/` 與 `deliverables/` 的相對位置。

## 研究問題與成功條件

- RQ1：B1 是否比 B0 更符合保留期間的用電型態？以同一批有效點比較 MAE。
- RQ2：Agent 能否維持必要資訊與證據品質，同時減少不必要規則評估？比較固定模板、固定流程＋LLM、受限 Agent。
- RQ3：證據檢查能否拒絕錯 ID、數值、單位與對象？以故意置錯的契約案例和人工語意審閱驗證。

失敗與零改善也是結果。所有效能欄位目前是「待測」；[合成計算例](research/proposed_scheme.md)僅用來解釋 240 kWh 偏離量的算法，不是 BDG2 的實驗成果。

## 階段狀態

本 Repository 收錄 Proposal 文件、PPT 與 DESIGN.md。期末實作須另完成真實實驗、結果比較、結論、至少 21 頁 Final PPT，以及超過 10 分鐘的 YouTube 簡報與 Demo。

## DIC3 提案重構

本版保留第25組組員、實驗協議及既有簡報，將摘要 A–F、Introduction G–L、Related Work M–O 對齊課堂架構，並把系統設計轉成 OpenSpec 需求與驗收情境。

- 提案：[Proposal.docx](deliverables/Proposal.docx)
- 簡報：[Proposal.pptx](deliverables/Proposal.pptx)（30頁）
- 系統設計：[DESIGN.md](DESIGN.md)
- 規格與流程：[openspec/README.md](openspec/README.md)

OpenSpec 的格式驗證不代表 Agent 已實作；後續程式及實驗任務保持未完成。

合併前版本保留為 `before-dic3-20261112` 標籤。DIC3 透過 `dic3-refactor` 分支整合；若需撤回，可對合併 commit 執行 `git revert -m 1 <merge-commit>`，保留歷史。
