import reflex as rx
from app.pages.landing import landing_page
from app.pages.login import login_page
from app.pages.signup import signup_page
from app.pages.user import user_page
from app.pages.createmindmap import createmindmap_page
from app.pages.mindmap import mindmap_page
from app.pages.fillinmindmap import fillinmindmap_page
from app.pages.choicemindmap import choicemindmap_page
from app.pages.contest import contest_page
from app.pages.createContest import createcontest_page
from app.pages.library import library_page
from app.pages.InFolder import folder_page
from app.pages.InContest import inContest_page
from app.pages.Main_page import index_main as Entire_page_main
from app.pages.Achievements import Achievements_page
from app.pages.searching import searching_page
from app.pages.your_streak import index_streak as your_streak_page

app = rx.App()
app.add_page(landing_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")
app.add_page(Entire_page_main, route="/main")
app.add_page(user_page, route="/user")
app.add_page(createmindmap_page, route="/createmindmap")
app.add_page(mindmap_page, route="/mindmap")
app.add_page(fillinmindmap_page, route="/fillin")
app.add_page(choicemindmap_page, route="/choice")
app.add_page(contest_page, route="/contest")
app.add_page(createcontest_page, route="/create_contest")
app.add_page(library_page, route="/library")
app.add_page(folder_page, route="/folder/")
app.add_page(inContest_page, route="/in_contest/")
app.add_page(your_streak_page, route="/calendar")
app.add_page(Achievements_page, route="/egg")
app.add_page(searching_page, route="/search")