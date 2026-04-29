document.addEventListener('DOMContentLoaded', function() {
    const addIngredientBtn = document.getElementById('add-ingredient');
    const ingredientList = document.getElementById('ingredient-list');
    
    if (addIngredientBtn && ingredientList) {
        addIngredientBtn.addEventListener('click', function() {
            const row = document.createElement('div');
            row.className = 'row mb-2 ingredient-row animate-fade-in';
            row.innerHTML = `
                <div class="col-6">
                    <input type="text" class="form-control" name="ingredient_name[]" placeholder="名稱 (例: 鹽)">
                </div>
                <div class="col-4">
                    <input type="text" class="form-control" name="ingredient_quantity[]" placeholder="份量 (例: 1茶匙)">
                </div>
                <div class="col-2">
                    <button type="button" class="btn btn-outline-danger w-100 remove-btn"><i class="bi bi-trash"></i></button>
                </div>
            `;
            ingredientList.appendChild(row);
        });
    }

    const addStepBtn = document.getElementById('add-step');
    const stepList = document.getElementById('step-list');
    
    if (addStepBtn && stepList) {
        addStepBtn.addEventListener('click', function() {
            const row = document.createElement('div');
            row.className = 'row mb-2 step-row animate-fade-in';
            row.innerHTML = `
                <div class="col-10">
                    <textarea class="form-control" name="step_content[]" rows="2" placeholder="詳細步驟..."></textarea>
                </div>
                <div class="col-2 d-flex align-items-center">
                    <button type="button" class="btn btn-outline-danger w-100 remove-btn"><i class="bi bi-trash"></i></button>
                </div>
            `;
            stepList.appendChild(row);
        });
    }

    // 使用事件委派處理刪除按鈕
    document.addEventListener('click', function(e) {
        if (e.target && (e.target.classList.contains('remove-btn') || e.target.closest('.remove-btn'))) {
            const btn = e.target.closest('.remove-btn');
            btn.closest('.row').remove();
        }
    });
});
