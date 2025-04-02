import reflex as rx
from app.states import LoginState

class SidebarToggle(rx.State):
    expanded: bool = False
    
    def toggle_sidebar(self):
        self.expanded = not self.expanded

def sidebar_view():
    return rx.cond(
        SidebarToggle.expanded,
        sidebar_expand(),
        sidebar()
    )

def sidebar():
    def icon_box(icon_src, href="/main", width="40px"): # go to
        return rx.link(
            rx.box(
            rx.image(src=icon_src, width=width, cursor="pointer"),
            border_radius="15px",
            padding="12px",
            _hover={"bg": "#3a3a3a"},
            transition="all 0.2s"
            ),
            href=href
        )

    return rx.vstack(
        rx.box(
            rx.image(
                src="/arrow_right.svg",
                width="36px",
                cursor="pointer",
                on_click=SidebarToggle.toggle_sidebar
            ),
            border_radius="md",
            padding="8px",
            transition="all 0.2s"
        ),
        rx.box(
            rx.image(src="/homepage_icon.svg", width="50px", cursor="pointer"), 
            border_radius="15px",
            padding="8px",
            _hover={"bg": "#3a3a3a"},
            transition="all 0.2s"
        ),
        icon_box("/library_icon.svg", "/library"),
        icon_box("/streak_icon.svg", "/your_streak"),
        rx.divider(bg="white", width="85%", height="3px"),
        rx.link(
        rx.box(
            rx.image(src="/sb_mindmap_icon.svg", width="40px", height="45px", cursor="pointer"),
            border_radius="15px",
            padding="10px",
            _hover={"bg": "#3a3a3a"},
            transition="all 0.2s",     
        ),
        href="/createmindmap" 
        ),
        icon_box("/contest_icon.svg", "/contest"),
        spacing="7",
        align_items="center",
        bg="#282629",
        padding_y="30px",
        border_radius="md",
        width=rx.cond(SidebarToggle.expanded, "300px", "100px"),
        height="100vh",
        transition="width 0.3s ease-in-out"
    )
    
def sidebar_expand():
    return rx.vstack(
        # Header with logo and toggle
        rx.hstack(
            rx.image(src="/logo_w_name.svg", width="180px", margin_left="10px"),
            rx.image(
                src="/arrow_left.svg",
                width="36px",
                cursor="pointer",
                on_click=SidebarToggle.toggle_sidebar
            ),
            align_items="center",
            width="100%",
            padding_x="16px",
            margin_bottom="-10px"
        ),

        # Individual nav rows
        rx.link(
            rx.box(
                rx.hstack(
                    rx.image(src="/homepage_icon.svg", width="50px", cursor="pointer"),
                    rx.text("Home", color="white", font_size="1.6em", cursor="pointer", margin_left="5px"),
                    gap="12px",
                    align_items="center",
                    width="100%",
                    padding_x="20px"
                ),
                padding_y="6px",
                _hover={"bg": "#3a3a3a","margin_left":"20px"},
                transition="all 0.2s",
                border_radius="15px"
            ),
            href="/main"
        ),

        rx.link(
            rx.box(
                rx.hstack(
                    rx.image(src="/library_icon.svg", width="40px", cursor="pointer"),
                    rx.text("Your Library", color="white", font_size="1.6em", cursor="pointer", margin_left="5px"),
                    gap="15px",
                    align_items="center",
                    width="100%",
                    padding_x="25px",
                ),
                padding_y="10px",
                _hover={"bg": "#3a3a3a","margin_left":"20px"},
                transition="all 0.2s",
                border_radius="15px"
            ),
            href="/library"
        ),
        
        rx.link(
            rx.box(
                rx.hstack(
                    rx.image(src="/streak_icon.svg", width="40px", cursor="pointer"),
                    rx.text("Your Streaks", color="white", font_size="1.6em", cursor="pointer", margin_left="5px"),
                    gap="12px",
                    align_items="center",
                    width="100%",
                    padding_x="25px"
                ),
                padding_y="10px",
                _hover={"bg": "#3a3a3a","margin_left":"20px"},
                transition="all 0.2s",
                border_radius="15px"
            ),
            href="/your_streak"
        ),

        rx.divider(bg="white", width="85%", height="3px", margin_left="15px"),

        rx.link(
            rx.box(
                rx.hstack(
                    rx.image(src="/sb_mindmap_icon.svg", width="40px", cursor="pointer"),
                    rx.text("MindMaps", color="white", font_size="1.6em", cursor="pointer", margin_left="5px"),
                    gap="12px",
                    align_items="center",
                    width="100%",
                    padding_x="25px"
                ),
                padding_y="10px",
                _hover={"bg": "#3a3a3a","margin_left":"20px"},
                transition="all 0.2s",
                border_radius="15px"
            ),
            href="/cretemindmap"
        ),

        rx.link(
            rx.box(
                rx.hstack(
                    rx.image(src="/contest_icon.svg", width="40px", cursor="pointer"),
                    rx.text("Contests", color="white", font_size="1.6em", cursor="pointer", margin_left="5px"),
                    gap="12px",
                    align_items="center",
                    width="100%",
                    padding_x="25px"
                ),
                padding_y="10px",
                _hover={"bg": "#3a3a3a","margin_left":"20px"},
                transition="all 0.2s",
                border_radius="15px"
            ),
            href = "/contest"
        ),
        
        spacing="7",
        align_items="start",
        bg="#282629",
        padding_y="30px",
        border_radius="md",
        width=rx.cond(SidebarToggle.expanded, "300px", "100px"),
        height="100vh",
        transition="width 0.3s ease-in-out"
    )