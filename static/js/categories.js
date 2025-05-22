// Dropdown functionality
const dropdownButton = document.getElementById('dropdownButton')
const dropdownArrow = document.getElementById('dropdownArrow')
const dropdownMenu = document.getElementById('dropdownMenu')
const dropdownItems = document.querySelectorAll('.dropdown-item')
const goToCatalog = document.getElementById('goToCatalog')
const mobileCatalogButton = document.getElementById('mobileCatalogButton')

dropdownButton.addEventListener('click', () => {
	dropdownMenu.classList.toggle('open')
	dropdownArrow.classList.toggle('rotated')
})

dropdownItems.forEach((item) => {
	item.addEventListener('click', () => {
		const category = item.getAttribute('data-category')
		document.querySelector('.dropdown-item.active')?.classList.remove('active')
		item.classList.add('active')
		dropdownButton.textContent = category
		dropdownMenu.classList.remove('open')
		dropdownArrow.classList.remove('rotated')
		// Here you would typically filter products by category
	})
})

goToCatalog.addEventListener('click', () => {
	window.location.href = '/catalog'
})

mobileCatalogButton.addEventListener('click', () => {
	window.location.href = '/catalog'
})

// Sort dropdown functionality
const sortButton = document.getElementById('sortButton')
const sortArrow = document.querySelector('.sort-arrow')
const sortMenu = document.getElementById('sortMenu')
const sortItems = document.querySelectorAll('.sort-item')
const currentSort = document.getElementById('currentSort')

sortButton.addEventListener('click', () => {
	sortMenu.classList.toggle('open')
	sortArrow.classList.toggle('rotated')
})

sortItems.forEach((item) => {
	item.addEventListener('click', () => {
		const sortOption = item.getAttribute('data-sort')
		currentSort.textContent = sortOption
		sortMenu.classList.remove('open')
		sortArrow.classList.remove('rotated')
		// Here you would typically sort products
	})
})

// Pagination functionality
const prevPage = document.getElementById('prevPage')
const nextPage = document.getElementById('nextPage')
const pageButtons = document.querySelectorAll(
	'.page-button:not(#prevPage):not(#nextPage)'
)
let activePage = 1
const totalPages = 4

function updatePagination() {
	pageButtons.forEach((button, index) => {
		if (index + 1 === activePage) {
			button.classList.add('active')
		} else {
			button.classList.remove('active')
		}
	})

	prevPage.disabled = activePage === 1
	nextPage.disabled = activePage === totalPages
}

pageButtons.forEach((button, index) => {
	button.addEventListener('click', () => {
		activePage = index + 1
		updatePagination()
		// Here you would typically load the new page of products
	})
})

prevPage.addEventListener('click', () => {
	if (activePage > 1) {
		activePage--
		updatePagination()
		// Here you would typically load the new page of products
	}
})

nextPage.addEventListener('click', () => {
	if (activePage < totalPages) {
		activePage++
		updatePagination()
		// Here you would typically load the new page of products
	}
})

// Close dropdowns when clicking outside
document.addEventListener('click', (event) => {
	if (
		!dropdownButton.contains(event.target) &&
		!dropdownMenu.contains(event.target)
	) {
		dropdownMenu.classList.remove('open')
		dropdownArrow.classList.remove('rotated')
	}

	if (!sortButton.contains(event.target) && !sortMenu.contains(event.target)) {
		sortMenu.classList.remove('open')
		sortArrow.classList.remove('rotated')
	}
})

// Set active nav link based on current URL
const navLinks = document.querySelectorAll('.nav-link')
const currentPath = window.location.pathname

navLinks.forEach((link) => {
	if (link.getAttribute('href') === currentPath) {
		link.classList.add('active')
	}
})

// In a real app, you would fetch categories from an API
// This is just a mock implementation
async function fetchCategories() {
	// Simulate API call
	return new Promise((resolve) => {
		setTimeout(() => {
			resolve([
				{ id: 1, name: 'Все' },
				{ id: 2, name: 'Офис' },
				{ id: 3, name: 'Дом' },
				{ id: 4, name: 'Кухня' },
				{ id: 5, name: 'Детская' },
			])
		}, 500)
	})
}

// Load categories when page loads
document.addEventListener('DOMContentLoaded', async () => {
	const categories = await fetchCategories()
	const dropdownMenu = document.getElementById('dropdownMenu')

	// Clear existing items except the "Go to catalog" button
	dropdownMenu.innerHTML = ''

	// Add categories to dropdown
	categories.forEach((category) => {
		const item = document.createElement('li')
		item.className = 'dropdown-item'
		item.setAttribute('data-category', category.name)

		item.innerHTML = `
                    <div class="radio-indicator">
                        <div class="radio-dot"></div>
                    </div>
                    <span>${category.name}</span>
                `

		item.addEventListener('click', () => {
			document
				.querySelector('.dropdown-item.active')
				?.classList.remove('active')
			item.classList.add('active')
			dropdownButton.textContent = category.name
			dropdownMenu.classList.remove('open')
			dropdownArrow.classList.remove('rotated')
		})

		dropdownMenu.appendChild(item)
	})

	// Add "Go to catalog" button back
	const catalogButton = document.createElement('li')
	catalogButton.className = 'go-to-catalog'
	catalogButton.textContent = 'Перейти в каталог'
	catalogButton.addEventListener('click', () => {
		window.location.href = '/catalog'
	})
	dropdownMenu.appendChild(catalogButton)

	// Set first category as active by default
	if (categories.length > 0) {
		dropdownMenu.querySelector('.dropdown-item').classList.add('active')
		dropdownButton.textContent = categories[0].name
	}
})
