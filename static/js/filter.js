document.addEventListener('DOMContentLoaded', () => {
	const openFilterBtn = document.getElementById('openFilterBtn')
	const closeFilterBtn = document.getElementById('closeFilterBtn')
	const filterPanel = document.getElementById('filterPanel')
	const filterOverlay = document.getElementById('filterOverlay')
	const sortToggle = document.getElementById('sortToggle')
	const sortDropdown = document.getElementById('sortDropdown')
	const currentSort = document.getElementById('currentSort')
	const sortItems = document.querySelectorAll('.filtersidebar__dropdown-item')

	// Открытие/закрытие панели фильтров
	const toggleFilter = () => {
		const isOpen = filterPanel.classList.toggle('active')
		filterOverlay.classList.toggle('active', isOpen)
		document.body.style.overflow = isOpen ? 'hidden' : 'auto'
	}

	// Открытие/закрытие меню сортировки
	const toggleSort = () => {
		sortDropdown.classList.toggle('active')
	}

	// Выбор опции сортировки
	const selectSort = (option) => {
		currentSort.textContent = option
		sortDropdown.classList.remove('active')
	}

	// Обработчики для панели фильтров
	openFilterBtn.addEventListener('click', toggleFilter)
	closeFilterBtn.addEventListener('click', toggleFilter)
	filterOverlay.addEventListener('click', toggleFilter)

	// Обработчик для сортировки
	sortToggle.addEventListener('click', toggleSort)

	// Обработчики для выбора опции сортировки
	sortItems.forEach((item) => {
		item.addEventListener('click', () => {
			const sortOption = item.getAttribute('data-sort')
			selectSort(sortOption)
		})
	})
})
