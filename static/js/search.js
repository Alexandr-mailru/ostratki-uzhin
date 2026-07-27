(function () {
    const input = document.getElementById('ingredients-input') || document.querySelector('input[name="ingredients"]');
    const cards = document.querySelectorAll('.product-card');
    const tagsContainer = document.getElementById('selected-ingredients');
    const emptyHint = document.getElementById('fridge-empty');
    const countEl = document.getElementById('fridge-count');
    const submitBtn = document.getElementById('submit-btn');
    const mobileBtn = document.getElementById('mobile-search-btn');
    const mobileBar = document.getElementById('mobile-bar');
    const loading = document.getElementById('loading');
    const form = document.getElementById('search-form');

    const saved = input?.value
        ? input.value.split(/[,\n]/).map(s => s.trim()).filter(Boolean)
        : [];
    const selected = new Set(saved);

    function updateFridgeUI() {
        if (!input || !tagsContainer) return;
        input.value = Array.from(selected).join(', ');
        const count = selected.size;
        if (countEl) countEl.textContent = count;
        if (emptyHint) emptyHint.style.display = count ? 'none' : 'block';
        if (submitBtn) submitBtn.disabled = count === 0;
        if (mobileBtn) {
            mobileBtn.disabled = count === 0;
            mobileBtn.textContent = count ? `Найти рецепты (${count})` : 'Найти рецепты';
        }
        if (mobileBar) mobileBar.classList.toggle('is-visible', count > 0);

        tagsContainer.innerHTML = '';
        selected.forEach(name => {
            const tag = document.createElement('button');
            tag.type = 'button';
            tag.className = 'fridge-tag';
            tag.title = 'Убрать';
            tag.innerHTML = `${name}<span class="fridge-tag__x">×</span>`;
            tag.addEventListener('click', () => {
                selected.delete(name);
                updateFridgeUI();
            });
            tagsContainer.appendChild(tag);
        });

        cards.forEach(card => {
            card.classList.toggle('is-selected', selected.has(card.dataset.ingredient));
        });
    }

    cards.forEach(card => {
        card.addEventListener('click', () => {
            const name = card.dataset.ingredient;
            if (selected.has(name)) selected.delete(name);
            else selected.add(name);
            updateFridgeUI();
        });
    });

    document.querySelectorAll('.quick-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            chip.dataset.preset.split(',').forEach(raw => {
                const name = raw.trim();
                if (name) selected.add(name);
            });
            updateFridgeUI();
        });
    });

    function submitSearch() {
        if (selected.size === 0) return;
        loading?.classList.remove('d-none');
        form.submit();
    }

    submitBtn?.addEventListener('click', e => { e.preventDefault(); submitSearch(); });
    mobileBtn?.addEventListener('click', submitSearch);

    // Category tabs
    const catTabs = document.querySelectorAll('.cat-tab');
    const categories = document.querySelectorAll('.ingredient-category');
    catTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            catTabs.forEach(t => t.classList.remove('is-active'));
            tab.classList.add('is-active');
            const id = tab.dataset.cat;
            categories.forEach(cat => {
                cat.classList.toggle('hidden', id !== 'all' && cat.id !== id);
            });
        });
    });

    // Product search
    const searchInput = document.getElementById('ingredient-search');
    searchInput?.addEventListener('input', () => {
        const q = searchInput.value.trim().toLowerCase();
        cards.forEach(card => {
            const match = !q || card.dataset.ingredient.toLowerCase().includes(q);
            card.classList.toggle('hidden', !match);
        });
        categories.forEach(cat => {
            const visible = cat.querySelectorAll('.product-card:not(.hidden)').length > 0;
            cat.classList.toggle('hidden', q && !visible);
        });
        if (q) {
            catTabs.forEach(t => t.classList.remove('is-active'));
            document.querySelector('.cat-tab[data-cat="all"]')?.classList.add('is-active');
        }
    });

    updateFridgeUI();

    // Results rendering
    const data = window.APP_DATA || {};
    let recipes = data.recipes || [];
    let favorites = data.favorites || [];
    let activeFilter = 'all';

    function difficultyEmoji(label) {
        if (label === 'Сложно') return '🔥';
        if (label === 'Средне') return '👨‍🍳';
        return '⚡';
    }

    function filteredRecipes() {
        return recipes.filter(r => {
            if (activeFilter === 'complete' && r.missedIngredientCount > 0) return false;
            if (activeFilter === 'local' && !r.is_local) return false;
            if (activeFilter === 'quick' && (r.readyInMinutes || 999) > 30) return false;
            return true;
        });
    }

    function renderRecipes() {
        const container = document.getElementById('recipes-container');
        const countEl = document.getElementById('results-count');
        if (!container) return;

        const list = filteredRecipes();
        if (countEl) countEl.textContent = list.length;

        if (!list.length) {
            container.innerHTML = '<div class="empty-state"><p>По этому фильтру ничего нет</p></div>';
            return;
        }

        container.innerHTML = list.map(recipe => {
            const rid = String(recipe.id);
            const isFav = favorites.includes(rid);
            const pct = recipe.matchPercent ?? Math.round((recipe.usedIngredientCount / (recipe.totalIngredients || 1)) * 100);
            const badge = recipe.is_local
                ? '<span class="recipe-card__badge">Моя база</span>'
                : '<span class="recipe-card__badge recipe-card__badge--api">API</span>';

            return `
            <article class="recipe-card">
                <div class="recipe-card__img-wrap">
                    ${badge}
                    <img src="${recipe.image}" alt="${recipe.title}" loading="lazy"
                         onerror="this.src='https://placehold.co/400x240/d8f3dc/2d6a4f?text=🍽️'">
                </div>
                <div class="recipe-card__body">
                    <h3 class="recipe-card__title">${recipe.title}</h3>
                    <div class="match-bar"><div class="match-bar__fill" style="width:${pct}%"></div></div>
                    <p class="recipe-meta">
                        Совпадение ${pct}% · ${recipe.usedIngredientCount}/${recipe.totalIngredients} продуктов
                        ${recipe.readyInMinutes ? ` · ~${recipe.readyInMinutes} мин` : ''}
                        ${recipe.difficulty_label ? ` · ${difficultyEmoji(recipe.difficulty_label)} ${recipe.difficulty_label}` : ''}
                    </p>
                    <div class="recipe-card__actions">
                        <a href="/recipe/${rid}/" class="btn btn-green btn-sm">Рецепт</a>
                        <button type="button" class="btn btn-outline-secondary btn-sm fav-btn ${isFav ? 'is-on' : ''}" data-recipe-id="${rid}" aria-label="В избранное">♥</button>
                    </div>
                </div>
            </article>`;
        }).join('');

        container.querySelectorAll('.fav-btn').forEach(btn => {
            btn.addEventListener('click', () => toggleFavorite(btn));
        });
    }

    function toggleFavorite(btn) {
        const id = String(btn.dataset.recipeId);
        fetch(`/favorite/${id}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': data.csrf },
        })
        .then(res => res.json())
        .then(res => {
            if (res.is_favorite) {
                if (!favorites.includes(id)) favorites.push(id);
                btn.classList.add('is-on');
            } else {
                favorites = favorites.filter(f => f !== id);
                btn.classList.remove('is-on');
            }
            const badge = document.querySelector('.nav-pill__badge');
            if (badge) badge.textContent = res.count;
            else if (res.count > 0) {
                const favLink = document.querySelector('a[href*="favorites"]');
                if (favLink && !favLink.querySelector('.nav-pill__badge')) {
                    const span = document.createElement('span');
                    span.className = 'nav-pill__badge';
                    span.textContent = res.count;
                    favLink.appendChild(span);
                }
            }
        });
    }

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('is-active'));
            btn.classList.add('is-active');
            activeFilter = btn.dataset.filter;
            renderRecipes();
        });
    });

    if (data.hasResults && recipes.length) {
        renderRecipes();
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
})();
