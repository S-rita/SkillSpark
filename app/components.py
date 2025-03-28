import reflex as rx
from app.states import LoginState

def landing_bar():
    return rx.hstack(
        rx.image(src="/icon.png", width="50px"),
        rx.text("SkillSpark", font_size="2xl", font_weight="bold", color="gray"),
        rx.spacer(),
        rx.button("Start Study more", on_click=lambda: rx.redirect("/signup"), bg="yellow.400", border_radius="full"),
        rx.button("Login", on_click=lambda: rx.redirect("/login"), bg="yellow.400", border_radius="full"),
        spacing="4",
        padding="2",
        align="center",
        width="100%"
    )

def navbar(show_login_button=True):
    return rx.hstack(
        rx.image(src="/logo.png", width="50px"),
        rx.text("SkillSpark", font_size="2xl", font_weight="bold", color="gray"),
        rx.spacer(),
        rx.cond(
            show_login_button,
            rx.button("Login", on_click=rx.redirect("/login"), bg="yellow.400", border_radius="full"),
            rx.button("Logout", on_click=LoginState.logout, bg="gray.400", border_radius="full")
        ),
        padding="1",
        align="center",
        bg="white",
        shadow="md",
        width="100%"
    )

def info_section():
    return rx.box(
        rx.vstack(
            rx.text("The Best place blaaaa", font_size="lg", color="yellow.500"),
            rx.heading("Learn with....", font_size="5xl", font_weight="bold"),
            rx.text("The most educational place to blah blah.....", font_size="md", color="gray.600"),
            rx.button("Discover more", bg="gray", color="white", border_radius="md"),
            align="start",
            spacing="1"
        ),
        bg="yellow.200",
        width="100%",
        height="400px",
        padding="4",
        border_radius="lg"
    )
