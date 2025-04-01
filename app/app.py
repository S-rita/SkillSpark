import reflex as rx
from app.pages.landing import landing_page
from app.pages.login import login_page
from app.pages.signup import signup_page
from app.pages.main import main_page
from app.pages.Main_page import index_main as Entire_page_main
from app.pages.Achievements import Achievements_page
from app.pages.searching import searching_page
from app.pages.your_streak import index_streak as your_streak_page


app = rx.App()
# app.add_page(landing_page, route="/")
# app.add_page(login_page, route="/login")
# app.add_page(signup_page, route="/signup")
# app.add_page(main_page, route="/dashboard")
app.add_page(your_streak_page, route="/calendar")
app.add_page(Entire_page_main, route="/")
app.add_page(Achievements_page, route="/egg")
app.add_page(searching_page, route="/search")