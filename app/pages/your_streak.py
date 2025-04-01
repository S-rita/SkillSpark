
import reflex as rx
from datetime import date, timedelta
from datetime import datetime
import calendar
from app.components import SidebarToggle, sidebar, sidebar_expand


# Sample login data for demonstration
# login_data = {
#     date(2025, 3, 3): True,
#     date(2025, 3, 4): True,
#     date(2025, 3, 5): True,
#     date(2025, 3, 6): True,
#     date(2025, 3, 8): True,
#     date(2025, 3, 10): True,
#     date(2025, 3, 11): True,
# }

# current_month = date(2025, 3, 1)

# month_inyear = {
#     1: "January",
#     2: "February",
#     3: "March",
#     4: "April",
#     5: "May",
#     6: "June",
#     7: "July",
#     8: "August",
#     9: "September",
#     10: "October",
#     11: "November",
#     12: "December",
# }

# dayLogin_month = {
#     1: [],
#     2: [],
#     3: [],
#     4: [],
#     5: [],
#     6: [],
#     7: [],
#     8: [],
#     9: [],
#     10: [],
#     11: [],
#     12: [],
# }



# def calculate_streak():
#     """Calculate the longest streak of consecutive login days."""
#     sorted_dates = sorted(login_data.keys(), reverse=True)
#     streak = 0
#     for i in range(len(sorted_dates) - 1):
#         if (sorted_dates[i] - sorted_dates[i + 1]).days == 1:
#             streak += 1
#         else:
#             break
#     return streak + 1 if streak > 0 else 0  # Adjust for single login days

# def is_consecutive(day: date) -> bool:
#     """Check if a given day is part of a consecutive streak."""
#     return day in login_data and (day - timedelta(days=1)) in login_data

# def change_month(offset: int):
#     """Change the current month by the given offset (positive or negative)."""
#     global current_month
#     new_month = current_month.replace(day=1) + timedelta(days=offset * 30)
#     current_month = new_month.replace(day=1)


# def calendar_component():
#     """Generate a Reflex component for displaying the streak calendar."""
#     first_day = date(2025, 3, 1)


#     calendar = []
#     for week in range(5):
#         row = []
#         for day in range(7):
#             current_day = first_day + timedelta(days=(week * 7 + day))

#             if current_day.month == first_day.month:  # Only display March
#                 if current_day in login_data:
#                     color = "orange" if is_consecutive(current_day) else ""
#                     icon = "🔥" if is_consecutive(current_day) else "🟡"
#                     row.append(rx.box(icon, bg=color, p="4px", border_radius="50%"))
#                 else:
#                     row.append(rx.box("🔘", bg="transparent", p="4px", border="none"))
#             else:
#                 row.append(rx.box(" "))
#         calendar.append(rx.hstack(*row, spacing='8'))

#     return rx.vstack(
#         rx.text(f"🔥 {calculate_streak()} day streak", font_size="5rem", font_weight="bold", color="black"),
#         rx.box(
#             rx.hstack(  # Horizontal stack for month label and buttons
            
#             rx.hstack(
#                 rx.button("◀", on_click=change_month(-1)),
#                 rx.text(f"{first_day.strftime('%b %Y')}", font_size="1.5rem", color="black", align="center"),
#                 rx.button("▶", on_click=change_month(1)),
#                 spacing="9",
#             ),
#             spacing="9",
#             align_items="center",
#             ),

#             # rx.text("MAR 2025", font_size="1.5rem", color="black"),
#             rx.vstack(*calendar),
#             width="70vw",  # Set a fixed width for the square
#             height="65vh",  # Set a fixed height for the square
#             bg="white",  # Background color for the square
#             border_radius="5%",  # Optional: round the corners of the square
#             padding="30px",  # Padding inside the square
            


#         ),
#         align_items="center",
#         spacing='9',
#         margin_top="10vh",
#         margin_bottom="10vh",
#     )

# def index() -> rx.Component:
#     return rx.center(calendar_component(),
#         bg="#FFFBEA",)



import reflex as rx
from datetime import date, timedelta, datetime
import calendar
from app.components import SidebarToggle, sidebar, sidebar_expand



# State
class CalendarState(rx.State):
    current_month: int = datetime.now().month
    current_year: int = datetime.now().year
    login_dates: list[dict] = [
        {"date": date(current_year, 1, 5), "has_login": True},
        {"date": date(current_year, 1, 6), "has_login": True},
        {"date": date(current_year, 1, 15), "has_login": True},
        {"date": date(current_year, 1, 16), "has_login": True},
        {"date": date(current_year, 1, 25), "has_login": True},
        {"date": date(current_year, 2, 1), "has_login": True},
        {"date": date(current_year, 2, 9), "has_login": True},
        {"date": date(current_year, 2, 10), "has_login": True},
        {"date": date(current_year, 2, 11), "has_login": True},
        {"date": date(current_year, 2, 20), "has_login": True},
        {"date": date(current_year, 2, 28), "has_login": True},
        {"date": date(current_year, 3, 5), "has_login": True},
        {"date": date(current_year, 3, 10), "has_login": True},
        {"date": date(current_year, 3, 15), "has_login": True},
        {"date": date(current_year, 3, 20), "has_login": True},
        {"date": date(current_year, 3, 21), "has_login": True},
        {"date": date(current_year, 3, 25), "has_login": True},
        {"date": date(current_year, 3, 31), "has_login": True},
        {"date": date(current_year, 4, 1), "has_login": True},
    ]

    @rx.var
    def current_streak(self) -> tuple[str, int]:
        """Get current streak of consecutive days ending with today."""
        today = datetime.now()
        
        # Get all login dates for current month and year
        current_streak = 0
        
        # Get all login dates sorted by date
        login_dates = sorted([
            d["date"] 
            for d in self.login_dates
        ], reverse=True)
        
        # Find consecutive days ending with today
        for date in login_dates:
            if date == today.date():
                current_streak = 1
                prev_date = today.date() - timedelta(days=1)
                
                # Check previous consecutive days
                while prev_date in [d["date"] for d in self.login_dates]:
                    current_streak += 1
                    prev_date -= timedelta(days=1)
                break
        
        # Format text based on streak
        if current_streak == 0:
            return "0 day streak", 0
        elif current_streak == 1:
            return "1 day streak", 1
        else:
            return f"{current_streak} days streak", current_streak
        

    @rx.var
    def streak_image(self) -> str:
        """Get streak image based on current streak."""
        _, streak = self.current_streak
        
        if streak == 1:
            return "/lowCostFire.png"
        else:
            return "/Fire_lowBG.png"

    # Add a new method to check if a day is part of consecutive days
    @rx.var
    def is_consecutive_day(self) -> list[int]:
        """Get all days that are part of consecutive sequences"""
        current_month_dates = sorted([
            d["date"] 
            for d in self.login_dates 
            if (d["date"].month == self.current_month and d["date"].year == self.current_year) or
            (d["date"].month == self.current_month-1 and d["date"].year == self.current_year and d["date"].day == 31) or
            (self.current_month == 1 and d["date"].month == 12 and d["date"].year == self.current_year-1 and d["date"].day == 31)
        ])
        
        next_month_dates = sorted([
            d["date"]
            for d in self.login_dates
            if ((d["date"].month == self.current_month+1 and d["date"].year == self.current_year and d["date"].day == 1) or
                (self.current_month == 12 and d["date"].month == 1 and d["date"].year == self.current_year+1 and d["date"].day == 1))
        ])
        
        # Combine the dates
        all_relevant_dates = sorted(current_month_dates + next_month_dates)
        
        consecutive_days = []
        current_group = []
        
        for i in range(len(all_relevant_dates)):
            if not current_group:
                current_group.append(all_relevant_dates[i])
            elif (all_relevant_dates[i] - current_group[-1]).days == 1:
                current_group.append(all_relevant_dates[i])
            else:
                if len(current_group) > 1:
                    consecutive_days.extend([d.day for d in current_group if d.month == self.current_month])
                current_group = [all_relevant_dates[i]]
        
        if len(current_group) > 1:
            consecutive_days.extend([d.day for d in current_group if d.month == self.current_month])
            
        return consecutive_days

    

    

    @rx.var
    def dates_in_current_month(self) -> list[str]:
        """Get login dates for current month as strings"""
        return [
            str(d["date"].day)
            for d in self.login_dates 
            if d["date"].month == self.current_month and 
                d["date"].year == self.current_year
        ]
    
    def next_month(self):
        # Only allow going forward if not at current month/year
        if (self.current_month < datetime.now().month or 
            self.current_year < datetime.now().year):
            if self.current_month == 12:
                self.current_month = 1
                self.current_year += 1
            else:
                self.current_month += 1
            
    def prev_month(self):
        # Only allow going back if not at January of current year
        if self.current_month > 1 and self.current_year == datetime.now().year:
            self.current_month -= 1

    @rx.var
    def month_name(self) -> str:
        return calendar.month_name[int(self.current_month)]
    
    @rx.var
    def can_go_forward(self) -> bool:
        return (self.current_month < datetime.now().month or 
                self.current_year < datetime.now().year)

    @rx.var
    def can_go_back(self) -> bool:
        return self.current_month > 1 and self.current_year == datetime.now().year
    
    @rx.var
    def days_in_month(self) -> int:
        return calendar.monthrange(self.current_year, self.current_month)[1]
    
    @rx.var
    def prev_month_days(self) -> int:
        if self.current_month == 1:
            return calendar.monthrange(self.current_year - 1, 12)[1]
        return calendar.monthrange(self.current_year, self.current_month - 1)[1]
    
    @rx.var
    def first_day_offset(self) -> int:
        # January starts on Wednesday (3)
        if self.current_month == 1:
            return 3
        
        # Calculate cumulative days to determine first day of other months
        total_days = 3  # Start from Wednesday
        for month in range(1, self.current_month):
            total_days += calendar.monthrange(self.current_year, month)[1]
        return total_days % 7


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