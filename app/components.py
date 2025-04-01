import reflex as rx

# def landing_bar():
#     return rx.hstack(
#         rx.image(src="/icon.png", width="50px"),
#         rx.text("SkillSpark", font_size="2xl", font_weight="bold", color="gray"),
#         rx.spacer(),
#         rx.button("Start Study more", on_click=lambda: rx.redirect("/signup"), bg="yellow.400", border_radius="full"),
#         rx.button("Login", on_click=lambda: rx.redirect("/login"), bg="yellow.400", border_radius="full"),
#         spacing="4",
#         padding="2",
#         align="center",
#         width="100%"
#     )


# def info_section():
#     return rx.box(
#         rx.vstack(
#             rx.text("The Best place blaaaa", font_size="lg", color="yellow.500"),
#             rx.heading("Learn with....", font_size="5xl", font_weight="bold"),
#             rx.text("The most educational place to blah blah.....", font_size="md", color="gray.600"),
#             rx.button("Discover more", bg="gray", color="white", border_radius="md"),
#             align="start",
#             spacing="1"
#         ),
#         bg="yellow.200",
#         width="100%",
#         height="400px",
#         padding="4",
#         border_radius="lg"
#     )


class SidebarToggle(rx.State):
    expanded: bool = False
    
    def toggle_sidebar(self):
        self.expanded = not self.expanded

def sidebar():
    return rx.vstack(
        rx.text(
            ">>",
            color="#FEDC45",
            font_weight="bold",
            font_size="2em",
            cursor="pointer",
            on_click=SidebarToggle.toggle_sidebar
        ),
        rx.link(
            rx.icon(
                "home",
                font_size="40px", 
                color="white",
                cursor="pointer"
            ),
            href="/",  # This will link to your home/index page
        ),
        
        rx.icon(
            "folder-closed", 
            font_size="40px",
            color="white",
            cursor="pointer"
        ),
        rx.link(
            rx.icon(
                "calendar", 
                font_size="40px",
                color="white",
                cursor="pointer"
            ),
            href="/calendar",  # This will link to your calendar page
        ),
        
        rx.divider(
            bg="white",
            width="85%",
            height="3px",
            cursor="pointer"
        ),
        rx.icon(
            "git-fork", 
            font_size="40px",
            color="white",
            cursor="pointer"
        ), 
        rx.icon(
            "medal", 
            font_size="40px",
            color="white",
            cursor="pointer"
        ),
        spacing="6",
        align_items="center",
        bg="#222",
        padding_y="30px",
        border_radius="md",
        width=rx.cond(SidebarToggle.expanded, "300px", "100px"),
        height="100vh",
        transition="width 0.3s ease-in-out"
    )

def sidebar_expand():
    return rx.vstack(
        rx.hstack(
            rx.text(
                "SkillSpark",
                color="#FEDC45",
                font_weight="bold",
                font_size="1em",
            ),
            rx.text(
                "<<",
                color="#FEDC45",
                font_weight="bold",
                font_size="1em",
                cursor="pointer",
                on_click=SidebarToggle.toggle_sidebar
            ),
        ),
        rx.link(
            rx.hstack(
                rx.icon(
                    "home", 
                    font_size="40px",
                    color="white",
                    cursor="pointer"
                ),
                rx.text(
                    "Home",
                    color="white",
                    font_weight="bold",
                    font_size="1em",
                    cursor="pointer",
                ),
            ),
            href="/",  # This will link to your home/index page
        ),
        
        rx.hstack(
            rx.icon(
                "folder-closed", 
                font_size="40px",
                color="white",
                cursor="pointer"
            ),
            rx.text(
                "Your Library",
                color="white",
                font_weight="bold",
                font_size="1em",
                cursor="pointer",
            ),
        ),
        rx.link(
            rx.hstack(
                rx.icon(
                    "calendar", 
                    font_size="40px",
                    color="white",
                    cursor="pointer"
                ),
                rx.text(
                    "Your Streaks",
                    color="white",
                    font_weight="bold",
                    font_size="1em",
                    cursor="pointer",
                ),
            ),
            href="/calendar",
        ),
        
        rx.divider(
            bg="white",
            width="85%",
            height="3px",
            cursor="pointer"
        ),
        rx.hstack(
            rx.icon(
                "git-fork", 
                font_size="40px",
                color="white",
                cursor="pointer"
            ),
            rx.text(
                "MindMaps",
                color="white",
                font_weight="bold",
                font_size="1em",
                cursor="pointer",
            ),
        ),
        rx.hstack(
            rx.icon(
                "medal", 
                font_size="40px",
                color="white",
                cursor="pointer"
            ),
            rx.text(
                "Contests",
                color="white",
                font_weight="bold",
                font_size="1em",
                cursor="pointer",
            ),
        ),
        spacing="6",
        align_items="center",
        bg="#222",
        padding_y="30px",
        border_radius="md",
        width=rx.cond(SidebarToggle.expanded, "300px", "100px"),
        height="100vh",
        transition="width 0.3s ease-in-out"
    )
