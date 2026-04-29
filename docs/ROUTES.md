# 路由設計文件 (ROUTES)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (食譜列表) | GET | `/` | `templates/index.html` | 顯示所有已收藏的食譜清單 |
| 新增食譜頁面 | GET | `/recipe/create` | `templates/create.html` | 顯示新增食譜表單 |
| 建立食譜 | POST | `/recipe/create` | — | 接收表單資料，寫入 DB 並重導向至首頁 |
| 食譜詳情 | GET | `/recipe/<int:id>` | `templates/detail.html` | 顯示單一食譜詳細內容（簡介、材料、步驟） |
| 編輯食譜頁面 | GET | `/recipe/<int:id>/edit` | `templates/edit.html` | 顯示編輯食譜表單並帶入原有資料 |
| 更新食譜 | POST | `/recipe/<int:id>/edit` | — | 接收更新資料，寫入 DB 並重導向至詳情頁 |
| 刪除食譜 | POST | `/recipe/<int:id>/delete` | — | 刪除該食譜相關紀錄，並重導向至首頁 |

## 2. 每個路由的詳細說明

### 首頁 (食譜列表) `GET /`
- **輸入**: 無
- **處理邏輯**: 呼叫 `Recipe.get_all()` 取得所有食譜清單。
- **輸出**: 渲染 `index.html` 並傳遞食譜清單資料。
- **錯誤處理**: 若無任何食譜，前端模板顯示提示訊息「尚無食譜，快來新增吧！」。

### 新增食譜頁面 `GET /recipe/create`
- **輸入**: 無
- **處理邏輯**: 準備渲染表單頁面。
- **輸出**: 渲染 `create.html`。
- **錯誤處理**: 無特殊錯誤。

### 建立食譜 `POST /recipe/create`
- **輸入**: 表單欄位包含 `title`、`description`，以及多個動態材料 (`ingredient_name[]`, `ingredient_quantity[]`) 與多個動態步驟 (`step_content[]`)。
- **處理邏輯**:
  1. 驗證必填欄位 (`title` 是否空白)。
  2. 呼叫 `Recipe.create()` 新增食譜主檔。
  3. 迴圈讀取材料與步驟陣列，分別呼叫 `Ingredient.create()` 與 `Step.create()` 以建立關聯。
- **輸出**: 重導向至 `/`。
- **錯誤處理**: 若 `title` 為空，提示錯誤訊息並重新渲染 `create.html`，並盡可能保留已填寫內容。

### 食譜詳情 `GET /recipe/<int:id>`
- **輸入**: URL 參數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)` 取得食譜主檔及其對應的材料與步驟（可透過 ORM lazy load 或 explicit query）。
- **輸出**: 渲染 `detail.html` 並傳遞該食譜物件。
- **錯誤處理**: 若找不到對應 `id` 的食譜，顯示「找不到該食譜」錯誤訊息並重導向至 `/`。

### 編輯食譜頁面 `GET /recipe/<int:id>/edit`
- **輸入**: URL 參數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)` 取得該食譜現有資料。
- **輸出**: 渲染 `edit.html` 並帶入既有資料至表單，讓使用者可以在畫面上直接修改。
- **錯誤處理**: 若找不到對應 `id` 的食譜，回傳 404 或重導向至 `/`。

### 更新食譜 `POST /recipe/<int:id>/edit`
- **輸入**: URL 參數 `id`，表單更新內容（包含主檔文字欄位與多個材料、步驟欄位）。
- **處理邏輯**:
  1. 呼叫 `Recipe.get_by_id(id)` 取得欲編輯的食譜。
  2. 呼叫該食譜實例的 `update()` 方法更新標題及描述。
  3. 針對材料和步驟：為了避免比對增刪的繁瑣邏輯，可先刪除該 `recipe_id` 底下所有舊的材料與步驟，接著再把表單傳來的新清單透過迴圈重新建立。
- **輸出**: 重導向至 `/recipe/<id>` (詳情頁面) 預覽更新後結果。
- **錯誤處理**: 若資料格式不符或找不到食譜，則提示錯誤或 404。

### 刪除食譜 `POST /recipe/<int:id>/delete`
- **輸入**: URL 參數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)` 並執行實例的 `delete()`（關聯的材料與步驟由於資料庫層級或 SQLAlchemy 的 cascading delete 將會被一併刪除）。
- **輸出**: 重導向至 `/`。
- **錯誤處理**: 若找不到該筆資料，忽略該動作並直接重導向至 `/`。

## 3. Jinja2 模板清單

所有的 HTML 頁面均繼承自 `base.html`，以保持共同的外觀配置與減少重複程式碼。

- `templates/base.html`: 共同母版。包含 `<head>`、CSS 與 JS 的引入，以及全站共用的導覽列（包含回到首頁、網站標題與「新增食譜」按鈕）及 Footer。
- `templates/index.html`: 繼承 `base.html`。首頁視圖，預計用網格(Grid)或列表卡片顯示所有食譜縮圖或摘要。
- `templates/detail.html`: 繼承 `base.html`。詳情頁，清楚排版顯示單一食譜的簡介、材料清單及條列式的烹飪步驟，並提供「編輯」與「刪除」操作按鈕。
- `templates/create.html`: 繼承 `base.html`。顯示新增食譜的表單。當中將包含動態新增「材料列」與「步驟列」的前端 JS 邏輯。
- `templates/edit.html`: 繼承 `base.html`。顯示可修改的食譜表單。介面預計與 `create.html` 高度相似，但預先填有舊資料。

## 4. 路由骨架程式碼
對應的路由邏輯骨架已建立於 `app/routes/main_routes.py` 檔案中。
