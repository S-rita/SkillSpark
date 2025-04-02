import reflex as rx

def landing_page():
    return rx.box(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.hstack(
                            rx.hstack(
                                rx.image(src="/icon.png", height="60px", margin_right = "10px", margin_left = "25px"),
                                rx.text("Skill", font_weight="bold", style={"color": "#DDB300", "fontSize": "28px"}),
                                rx.text("Spark", font_weight="bold", style={"color": "black", "fontSize": "28px"}),
                                spacing="1",
                                align="center",
                                margin_left = "20px"
                            ),
                            rx.spacer(),
                            rx.hstack(
                                rx.button(
                                    "Start study now",
                                    bg="white",  # ✅ white background
                                    border="2px solid black",
                                    padding_x="20px",  # ⬅️ wider
                                    padding_y="20px",   # ⬅️ taller = thicker
                                    style={
                                        "color": "black",
                                        "borderRadius": "40px",  # ✅ custom round
                                        "fontSize": "16px"
                                    },
                                    on_click=rx.redirect("/signup")
                                ),
                                rx.button(
                                    "Login",
                                    bg="#FDCC00",
                                    padding_x="30px",
                                    padding_y="20px",
                                    style={
                                        "color": "black",
                                        "borderRadius": "40px",  # ✅ added this too
                                        "fontSize": "16px"
                                    },
                                    on_click=rx.redirect("/login")
                                ),
                                spacing="5",
                                margin_right = "30px" 
                                
                            ),
                            width="100%",
                            align="center",
                        ),
                        bg="white",
                        padding_x="6",
                        padding_y="15px",   # ✅ more vertical padding
                        height="90px",  # ✅ optional fixed height
                        margin_y="6",
                        width="80%",
                        style={
                            "borderTopLeftRadius": "60px",
                            "borderTopRightRadius": "0px",
                            "borderBottomLeftRadius": "60px",
                            "borderBottomRightRadius": "0px",
                            "boxShadow": "0 10px 25px rgba(0, 0, 0, 0.2)"
                        }
                    ),
                    justify="end",
                    width="100%"
                ),

                # Main content
                rx.hstack(
                    rx.box(
                        rx.text("The Best Place to Learn with", font_size="26px", color="white", font_weight="bold", margin_bottom="-20px", margin_top="70px"),
                        rx.text(
                            "Mind Maps",
                            font_size="72px",
                            color="black",
                            font_weight="bold",
                            margin_bottom="-10px",
                            style={"letterSpacing": "3px"}  # ✅ adjust spacing between letters
                        ),
                        rx.text(
                            "Visualize, connect, and remember with\ninteractivemind maps and practice tools.",
                            font_size="22px",
                            color="black",
                            margin_y="0",
                            margin_bottom="20px",
                            white_space="pre-line"  # ✅ required to render \n
                        ),

                    rx.button(
                        "Discover more",
                        bg="black",
                        color="white",
                        font_size="21px",
                        border_radius="200px",
                        padding_x="80px",   # ✅ wider horizontally
                        padding_y="25px",   # ✅ taller vertically
                        margin_top="10px",
                        on_click=rx.redirect("/signup")
                    ),
                        width="50%",
                        padding_x="10"
                    ),
                    rx.image(
                        src="/landing_icon.png",
                        width="35%",
                        margin_right="250px"  # ✅ Move it to the left
                    ),
                    width="100%",
                    justify="between",
                    padding="10",
                    margin_left="150px",  # ✅ shift everything to the right
                    margin_top="30px"
                ),

                spacing="6",
                width="100%",
            ),
            padding="6",
            background="center/cover url('/landing_bg.png')",
            height="100vh",
            width="100%",
        ),
        bg="white"
    )