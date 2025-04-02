import reflex as rx
from app.components import (sidebar, sidebar_expand, SidebarToggle)

def profile_card():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.box(
                        border_radius="100px",
                        width="150px",
                        height="150px",
                        margin_top="80px",
                        margin_left="100px",
                        bg="#D9D9D9"
                    ),
                    rx.icon(
                        "pencil",
                        cursor="pointer",
                        position="absolute",
                        bottom="0px",
                        right="0px",
                        bg="white",
                        width="40px",
                        height="40px",
                        border_radius="40px",
                        padding="3px",
                        box_shadow="lg",
                    ),
                    position="relative", 
                ),
                rx.vstack(
                    rx.heading(
                        "Bew wiiiiiii", 
                        font_size="2em",
                        margin_top="120px",
                        margin_left="1em"
                    ),
                    rx.text(
                        "yourmailaddress@gmail.com", 
                        font_size="1em",
                        margin_left="2em",
                        color="gray"
                    ),
                ),
            ),
            rx.divider(
                height="3px",
                width="90%",
                bg="#D9D9D9",
                margin_x="100px"
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Username", 
                        font_weight="bold",
                        font_size="1.5em",
                        margin_left="100px",
                    ),
                    rx.spacer(),
                    rx.text(
                        "Bew wiiiiiii",
                        margin_right="1em",
                        font_size="1.25em",
                        text_align="right"
                    ),
                    rx.icon(
                        "pencil", 
                        cursor="pointer",
                        text_align="right",
                        margin_right="120px"
                    ),
                    width="100%"
                ),
                rx.divider(
                    height="3px",
                    width="90%",
                    bg="#D9D9D9",
                    margin_x="100px",
                    margin_y="5px"
                ),
                rx.hstack(
                    rx.text(
                        "Email", 
                        font_weight="bold",
                        font_size="1.5em",
                        margin_left="100px",
                    ),
                    rx.spacer(),
                    rx.text(
                        "yourmailaddress@gmail.com", 
                        color="blue",
                        margin_right="150px",
                        font_size="1.25em",
                        text_align="right"
                    ),
                    width="100%"
                ),
                rx.divider(
                    height="3px",
                    width="90%",
                    bg="#D9D9D9",
                    margin_x="100px",
                    margin_y="5px"
                ),
                rx.hstack(
                    rx.text(
                        "Password", 
                        font_weight="bold",
                        font_size="1.5em",
                        margin_left="100px",
                    ),
                    rx.spacer(),
                    rx.text(
                        "**********",
                        margin_right="150px",
                        text_align="right",
                        font_size="1.25em"
                    ),
                    width="100%"
                ),
                align_items="flex_start",
                spacing="2",
                width="100%"
            ),
            rx.hstack(
                rx.spacer(),
                rx.button(
                    "See Achievement", 
                    bg="#FEE381", 
                    color="#000000",
                    font_size="1em",
                    padding="4",
                    width="230px",
                    height="50px",
                    border_radius="10px"
                ),
                rx.button(
                    "Change password", 
                    bg="#FEE381", 
                    color="#000000",
                    font_size="1em",
                    padding="4",
                    width="230px",
                    height="50px",
                    border_radius="10px"
                ),
                spacing="4",
                width="100%"
            ),
            align_items="flex_start",
            spacing="6",
            bg="#FFFBEA",
            box_shadow="md",
            width="90%",
        ),
        display="flex",
        justify_content="center",
        width="100%"
    )

def user_page():
    return rx.hstack(
        rx.cond(SidebarToggle.expanded, sidebar_expand(), sidebar()),
        rx.box(
            profile_card(),
            align="start",
            width="100%",
            height="100vh"
        ),
        bg="#FFFBEA"
    )
