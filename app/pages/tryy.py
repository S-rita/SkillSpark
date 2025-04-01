import reflex as rx

def circle_component(width: str, height: str, bg_color: str, icon: str) -> rx.Component:
    """Generate a circle with customizable size, background color, and icon."""
    return rx.box(
        bg=bg_color,  # Background color of the circle
        p="8px",  # Padding inside the circle (creates the circular shape)
        border_radius="50%",  # Makes it a circle
        color="black",  # Icon color (text color)
        width=width,  # Dynamically adjustable width
        height=height,  # Dynamically adjustable height
        align_items="center",  # Center icon inside the circle
        justify_content="center",  # Center the icon
    )

# Example usage of circle_component
def example_usage():
    return rx.vstack(
        circle_component("50px", "50px", "yellow", "🟡"),  # Yellow circle with emoji 🟡
        circle_component("70px", "70px", "blue", "🔵"),  # Blue circle with emoji 🔵
        circle_component("60px", "60px", "grey", "⚫"),  # Grey circle with emoji ⚫
    )

#🔘