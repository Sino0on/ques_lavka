const footer = `
  <footer class="footer">
			<div class="footer-container">
				<img src="./assets/icons/logoWhite.svg" alt="Логотип" class="logo-footer" />

				<ul class="footer-links">
					<li><a href="/faq">Часто задаваемые вопросы</a></li>
					<li><a href="/catalog">Каталог</a></li>
					<li><a href="/profile">Личный кабинет</a></li>
					<li><a href="/cart">Корзина</a></li>
				</ul>

				<div class="footer-contacts">
					<h3>Контакты</h3>
					<a href="#" class="contact-item">
						<img src="./assets/icons/contactIcon.svg" alt="" />
						Телефон: 0 312 123456
					</a>
					<a href="#" class="contact-item">
						<img src="./assets/icons/location.svg" alt="" />
						Адрес: ул. пр. Чуй 132
					</a>
					<a class="contact-map" href="https://go.2gis.com/4401o6">
						https://go.2gis.com/4401o6
					</a>
					<div class="social-links">
						<a href="#"
							><img src="./assets/icons/instagramIcon.svg" alt="Instagram"
						/></a>
						<a href="#"
							><img src="./assets/icons/tiktokIcon.svg" alt="TikTok"
						/></a>
					</div>
				</div>
			</div>
		</footer>
		<footer class="mobile-footer">
        <div class="container">
            <div class="footer-nav">
                <a href="/" class="nav-link">
                    <img src="./assets/icons/homeIcon.svg" alt="Home" class="nav-icon">
                    <img src="./assets/icons/homeIconActive.svg" alt="Home Active" class="nav-icon-active">
                </a>
                <a href="/favorites" class="nav-link">
                    <img src="./assets/icons/favoriteIcon.svg" alt="Favorites" class="nav-icon">
                    <img src="./assets/icons/favoriteIconActive.svg" alt="Favorites Active" class="nav-icon-active">
                </a>
                <a href="/shop" class="nav-link">
                    <img src="./assets/icons/shopIcon.svg" alt="Shop" class="nav-icon">
                    <img src="./assets/icons/shopIconActive.svg" alt="Shop Active" class="nav-icon-active">
                </a>
                <a href="/contacts" class="nav-link">
                    <img src="./assets/icons/accountIcon.svg" alt="Contacts" class="nav-icon">
                    <img src="./assets/icons/accountIconActive.svg" alt="Contacts Active" class="nav-icon-active">
                </a>
            </div>
        </div>
    </footer>
`

document.getElementById('footer').innerHTML = footer
