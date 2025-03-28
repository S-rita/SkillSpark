import reflex as rx
from app.pages.landing import landing_page
from app.pages.login import login_page
from app.pages.signup import signup_page
from app.pages.main import main_page

app = rx.App()
app.add_page(landing_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")
app.add_page(main_page, route="/dashboard")
