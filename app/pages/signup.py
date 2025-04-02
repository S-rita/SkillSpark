import reflex as rx
from app.states import SignupState

def signup_page():
    return rx.box(
        # Top-right login link
        rx.hstack(
            rx.spacer(),
            rx.text(
                "Already have an account?",
                color="#9EA4A9",
                font_size="sm",
                margin_top="20px",
            ),
            rx.link(
                "Login",
                href="/login",
                color="#F8CF79",  # yellow
                font_size="sm",
                margin_top="20px",
                margin_right="30px",
                font_weight="bold"
            ),
            padding="4"
        ),

        # Centered form
        rx.center(
            rx.vstack(
                rx.heading(
                    "Sign up",
                    color="#DBDFE0",
                    font_size="42px",
                    margin_bottom="20px",
                    margin_left="70px",
                    margin_top="10px"
                ),
                
                # Fixed space for signup error
                rx.box(
                    rx.cond(
                        SignupState.signup_error != "",
                        rx.text(SignupState.signup_error, color="red", font_size="12px", margin_bottom="-10px", margin_left="150px")
                    ),
                ),
                
                rx.input(
                    placeholder="Username",
                    type_="username",
                    value=SignupState.username,
                    on_change=SignupState.set_username,
                    bg="#393D45",
                    color="#DBDFE0",
                    border="none",
                    border_radius="10px",
                    padding="4",
                    width="300px",
                    height="50px",
                    margin_bottom="10px"
                ),
                rx.input(
                    placeholder="Email",
                    type_="email",
                    value=SignupState.email,
                    on_change=SignupState.set_email,
                    bg="#393D45",
                    color="#DBDFE0",
                    border="none",
                    border_radius="10px",
                    padding="4",
                    width="300px",
                    height="50px",
                    margin_bottom="10px"
                ),

                rx.input(
                    placeholder="Password",
                    type_="password",
                    value=SignupState.password,
                    on_change=SignupState.set_password,
                    bg="#393D45",
                    color="#DBDFE0",
                    border="none",
                    border_radius="10px",
                    padding="4",
                    width="300px",
                    height="50px",
                    margin_bottom="5px"
                ),

                rx.hstack(
                    rx.checkbox("Remember me", color_scheme="gray"),
                    width="300px",
                    margin_top="2",
                    margin_bottom="10px"
                ),

                rx.button(
                    "Sign Up",
                    on_click=SignupState.handle_signup,
                    bg="#FFD369",
                    color="#413B37",
                    font_size="20px",
                    width="300px",
                    height="50px",
                    padding_y="16px",
                    font_weight="bold",
                    border_radius="10px",
                    style={
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.2)"
                    }
                ),

                spacing="4"
            ),
            margin_top="40px"
        ),

        # Footer image
        rx.image(
            src="/signup_login_footer.png",
            position="absolute",
            bottom="0",
            left="0",
            width="100%",
            z_index="0"
        ),

        # Outer styling
        bg="#212932",
        height="100vh",
        width="100%",
        position="relative",
        overflow="hidden"
    )