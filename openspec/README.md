# Energy Detective OpenSpec 工作流程

目前是 Proposal 階段。`changes/energy-investigation-workflow/` 為待實作能力，尚未封存；`specs/` 尚無已完成系統規格。

1. `proposal.md`：說明為何改、改哪些內容。
2. `specs/energy-investigation/spec.md`：需求及 WHEN／THEN 驗收情境。
3. `design.md`：把根目錄 DESIGN.md 對應成工作流程與決策。
4. `tasks.md`：本次文件項目已完成；後續程式與實驗保持未勾選。
5. 後續依規格實作、驗證，再封存更新正式 specs。

安裝及檢查：

```powershell
npm install -g @fission-ai/openspec@2.0.0
openspec list
openspec validate energy-investigation-workflow --strict
```

本次 CLI 2.0.0 安裝在工作區的 `.dic3-tools`，不納入繳交；驗證結果見 `validation.txt`。驗證僅證明規格格式通過，不代表系統功能已實作。

參考官方文件：https://github.com/Fission-AI/OpenSpec
