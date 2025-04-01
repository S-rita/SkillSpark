# import reflex as rx
# from app.states import SignupState

# def signup_page():
#     return rx.center(
#         rx.vstack(
#             rx.heading("Signup to SkillSpark", font_size="2xl", mb=6),
            
#             rx.cond(
#                 SignupState.signup_error != "",
#                 rx.box(
#                     rx.text(SignupState.signup_error, color="white"),
#                     bg="red.500",
#                     width="100%",
#                     p=3,
#                     border_radius="md",
#                     mb=4
#                 )
#             ),
            
#             rx.input(
#                 placeholder="Username",
#                 value=SignupState.username,
#                 on_change=SignupState.set_username,
#                 mb=4,
#                 width="100%"
#             ),
#             rx.input(
#                 placeholder="Password",
#                 type_="password",
#                 value=SignupState.password,
#                 on_change=SignupState.set_password,
#                 mb=6,
#                 width="100%"
#             ),
#             rx.input(
#                 placeholder="Email",
#                 type_="email",
#                 value=SignupState.email,
#                 on_change=SignupState.set_email,
#                 mb=6,
#                 width="100%"
#             ),
#             rx.button(
#                 "Sign Up",
#                 on_click=SignupState.handle_signup,
#                 width="100%",
#                 bg="yellow.400",
#                 color="white"
#             ),
#             rx.link(
#                 "Already have an account? Login",
#                 href="/login",
#                 color="blue.500",
#                 mt=4
#             ),
#             width="300px",
#             bg="white",
#             padding="6",
#             border_radius="lg",
#             shadow="xl"
#         ),
#         width="100%",
#         height="100vh",
#         bg="gray.100"
#     )
