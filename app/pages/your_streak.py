import reflex as rx
from datetime import date, timedelta, datetime
import calendar
from app.components import SidebarToggle, sidebar, sidebar_expand
from app.states import CalendarState


# Components
def calendar_component() -> rx.Component:
    return rx.vstack(

        # Month navigation row
        rx.hstack(
            rx.button(
                rx.icon("chevron-left"),
                on_click=CalendarState.prev_month,
                variant="ghost",
                is_disabled=~CalendarState.can_go_back,
                color="#848A95", # Grey color for  button
                _hover={
                    "background": "transparent",
                    "color": "#0F2552",
                    "transform": "scale(1.1)",
                    "transition": "all 0.2s ease-in-out"
                },
                _active={
                    "transform": "scale(0.95)"
                }
            ),
            rx.heading(
                rx.text(
                    CalendarState.month_name[:3] + " " + CalendarState.current_year.to_string(),
                    color="#0F2552",
                ),
                size="4",
                weight="medium",
            ),
            rx.button(
                rx.icon("chevron-right"),
                on_click=CalendarState.next_month,
                variant="ghost",
                is_disabled=~CalendarState.can_go_forward,  # Disable if can't go forward
                color="#848A95", # Grey color for  button
                _hover={
                    "background": "transparent",
                    "color": "#0F2552",
                    "transform": "scale(1.1)",
                    "transition": "all 0.2s ease-in-out"
                },
                _active={
                    "transform": "scale(0.95)"
                },

            ),
            spacing="3",
            align="center",
            width="100%",
            justify_content="space-between",
            padding="0 1em 0 1em",
        ),


        
        # Days of week header
        rx.hstack(
            *[
                rx.box(
                    day,
                    width="40px",
                    height="40px",
                    border_radius="50%",
                    display="flex",
                    justify_content="center",
                    align_items="center",
                    font_weight="medium",
                    color="black",
                    font_size="0.75em",
                )
                for day in ["S", "M", "T", "W", "T", "F", "S"]
            ],
            spacing="8",
        ),
        # Calendar grid
        rx.vstack(
            rx.foreach(
                range(6),
                lambda row: rx.hstack(
                    rx.foreach(
                        range(7),
                        lambda col: rx.cond(
                            ((row * 7 + col - CalendarState.first_day_offset) >= 0) & 
                            ((row * 7 + col - CalendarState.first_day_offset + 1) <= CalendarState.days_in_month),
                            rx.box(
                                rx.box(
                                    rx.cond(
                                        CalendarState.is_consecutive_day.contains(
                                            row * 7 + col - CalendarState.first_day_offset + 1
                                        ),
                                        rx.image(
                                            src="/highCostFire.png",
                                            width="20px", 
                                            height="20px",
                                            position="absolute",
                                            left="50%",
                                            top="50%",
                                            transform="translate(-50%, -50%)",
                                            z_index="2",
                                        ),
                                        rx.text(
                                            (row * 7 + col - CalendarState.first_day_offset + 1).to_string(),
                                            position="absolute",
                                            left="50%",
                                            top="50%",
                                            transform="translate(-50%, -50%)",
                                            z_index="1",
                                            color=rx.cond(
                                                CalendarState.dates_in_current_month.contains(
                                                    (row * 7 + col - CalendarState.first_day_offset + 1).to_string()
                                                ),
                                                "white",
                                                "black"
                                            ),
                                        )
                                    ),
                                    position="relative",
                                    width="40px",
                                    height="40px",
                                    border_radius="2em",
                                    border="1px solid #E2E8F0",
                                    bg=rx.cond(
                                        CalendarState.dates_in_current_month.contains(
                                            (row * 7 + col - CalendarState.first_day_offset + 1).to_string()
                                        ),
                                        "#FFCE51",
                                        "#EDEFF1"
                                    ),
                                ),
                                width="40px",
                                height="40px",
                                position="relative"
                            ),
                            rx.cond(
                                (row * 7 + col - CalendarState.first_day_offset) < 0,
                                rx.box(
                                    (CalendarState.prev_month_days + 
                                    (row * 7 + col - CalendarState.first_day_offset + 1)).to_string(),
                                    width="40px",
                                    height="40px",
                                    border_radius="2em",
                                    border="1px solid #E2E8F0",
                                    display="flex",
                                    justify_content="center",
                                    align_items="center",
                                    color="black",
                                    opacity="0.5"
                                ),
                                rx.box(
                                    ((row * 7 + col - CalendarState.first_day_offset + 1) - 
                                    CalendarState.days_in_month).to_string(),
                                    width="40px",
                                    height="40px",
                                    border_radius="2em",
                                    border="1px solid #E2E8F0",
                                    display="flex",
                                    justify_content="center",
                                    align_items="center",
                                    color="black",
                                    opacity="0.5"
                                )
                            )
                        )
                    ),
                    spacing="8"
                )
            ),
            spacing="4"
        ),
        spacing="6",
        padding="1em 3em 1em 3em",
        border_radius="2em",  # More curved borders
        bg="white",  # White background
        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",

    )


def layout(*children):
    return rx.hstack(
        rx.cond(
            SidebarToggle.expanded,
            sidebar_expand(),
            sidebar(),
        ),
        rx.box(
            *children,
            flex="1",  # Takes up remaining space
            height="100vh",
            overflow_y="auto",
        ),
        width="100%",
        spacing="0",
    )

def index_streak() -> rx.Component:
    return layout(
        rx.vstack(
            # Title with image
            rx.hstack(
                rx.box(
                    rx.image(
                        src=CalendarState.streak_image,  # Add your calendar icon image
                        width="100%",
                        height="100%",
                        object_fit="contain",
                        style={"& img": {"object_fit": "contain"}},

                    ),
                    width="auto",
                    height="15vh",
                ),
                rx.text(
                    (CalendarState.current_streak)[0],
                    color="black",
                    font_size="2.5em",
                    font_weight="bold",
                ),
                width="auto",
                padding="1",
                align="center",

            ),
            calendar_component(),
            spacing="2",
            align="center",
            justify_content="center",
            bg="#FFFBEA",
            width="100%",
            height="100%",
            padding="3em 4em 4em 4em",
        )
    )