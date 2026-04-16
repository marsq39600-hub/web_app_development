# 流程圖設計

以下是「食譜收藏夾」的使用者操作流程，以及背後的系統資料流動流程。視覺化的圖表將幫助我們釐清各個功能的頁面切換機制與資料儲存的運作邏輯。

## 1. 使用者流程圖 (User Flow)

這張圖展示了從使用者開啟網站開始，可能採取的各項操作流程。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 食譜列表]
    Home --> Choice{想要做什麼？}
    
    Choice -->|想加新菜| Add[點擊「新增食譜」]
    Add --> FormCreate[填寫新食譜表單<br>包含菜名、簡介、材料、步驟]
    FormCreate --> SubmitCreate{送出表單}
    SubmitCreate -->|成功| Home
    SubmitCreate -->|驗證失敗/取消| FormCreate

    Choice -->|瀏覽某食譜| Detail[點選某道食譜]
    Detail --> ViewRecipe[查看食譜詳情頁面]
    ViewRecipe --> Action{其他操作}
    
    Action -->|返回首頁| Home
    
    Action -->|修改內容| Edit[點擊「編輯食譜」]
    Edit --> FormEdit[進入修改內容表單]
    FormEdit --> SubmitEdit{送出修改}
    SubmitEdit -->|成功| ViewRecipe
    SubmitEdit -->|取消| ViewRecipe

    Action -->|不想要了| Delete[點擊「刪除食譜」]
    Delete --> ConfirmDelete{確認刪除？}
    ConfirmDelete -->|是| Home
    ConfirmDelete -->|否| ViewRecipe
```

---

## 2. 系統序列圖 (Sequence Diagram)

這裡以最核心的功能**「新增食譜」**為例，展示從使用者點擊送出表單，到資料最後存入 SQLite 的完整溝通流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 使用者瀏覽器
    participant Flask as Flask (Controller)
    participant Model as SQLAlchemy (Model)
    participant DB as SQLite (database.db)

    User->>Browser: 填寫「新增食譜」表單並送出
    Browser->>Flask: 發送 POST 請求 (攜帶表單資料)<br>路徑：/recipe/create
    
    activate Flask
    Flask->>Flask: 驗證表單資料(如必填欄位是否空白)
    opt 資料不完整
        Flask-->>Browser: 返回新增頁面並顯示錯誤訊息
    end
    
    Flask->>Model: 準備建立新的 Recipe 物件資料
    activate Model
    Model->>DB: 轉換為 SQL INSERT 語法並執行
    activate DB
    DB-->>Model: 寫入成功
    deactivate DB
    Model-->>Flask: 回傳建立成功
    deactivate Model
    
    Flask-->>Browser: 回傳 HTTP 302 重導向 (Redirect)
    deactivate Flask
    
    Browser->>Flask: 收到 302，對首頁發送 GET 請求
    Flask-->>Browser: 回傳擁有最新食譜列表的 HTML
```

---

## 3. 功能清單對照表

根據前面的架構規劃與使用者流程，我們定義了在後端開發時需要實作的路由以及 HTTP 方法。

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁 (食譜列表)** | `/` | GET | 顯示所有已收藏的私人食譜名稱列表。 |
| **新增食譜 (顯示表單)** | `/recipe/create` | GET | 渲染並顯示空白的食譜填寫表單給使用者。 |
| **新增食譜 (處理送出)** | `/recipe/create` | POST | 接收填妥的資料，寫入資料庫並重新導回首頁。 |
| **查看食譜詳情** | `/recipe/<int:id>` | GET | 根據該食譜的 id，從資料庫撈取並顯示所有詳細內容。 |
| **編輯食譜 (顯示表單)** | `/recipe/<int:id>/edit` | GET | 顯示舊有資料表單供使用者修改。 |
| **編輯食譜 (處理更新)** | `/recipe/<int:id>/edit` | POST | 儲存更新後的資料並重導回該筆詳情頁面。 |
| **刪除食譜** | `/recipe/<int:id>/delete` | POST | 刪除指定的食譜並重導向至首頁。<br>*(防止誤觸或被搜尋引擎機器人拜訪刪除，故使用 POST)* |
