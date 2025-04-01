# import reflex as rx

# class Main_Pages_state(rx.State):
#     # Add state vars to store data
#     mindmaps: list[dict] = []  
#     contests: list[dict] = []
#     search_query: str = ""
    
#     async def get_mindmaps(self):
#         # Make API call to your FastAPI endpoint
#         response = await rx.utils.http.httpx.get("http://localhost:8000/mindmaps/")
#         self.mindmaps = response.json()
    
#     async def get_contests(self):
#         response = await rx.utils.http.httpx.get("http://localhost:8000/contests/")
#         self.contests = response.json()
        
#     def handle_search(self, value: str):
#         self.search_query = value
        
#     @rx.event
#     async def execute_search(self):
#         if not self.search_query:
#             return
            
#         # Make API call with search query
#         response = await rx.utils.http.httpx.get(
#             f"http://localhost:8000/search?q={self.search_query}"
#         )
#         search_results = response.json()





# def search_area() -> rx.Component:
#     return rx.hstack(
#         rx.input(
#             rx.input.slot(
#                 rx.image(
#                     src="/searchArea.png",
#                     width="100%",
#                     height="90%",
#                     fit='cover',
#                     padding="0.5em",
#                 ),
#             ),
#             placeholder="Search public mindmaps and contests",
#             width="70vw",
#             height="100px",
#             on_change=State.handle_search,
#             bg='white',
#             style={"& input::placeholder": {"color": "grey", "opacity": "0.25"}},
#             border_radius="0.5em",
#             padding_left="1em",
#             color="grey",
#             font_size="2em",
#             box_shadow="0px 4px 12px rgba(0, 0, 0, 0.25)",
#         ),
#         rx.button(
#             "Search",
#             color="black",
#             font_size="2em",
#             font_weight="bold",
#             bg="#FFDA5D",  # Button background color
#             border_radius="8px",  # Optional: Rounded corners
#             padding="10px",
#             on_click=State.execute_search,  # Action on click
#             width="8em",
#             height="60px",
#             overflow="hidden",
#             box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#             _hover={
#                 "transform": "scale(1.05)",
#                 "transition": "transform 0.2s ease-in-out"
#             }

#         ),
#         spacing="6",
#         align="center", # Aligns items vertically in the middle
#         justify_content="space-between",  # Push items to opposite ends
#         width="100%",  # Make hstack take full width
#         padding="1em", # Add padding to prevent edge touching



#     )

# def Top_Area() -> rx.Component:
#     return rx.vstack(
        
#         rx.hstack(
#             rx.vstack(
        
#                 rx.text("Hello Bewieee!!🤫", font_size="6em", font_weight="bold", color="black"),
#                 rx.text("Welcome back, let's start practice today", font_size="1.5em", color='#919191'),
#                 spacing="0",
#             ),
#             rx.hstack(
#                 rx.button(
#                     rx.image(
#                         src="/AddM.png",
#                         width="100%",
#                         height="100%",
#                         fit='cover',
#                     ), # Ensures the image fits the button,
#                     bg="#FDCC00",  # Button background color
#                     border_radius="8px",  # Optional: Rounded corners
#                     padding="10px",
#                     on_click=State.execute_search,  # Action on click
#                     width="6em",
#                     height="6em",
#                     overflow="hidden",
#                     box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                     _hover={
#                         "transform": "scale(1.05)",
#                         "transition": "transform 0.2s ease-in-out"
#                     }
#                 ),
                
#                 rx.avatar(
#                     src="/static/logo.png",
#                     size="9",  # Controls size from "1" to "9"
#                     fallback="PROFILE",  # Fallback text if image fails to load
#                     radius="full",  # Makes it circular
#                     variant="solid",  # Gives a softer appearance
#                     color_scheme="gray",  # Makes it grayscale
#                     opacity="0.5",
#                     high_contrast=False,
#                 ),
#                 align="center", # Aligns items vertically in the middle
#                 spacing="7",    # Adds space between button and avatar
#             ),
            
            
#             spacing="2",
#             align_items="center",
#             width="100%",  # Make hstack take full width
#             justify_content="space-between",  # Push items to opposite ends
#         ),
#         rx.hstack(
#             search_area(),
#             spacing="4",
#             margin_y="2em",

#         ),
#         padding="4em 4em 0 4em",  # Add padding inside the background
#         width="100vw",  # Full width of the viewport
#     )


# def Middle_area() -> rx.Component:
#     return rx.vstack(
#         rx.text("Recents", font_size="4em", font_weight="bold", color="black", margin_left="1.5em"),
#         # First Row
#         rx.hstack(
#             # Column 1
#             rx.box(
#                 rx.hstack(
#                 rx.box(
#                     rx.image(
#                         src="/mindmap.png",
#                         width="100%",
#                         height="100%",
#                         object_fit="cover"
#                     ),
#                     bg="#FFDA5D",
#                     border_radius="1.5em", 
#                     padding="1em",
#                     width="120px",
#                     height="120px",
#                     overflow="hidden",
#                     box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                     _hover={
#                         "transform": "scale(1.05)",
#                         "transition": "transform 0.2s ease-in-out"
#                     }
#                 ),
#                 rx.vstack(
#                     rx.text("Chinese Sentences", font_size="2em", font_weight="bold", color="black"),
#                     rx.text(f"Mindmap set    ●    27 terms    ●    by Sarita", font_size="1em", color="#969696", margin_left="1em", white_space="pre"),
#                     spacing="0",  # Reduce space between lines
#                     align_items="start",  # Align items to the start
#                 ),
                
#                 align="center",
#                 spacing="6",
#                 margin_left="6em",
#                 ),
#                 width="50%",  # Set width for the box
#             ),
            
#             # Column 2
#             rx.box(
#                 rx.hstack(
#                 rx.box(
#                     rx.image(
#                         src="/mindmap.png",
#                         width="100%",
#                         height="100%",
#                         object_fit="cover"
#                     ),
#                     bg="#FFDA5D",
#                     border_radius="1.5em",
#                     padding="1em",
#                     width="120px",
#                     height="120px",
#                     overflow="hidden", 
#                     box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                     _hover={
#                         "transform": "scale(1.05)",
#                         "transition": "transform 0.2s ease-in-out"
#                     }
#                 ),
#                 rx.vstack(
#                     rx.text("German Sentences", font_size="2em", font_weight="bold", color="black"),
#                     rx.text(f"Mindmap set    ●    27 terms    ●    by Sarita", font_size="1em", color="#969696", margin_left="1em", white_space="pre"),
#                     spacing="0",  # Reduce space between lines
#                     align_items="start",  # Align items to the start
#                 ),

#                 align="center",
#                 spacing="6",
#                 ),
#                 width="50%",  # Set width for the box
#             ),
            
#             spacing="6",
#             width="100%",
#         ),
#         # Second Row
#         rx.hstack(
#             # Column 1
#             rx.box(
#                 rx.hstack(
#                     rx.box(
#                         rx.image(
#                             src="/mindmap.png",
#                             width="100%",
#                             height="100%",
#                             object_fit="cover"
#                         ),
#                         bg="#FFDA5D",
#                         border_radius="1.5em",
#                         padding="1em",
#                         width="120px",
#                         height="120px",
#                         overflow="hidden",
#                         box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                         _hover={
#                             "transform": "scale(1.05)",
#                             "transition": "transform 0.2s ease-in-out"
#                         }
#                     ),
#                     rx.vstack(
#                         rx.text("Python Programming", font_size="2em", font_weight="bold", color="black"),
#                         rx.text(f"Mindmap set    ●    109 terms    ●    by Sarita", font_size="1em", color="#969696", margin_left="1em", white_space="pre"),
#                         spacing="0",  # Reduce space between lines
#                         align_items="start",  # Align items to the start
#                     ),

#                     align="center",
#                     spacing="6",
#                     margin_left="6em",
#                 ),
#                 width="50%",  # Set width for the box
#             ),
            
#             # Column 2
#             rx.box(
#                 rx.hstack(
#                     rx.box(
#                         rx.image(
#                             src="/mindmap.png",
#                             width="100%",
#                             height="100%",
#                             object_fit="cover"
#                         ),
#                         bg="#FFDA5D",
#                         border_radius="1.5em",
#                         padding="1em", 
#                         width="120px",
#                         height="120px",
#                         overflow="hidden",
#                         box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                         _hover={
#                             "transform": "scale(1.05)",
#                             "transition": "transform 0.2s ease-in-out"
#                         }
#                     ),
#                     rx.vstack(
#                         rx.text("I Love AI", font_size="2em", font_weight="bold", color="black"),
#                         rx.text(f"Mindmap set    ●    12 terms    ●    by Sarita", font_size="1em", color="#969696", margin_left="1em", white_space="pre"),
#                         spacing="0",  # Reduce space between lines
#                         align_items="start",  # Align items to the start
#                     ),

#                     align="center",
#                     spacing="6",
#                 ),
#                 width="50%",  # Set width for the box
#             ),
            
#             spacing="6",
#             width="100%",
#         ),
#         spacing="4",
#         padding="0 4em 4em 4em",  # Add padding inside the background
#         width="100%",  # Make hstack take full width
#     )

# def Bottom_area() -> rx.Component:
#     return rx.vstack(
#         rx.text("Favorites", font_size="4em", font_weight="bold", color="black", margin_left="1.5em"),
#         # First Row
#         rx.hstack(
#             #Column1
#             rx.hstack(
#                 rx.box(
#                     rx.vstack(
#                         rx.text("Python is the Best", font_size="1.5em", font_weight="bold", color="black"),
#                         rx.box(
#                             "27 terms",
#                             font_size="0.75em",
#                             color="black",
#                             background_color="#FFF5D0",
#                             border_radius="1.5em",
#                             padding="1px 20px 1px 20px",
#                             width="fit-content",
#                             height="fit-content",
#                             margin_bottom="2em",
#                         ),
#                         rx.hstack(
#                             rx.box(
#                                 rx.avatar(
#                                     src="/static/logo.png",
#                                     size="3",
#                                     radius="full",
#                                     fallback="",
#                                     variant="solid",
#                                     color_scheme="gray",
#                                     opacity="0.5",
#                                     high_contrast=False,
                                    
#                                 ),
#                             ),
#                             rx.text("Prang", font_size="1em", color="black"),
#                             spacing="2",
#                             align_items="center",
#                             justify_content="center",
#                             margin_top="2em",

#                         ),
#                     ),
#                     background_color="#FFDA5D",
#                     border_radius="1rem",
#                     width="22em",
#                     overflow="hidden",
#                     box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                     _hover={
#                         "transform": "scale(1.05)",
#                         "transition": "transform 0.2s ease-in-out"
#                     },
#                     padding="2em 1.5em 2em 1.5em",

                    
#                 ),
#                 rx.box(
#                     rx.vstack(
#                         rx.text("Rust for beginner", font_size="1.5em", font_weight="bold", color="black"),
#                         rx.box(
#                             "12 terms",
#                             font_size="0.75em",
#                             color="black",
#                             background_color="#FFF5D0",
#                             border_radius="1.5em",
#                             padding="1px 20px 1px 20px",
#                             width="fit-content",
#                             height="fit-content",
#                             margin_bottom="2em",
#                         ),
#                         rx.hstack(
#                             rx.box(
#                                 rx.avatar(
#                                     src="/static/logo.png",
#                                     size="3",
#                                     radius="full",
#                                     fallback="",
#                                     variant="solid",
#                                     color_scheme="gray",
#                                     opacity="0.5",
#                                     high_contrast=False,
#                                 ),
#                             ),
#                             rx.text("Khaopun", font_size="1em", color="black"),
#                             spacing="2",
#                             align_items="center",
#                             justify_content="center",
#                             margin_top="2em",

#                         ),
#                     ),
#                     background_color="#FFDA5D",
#                     border_radius="1rem",
#                     width="22em",
#                     overflow="hidden",
#                     box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                     _hover={
#                         "transform": "scale(1.05)",
#                         "transition": "transform 0.2s ease-in-out"
#                     },
#                     padding="2em 1.5em 2em 1.5em",

                    
#                 ),
#                 rx.box(
#                     rx.vstack(
#                         rx.text("OOP for beginner", font_size="1.5em", font_weight="bold", color="black"),
#                         rx.box(
#                             "20 terms",
#                             font_size="0.75em",
#                             color="black",
#                             background_color="#FFF5D0",
#                             border_radius="1.5em",
#                             padding="1px 20px 1px 20px",
#                             width="fit-content",
#                             height="fit-content",
#                             margin_bottom="2em",
#                         ),
#                         rx.hstack(
#                             rx.box(
#                                 rx.avatar(
#                                     src="/static/logo.png",
#                                     size="3",
#                                     radius="full",
#                                     fallback="",
#                                     variant="solid",
#                                     color_scheme="gray",
#                                     opacity="0.5",
#                                     high_contrast=False,
#                                 ),
#                             ),
#                             rx.text("Bew", font_size="1em", color="black"),
#                             spacing="2",
#                             align_items="center",
#                             justify_content="center",
#                             margin_top="2em",

#                         ),
#                     ),
#                     background_color="#FFDA5D",
#                     border_radius="1rem",
#                     width="22em",
#                     overflow="hidden",
#                     box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                     _hover={
#                         "transform": "scale(1.05)",
#                         "transition": "transform 0.2s ease-in-out"
#                     },
#                     padding="2em 1.5em 2em 1.5em",

                    
#                 ),
#                 align="center",
#                 spacing="6",
#                 margin_left="6em",
#                 width="100%",  # Full width for the hstack
#                 justify_content="center",  # Center the boxes in the row
#             ),
#         ),
#         spacing="4",
#         padding="0 4em 4em 4em",  # Add padding inside the background
#         width="100%",  # Make hstack take full width
#     )



# def Super_Bottom_area() -> rx.Component:
#     return rx.vstack(
#         rx.text("Top Creators", font_size="4em", font_weight="bold", color="black", margin_left="1.5em"),
#         # First Row
#         rx.hstack(
#             #Column1
#             rx.hstack(
#                 rx.box(
#                     rx.vstack(
                        
#                         rx.vstack(
#                             rx.box(
#                                 rx.avatar(
#                                     src="/static/logo.png",
#                                     size="6",
#                                     radius="full",
#                                     fallback="",
#                                     variant="solid",
#                                     color_scheme="gray",
#                                     opacity="0.5",
#                                     high_contrast=False,
#                                     margin_bottom="2em",
#                                 ),
#                             ),
#                             rx.text("Prang", font_size="1.5em", font_weight="bold", color="black"),
#                             spacing="2",
#                             align_items="center",
#                             justify_content="center",

#                         ),
#                         rx.hstack(
#                             rx.box(
#                                 rx.hstack(  # Use hstack to arrange horizontally
#                                     rx.image(  # Add image component
#                                         src="/smallM.png",
#                                         width="20px",
#                                         height="20px",
#                                         fit='cover',
#                                     ),
#                                     rx.text(  # Text component for better control
#                                         "12 mindmap sets",
#                                         font_size="0.75em",
#                                         color="black",
#                                     ),
#                                     align="center",
#                                     spacing="1",  # Add space between image and text
#                                 ),
#                                 background_color="#FFF5D0",
#                                 border_radius="1em", 
#                                 padding="1px 5px 1px 5px",
#                                 width="fit-content",
#                                 height="fit-content",
#                             ),
#                             rx.box(
#                                 rx.hstack(  # Use hstack to arrange horizontally
#                                     rx.image(  # Add image component
#                                         src="/champ.png",
#                                         width="20px",
#                                         height="20px",
#                                         fit='cover',
#                                     ),
#                                     rx.text(  # Text component for better control
#                                         "5 contests",
#                                         font_size="0.75em",
#                                         color="black",
#                                     ),
#                                     align="center",
#                                     spacing="1",  # Add space between image and text
#                                 ),
#                                 background_color="#FFF5D0",
#                                 border_radius="1em", 
#                                 padding="1px 5px 1px 5px",
#                                 width="fit-content",
#                                 height="fit-content",
#                             ),
#                             spacing="2",
#                         ),
#                     ),
#                     background_color="#FFDA5D",
#                     border_radius="1rem",
#                     width="22em",
#                     overflow="hidden",
#                     box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                     _hover={
#                         "transform": "scale(1.05)",
#                         "transition": "transform 0.2s ease-in-out"
#                     },
#                     padding="2em 1.5em 2em 1.5em",

                    
#                 ),
#                 rx.box(
#                     rx.vstack(
                        
#                         rx.vstack(
#                             rx.box(
#                                 rx.avatar(
#                                     src="/static/logo.png",
#                                     size="6",
#                                     radius="full",
#                                     fallback="",
#                                     variant="solid",
#                                     color_scheme="gray",
#                                     opacity="0.5",
#                                     high_contrast=False,
#                                     margin_bottom="2em",
#                                 ),
#                             ),
#                             rx.text("karina", font_size="1.5em", font_weight="bold", color="black"),
#                             spacing="2",
#                             align_items="center",
#                             justify_content="center",

#                         ),
#                         rx.hstack(
#                             rx.box(
#                                 rx.hstack(  # Use hstack to arrange horizontally
#                                     rx.image(  # Add image component
#                                         src="/smallM.png",
#                                         width="20px",
#                                         height="20px",
#                                         fit='cover',
#                                     ),
#                                     rx.text(  # Text component for better control
#                                         "5 mindmap sets",
#                                         font_size="0.75em",
#                                         color="black",
#                                     ),
#                                     align="center",
#                                     spacing="1",  # Add space between image and text
#                                 ),
#                                 background_color="#FFF5D0",
#                                 border_radius="1em", 
#                                 padding="1px 5px 1px 5px",
#                                 width="fit-content",
#                                 height="fit-content",
#                             ),
#                             rx.box(
#                                 rx.hstack(  # Use hstack to arrange horizontally
#                                     rx.image(  # Add image component
#                                         src="/champ.png",
#                                         width="20px",
#                                         height="20px",
#                                         fit='cover',
#                                     ),
#                                     rx.text(  # Text component for better control
#                                         "2 contests",
#                                         font_size="0.75em",
#                                         color="black",
#                                     ),
#                                     align="center",
#                                     spacing="1",  # Add space between image and text
#                                 ),
#                                 background_color="#FFF5D0",
#                                 border_radius="1em", 
#                                 padding="1px 5px 1px 5px",
#                                 width="fit-content",
#                                 height="fit-content",
#                             ),
#                             spacing="2",
#                         ),
#                     ),
#                     background_color="#FFDA5D",
#                     border_radius="1rem",
#                     width="22em",
#                     overflow="hidden",
#                     box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                     _hover={
#                         "transform": "scale(1.05)",
#                         "transition": "transform 0.2s ease-in-out"
#                     },
#                     padding="2em 1.5em 2em 1.5em",

                    
#                 ),
#                 rx.box(
#                     rx.vstack(
                        
#                         rx.vstack(
#                             rx.box(
#                                 rx.avatar(
#                                     src="/static/logo.png",
#                                     size="6",
#                                     radius="full",
#                                     fallback="",
#                                     variant="solid",
#                                     color_scheme="gray",
#                                     opacity="0.5",
#                                     high_contrast=False,
#                                     margin_bottom="2em",
#                                 ),
#                             ),
#                             rx.text("AsaBm", font_size="1.5em", font_weight="bold", color="black"),
#                             spacing="2",
#                             align_items="center",
#                             justify_content="center",

#                         ),
#                         rx.hstack(
#                             rx.box(
#                                 rx.hstack(  # Use hstack to arrange horizontally
#                                     rx.image(  # Add image component
#                                         src="/smallM.png",
#                                         width="20px",
#                                         height="20px",
#                                         fit='cover',
#                                     ),
#                                     rx.text(  # Text component for better control
#                                         "122 mindmap sets",
#                                         font_size="0.75em",
#                                         color="black",
#                                     ),
#                                     align="center",
#                                     spacing="1",  # Add space between image and text
#                                 ),
#                                 background_color="#FFF5D0",
#                                 border_radius="1em", 
#                                 padding="1px 5px 1px 5px",
#                                 width="fit-content",
#                                 height="fit-content",
#                             ),
#                             rx.box(
#                                 rx.hstack(  # Use hstack to arrange horizontally
#                                     rx.image(  # Add image component
#                                         src="/champ.png",
#                                         width="20px",
#                                         height="20px",
#                                         fit='cover',
#                                     ),
#                                     rx.text(  # Text component for better control
#                                         "52 contests",
#                                         font_size="0.75em",
#                                         color="black",
#                                     ),
#                                     align="center",
#                                     spacing="1",  # Add space between image and text
#                                 ),
#                                 background_color="#FFF5D0",
#                                 border_radius="1em", 
#                                 padding="1px 5px 1px 5px",
#                                 width="fit-content",
#                                 height="fit-content",
#                             ),
#                             spacing="2",
#                         ),
#                     ),
#                     background_color="#FFDA5D",
#                     border_radius="1rem",
#                     width="22em",
#                     overflow="hidden",
#                     box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
#                     _hover={
#                         "transform": "scale(1.05)",
#                         "transition": "transform 0.2s ease-in-out"
#                     },
#                     padding="2em 1.5em 2em 1.5em",

                    
#                 ),
#                 align="center",
#                 spacing="6",
#                 margin_left="6em",
#                 width="100%",  # Full width for the hstack
#                 justify_content="center",  # Center the boxes in the row
#             ),
#         ),
#         spacing="4",
#         margin_bottom="0",
#         padding="0 4em 4em 4em",  # Add padding inside the background
#         width="100%",  # Make hstack take full width
#     )




# def Entire_page_main() -> rx.Component:
#     return rx.vstack(  
#         Top_Area(),
#         Middle_area(),
#         Bottom_area(),
#         Super_Bottom_area(),

#         background_color="#FFFBEA",
#         width="100vw",
#     )







from typing import List, Dict
import reflex as rx
from app.components import SidebarToggle, sidebar, sidebar_expand
from app.states import Main_Pages_state



def search_area() -> rx.Component:
    return rx.hstack(
        rx.input(
            rx.input.slot(
                rx.image(
                    src="/searchArea.png",
                    width="100%",
                    height="90%",
                    fit='cover',
                    padding="0.5em",
                ),
            ),
            value=Main_Pages_state.search_text,  # Bind value to state
            on_change=Main_Pages_state.set_search,  # Update state when input changes
            placeholder="Search public mindmaps and contests",
            width="65vw",
            height="100px",
            bg='white',
            style={"& input::placeholder": {"color": "grey", "opacity": "0.25"}},
            border_radius="0.5em",
            color="grey",
            font_size="2em",
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.25)",
        ),
        rx.button(
            "Search",
            on_click=Main_Pages_state.handle_search,  # Add click handler
            color="black",
            font_size="2em",
            font_weight="bold",
            bg="#FFDA5D",
            border_radius="8px",
            padding="10px",
            width="6em",
            height="60px",
            overflow="hidden",
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
            _hover={
                "transform": "scale(1.05)",
                "transition": "transform 0.2s ease-in-out",
                "cursor": "pointer",
            }
        ),
        align="center",
        justify_content="space-between",
        width="100%",
    )

# def recent_mindmap_item(mindmap: dict) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.image(
                src=mindmap["image"].to_string(),
                width="100%",
                height="100%",
                object_fit="cover",
            ),
            bg="#FFDA5D",
            border_radius="1.5em",
            padding="1em",
            width="120px",
            height="120px",
            overflow="hidden",
            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
            _hover={
                "transform": "scale(1.05)",
                "transition": "transform 0.2s ease-in-out"
            } 
        ),
        rx.vstack(
            rx.text(mindmap["name"].to_string(), font_size="2em", font_weight="bold", color="black"),
            rx.text(
                f"Mindmap set    ●    {mindmap['terms'].to_string()} terms    ●    by {mindmap['creator'].to_string()}", 
                font_size="1em",
                color="#969696",
            ),
            spacing="0",
            align_items="start",
        ),
        align="center",
        spacing="6",
        margin_left="6em",

        
    )


def recent_mindmap_item(mindmap: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.image(
                    src=mindmap["image"],
                    width="100%",
                    height="100%",
                    object_fit="cover"
                ),
                bg="#FFDA5D",
                border_radius="1.5em",
                padding="1em",
                width="6em",
                height="6em",
                overflow="hidden",
                box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
                _hover={
                    "transform": "scale(1.05)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                }
            ),
            rx.vstack(
                rx.text(mindmap["name"], font_size="2em", font_weight="bold", color="black"),
                rx.text(
                    f"Mindmap set    ●    {mindmap['terms']} terms    ●    by {mindmap['creator']}", 
                    font_size="1em",
                    color="#969696",
                    margin_left="1em",
                    white_space="pre",
                ),
                spacing="0",
                align_items="start",
            ),
            align="center",
            spacing="6",
            _hover={
                    "transform": "scale(1.02)",
                    "transition": "transform 0.2s ease-in-out",
                    "cursor": "pointer",
                }
        ),
        margin_right="6em",
        width="100%",  # Full width for the box
    )

def recent_mindmaps_section() -> rx.Component:
    return rx.vstack(
        rx.text("Recents", font_size="4em", font_weight="bold", color="black", align="left",width="100%"),
        rx.grid(  # Use grid instead of vstack for the items
            rx.foreach(
                Main_Pages_state.recent_mindmaps,
                recent_mindmap_item
            ),
            columns="2",  # Set 2 columns
            spacing="6",  # Add spacing between grid items
            width="100%",
        ),
        spacing="4",
        padding="0 4em 4em 4em",  # Add padding inside the background
        width="auto",  # Make hstack take full width
        align_self="left",
    )



def favorite_mindmap_item(mindmap: Dict[str, str]) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(mindmap["name"], font_size="1.5em", font_weight="bold", color="black"),
            rx.box(
                f"{mindmap['terms'].to_string()} terms",
                font_size="0.75em",
                color="black",
                background_color="#FFF5D0",
                border_radius="1.5em",
                padding="1px 20px 1px 20px",
                width="fit-content",
                height="fit-content",
                margin_bottom="2em",
            ),
            rx.hstack(
                rx.avatar(
                    src=mindmap["avatar"].to_string(),
                    size="3",
                    radius="full",
                    fallback="",
                    variant="solid",
                    color_scheme="gray",
                    opacity="1",
                    high_contrast=False,
                ),
                rx.text(mindmap["creator"], font_size="1em", color="black"),
                spacing="2",
                align_items="center",
                justify_content="center",
                margin_top="2em",
            ),
        ),
        background_color="#FFDA5D",
        border_radius="1rem",
        width="22em",
        overflow="hidden",
        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
        _hover={
            "transform": "scale(1.05)",
            "transition": "transform 0.2s ease-in-out",
            "cursor": "pointer",
        },
        padding="2em 1.5em 2em 1.5em",
    )

def creator_item(creator: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.avatar(
                    src=creator["avatar"].to_string(),
                    size="6",
                    radius="full",
                    fallback="",
                    variant="solid",
                    color_scheme="gray",
                    opacity="1",
                    high_contrast=False,
                    margin_bottom="2em",
                ),
                rx.text(creator["name"], font_size="1.5em", font_weight="bold", color="black"),
                spacing="2",
                align_items="center",
                justify_content="center",
            ),
            
            rx.hstack(
                rx.box(
                    rx.hstack(
                        rx.image(
                            src="/smallM.png",
                            width="20px",
                            height="20px",
                            fit='cover',
                        ),
                        rx.text(
                            f"{creator['mindmap_count'].to_string()} mindmap sets",
                            font_size="0.75em",
                            color="black",
                        ),
                        align="center",
                        spacing="1",
                    ),
                    background_color="#FFF5D0",
                    border_radius="1em",
                    padding="1px 5px",
                    width="fit-content",
                    height="fit-content",
                ),
                rx.box(
                    rx.hstack(
                        rx.image(
                            src="/champ.png",
                            width="20px",
                            height="20px",
                            fit='cover',
                        ),
                        rx.text(
                            f"{creator['contest_count'].to_string()} contests",
                            font_size="0.75em",
                            color="black",
                        ),
                        align="center",
                        spacing="1",
                    ),
                    background_color="#FFF5D0",
                    border_radius="1em",
                    padding="1px 5px",
                    width="fit-content",
                    height="fit-content",
                ),
                spacing="2",
            ),
        ),
        background_color="#FFDA5D",
        border_radius="1rem",
        width="22em",
        overflow="hidden",
        box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
        _hover={
            "transform": "scale(1.05)",
            "transition": "transform 0.2s ease-in-out",
            "cursor": "pointer",
        },
        padding="2em 1.5em 2em 1.5em",
        align="start",
        
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
            width=rx.cond(
                SidebarToggle.expanded,
                "calc(100vw - 300px)",
                "calc(100vw - 100px)"
            ),
        ),
        width="100%",
        spacing="0",
        overflow="hidden",
    )

def index_main() -> rx.Component:
    return layout(
            rx.vstack(
            # Top Area
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text(f"Hello {Main_Pages_state.current_user['username']}!!🤫", font_size="6em", font_weight="bold", color="black"),
                        rx.text("Welcome back, let's start practice today", font_size="1.5em", color='#919191'),
                        spacing="0",
                    ),
                    rx.hstack(
                        rx.button(
                            rx.image(src="/AddM.png", width="100%", height="100%",fit='cover',),
                            bg="#FDCC00",
                            width="6em",
                            border_radius="8px",  # Optional: Rounded corners
                            padding="10px",
                            height="6em",
                            overflow="hidden",
                            box_shadow="0px 4px 12px rgba(0, 0, 0, 0.15)",
                            _hover={
                                "transform": "scale(1.05)",
                                "transition": "transform 0.2s ease-in-out",
                                "cursor": "pointer",
                            }
                        ),
                        # Fixed size avatar
                        rx.box(
                            rx.avatar(
                                src=Main_Pages_state.current_user["avatar"],
                                size="9",
                                radius="full",
                                fallback="PROFILE",
                                variant="solid",
                                color_scheme="gray",
                                opacity="1",
                                high_contrast=False,
                                background_color="white",
                            ),
                            width="fit-content",
                            height="fit-content",
                            margin_right="5em",
                        ),
                        align="center",
                        spacing="7",
                        width="auto",  # Full width for the hstack
                    ),

                    spacing="2",
                    align_items="center",
                    width="100%",
                    justify_content="space-between",
                ),
                rx.hstack(
                    search_area(),
                    width="100%",
                ),
                padding="4em 4em 0 4em",  # Add padding inside the background
                width="100%",  # Full width of the viewport
            ),

            # Recent Mindmaps
            # rx.vstack(
            #     rx.text("Recents", font_size="4em", font_weight="bold", color="black"),
            #     rx.foreach(
            #         Main_Pages_state.recent_mindmaps,
            #         recent_mindmap_item
            #     ),
            #     padding="2em",
            # ),
            recent_mindmaps_section(),


            # Favorites
            rx.vstack(
                rx.text("Favorites", font_size="4em", font_weight="bold", color="black", align="left",width="100%"),
                rx.hstack(
                    rx.foreach(
                        Main_Pages_state.favorite_mindmaps,
                        favorite_mindmap_item
                    ),
                    spacing="7",
                    width="100%",  # Full width for the hstack
                    justify="start",
                    align="start",
                ),
                spacing="4",
                padding="0 4em 4em 4em",  # Add padding inside the background
                width="100%",  # Make hstack take full width
                align_self="start",

            ),

            # Top Creators
            rx.vstack(
                rx.text("Top Creators", font_size="4em", font_weight="bold", color="black", align="left",width="100%"),
                rx.hstack(
                    rx.foreach(
                        Main_Pages_state.top_creators,
                        creator_item
                    ),
                    spacing="7",
                    width="100%",
                    justify="start",
                    align="start",
                ),
                spacing="4",
                margin_bottom="0",
                padding="0 4em 4em 4em",  # Add padding inside the background
                width="100%",  # Make hstack take full width
                align_self="start",

            ),

            background_color="#FFFBEA",
            width="100%",
            spacing="2",
            height="100%",
            overflow_y="auto",  # Allow scrolling within the content
            overflow_x="auto", # Prevent horizontal overflow
        ),

    )