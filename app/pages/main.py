# import reflex as rx
# from app.states import LoginState
# from app.components import navbar

# def main_page():
#     return rx.fragment(
#         rx.cond(
#             ~LoginState.is_logged_in,
#             rx.script("window.location.href = '/login'"),
#             rx.fragment()
#         ),
#         rx.vstack(
#             navbar(show_login_button=False),
#             rx.heading(f"Welcome to your dashboard, {LoginState.username}!", font_size="2xl", mt=6),
#             rx.text("This is your main dashboard where you can access all features.", mt=2),
            
#             rx.hstack(
#                 rx.box(
#                     rx.vstack(
#                         rx.heading("My Mindmaps", font_size="lg"),
#                         rx.text("View and create mindmaps"),
#                         rx.button("Create New", bg="yellow.400", mt=4)
#                     ),
#                     bg="white",
#                     p=4,
#                     border_radius="lg",
#                     shadow="md",
#                     width="250px"
#                 ),
#                 rx.box(
#                     rx.vstack(
#                         rx.heading("My Contests", font_size="lg"),
#                         rx.text("Participate in or create contests"),
#                         rx.button("Browse Contests", bg="yellow.400", mt=4)
#                     ),
#                     bg="white",
#                     p=4,
#                     border_radius="lg",
#                     shadow="md",
#                     width="250px"
#                 ),
#                 spacing="4",
#                 mt=6
#             ),
            
#             width="100%",
#             min_height="100vh",
#             bg="gray.100",
#             padding="4"
#         )
#     )
