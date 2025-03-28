import reflex as rx
from app.components import landing_bar, info_section

def landing_page() -> rx.Component:
    return rx.vstack(
        landing_bar(),
        info_section(),
        spacing="2",
        align="center",
        bg="gray.100",
        padding="2"
    )
