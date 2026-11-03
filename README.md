# Energy Detective：建築用電異常調查 AI Agent

「物聯網數據分析與應用」期末專題提案。本階段交付研究、系統設計與簡報，系統程式與實驗尚未完成。

Repository：<https://github.com/benson103081/energy-detective-agent>。組員與學號將於繳交前補上。

## 提案交付

- [Proposal.docx](deliverables/Proposal.docx)：提案文件（可編輯）。
- [Proposal.html](deliverables/Proposal.html)：下載後可在瀏覽器閱讀與列印的提案文件；請連同 `assets/` 圖檔下載。
- [Proposal.pptx](deliverables/Proposal.pptx)：Proposal 簡報（可編輯）。
- [Proposal-slides.pdf](deliverables/Proposal-slides.pdf)：簡報閱讀版。
- [DESIGN.md](DESIGN.md)：架構、元件、資料流、演算法、實作對應與預定驗證方式。
- [research/](research/)：查核來源與整合前研究稿。

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

## 階段狀態

本 Repository 收錄 Proposal 文件、PPT 與 DESIGN.md。期末實作須另完成真實實驗、結果比較、結論、至少 21 頁 Final PPT，以及超過 10 分鐘的 YouTube 簡報與 Demo。

