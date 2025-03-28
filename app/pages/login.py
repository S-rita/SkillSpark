import reflex as rx
from app.states import LoginState

def login_page():
    return rx.center(
        rx.vstack(
            rx.heading("Login to SkillSpark", font_size="2xl", mb=6),
            
            rx.cond(
                LoginState.login_error != "",
                rx.box(
                    rx.text(LoginState.login_error, color="white"),
                    bg="red.500",
                    width="100%",
                    p=3,
                    border_radius="md",
                    mb=4
                )
            ),
            
            rx.input(
                placeholder="Username",
                value=LoginState.username,
                on_change=LoginState.set_username,
                mb=4,
                width="100%"
            ),
            rx.input(
                placeholder="Password",
                type_="password",
                value=LoginState.password,
                on_change=LoginState.set_password,
                mb=6,
                width="100%"
            ),
            rx.button(
                "Login",
                on_click=LoginState.handle_login,
                width="100%",
                bg="yellow.400",
                color="white"
            ),
            rx.link(
                "Don't have an account? Sign up",
                href="/signup",
                color="blue.500",
                mt=4
            ),
            width="300px",
            bg="white",
            padding="6",
            border_radius="lg",
            shadow="xl"
        ),
        width="100%",
        height="100vh",
        bg="gray.100"
    )
