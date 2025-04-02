import reflex as rx
from app.states import LoginState

def login_page():
    return rx.box(
        # Top-right signup link
        rx.hstack(
            rx.spacer(),
            rx.text(
                "New User?",
                color="#9EA4A9",
                font_size="sm",
                margin_top="20px",
            ),
            rx.link(
                "Signup",
                href="/signup",
                color="#F8CF79",
                font_size="sm",
                margin_top="20px",
                margin_right="30px",
            ),
            padding="4"
        ),

        # Centered login form
        rx.center(
            rx.vstack(
                rx.heading("Log in", color="#DBDFE0", font_size="42px", margin_bottom="15px", margin_left="90px", margin_top="10px"),

                # Fixed space for error message (below inputs)
                rx.box(
                    rx.cond(
                        LoginState.login_error != "",
                        rx.text(LoginState.login_error, color="red", font_size="12px", margin_bottom="-10px", margin_left="120px"),
                    ),
                ),
                
                rx.input(
                    placeholder="Username",
                    value=LoginState.username,
                    on_change=LoginState.set_username,
                    bg="#393D45",
                    color="#DBDFE0",
                    border="none",
                    border_radius="10px",
                    padding="4",
                    width="300px",
                    height="50px",
                    margin_bottom="20px"
                ),

                rx.input(
                    placeholder="Password",
                    type_="password",
                    value=LoginState.password,
                    on_change=LoginState.set_password,
                    bg="#393D45",
                    color="#DBDFE0",
                    border="none",
                    border_radius="10px",
                    padding="4",
                    width="300px",
                    height="50px",
                    margin_bottom="10px"
                ),

                # Remember me + Forgot password
                rx.hstack(
                    rx.checkbox("Remember me", color_scheme="gray", font_size="12px"),
                    rx.spacer(),
                    rx.link("Forgot password?", href="#", color="#FFD369", font_size="14px"),
                    width="300px",
                    margin_top="2",
                    margin_bottom="15px"
                ),

                # Login button
                rx.button(
                    "Login",
                    on_click=LoginState.handle_login,
                    bg="#FFD369",
                    color="#413B37",
                    font_size="20px",
                    width="300px",
                    height="50px",
                    padding_y="16px",
                    font_weight="bold",
                    border_radius="10px",  # ✅ rounder button
                    style={
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.2)"
                    }
                ),

                spacing="4"
            ),
            margin_top="40px"
        ),
        # Decorative footer circles
        rx.image(
            src="/signup_login_footer.png",
            position="absolute",
            bottom="0px",
            left="0",
            width="100%",
            z_index="0"
        ),

        bg="#212932",
        height="100vh",
        width="100%",
        overflow="hidden",  # ✅ add this line here

    )