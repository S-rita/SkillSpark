import reflex as rx
from app.pages.landing import landing_page
from app.pages.login import login_page
from app.pages.signup import signup_page
from app.pages.main import main_page
from app.pages.contest import contest_page
from app.pages.createContest import createcontest_page
from app.pages.library import library_page
from app.pages.InFolder import folder_page
from app.pages.InContest import inContest_page

app = rx.App()
app.add_page(landing_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")
app.add_page(main_page, route="/dashboard")
app.add_page(contest_page, route="/contest")
app.add_page(createcontest_page, route="/create_contest")
app.add_page(library_page, route="/library")
app.add_page(folder_page, route="/folder/")
app.add_page(inContest_page, route="/in_contest/")




