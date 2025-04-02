import reflex as rx
import calendar
from datetime import date, timedelta, datetime


#????? main_page   
#????? recent section use name, terms, creator, image 
#????? favorite_mindmaps section use name, terms, creator, image of that mindmap creator
#????? top_creators section use name, mindmap_count( count users mindmap sets ), contest_count( count users contests ), image
#????? Current user use username, bookmark_mindmap( list of mindmap name ), achievements_ids( list of achievement id ), user_id, image

#????? searching page
#????? Mind_map section use name, terms, creator, image of that mindmap creator
#????? Contest section use name, sets, creator, image of that contest creator
class Main_Pages_state(rx.State):
    """The app state."""

    # Add search text state
    search_text: str = ""
    display_text: str = ""  # Store the displayed text
    filtered_mindmaps: list[dict] = []  # New state var for filtered results#!!!!!
    filtered_contests: list[dict] = []  # New state var for filtered contests#!!!!!


    # Add state var to track view on search page when click "view more" button
    show_mindmaps_full: bool = False
    show_contests_full: bool = False

    def toggle_mindmaps_view(self):
        self.show_mindmaps_full = not self.show_mindmaps_full
        self.show_contests_full = False  # Reset other view

    def toggle_contests_view(self):
        self.show_contests_full = not self.show_contests_full
        self.show_mindmaps_full = False  # Reset other view


    # Add a state variable to track the search results is it have mind map > 3 if yes show "view more" button
    @rx.var
    def has_more_mindmaps(self) -> bool:
        return len(self.filtered_mindmaps) > 3
    
    # Add a state variable to track the search results is it have contest > 3 if yes show "view more" button
    @rx.var
    def has_more_contests(self) -> bool:
        return len(self.filtered_contests) > 3
        
    #for Slide show##########################################
    current_index: int = 0  # Track current position

    @rx.var
    def visible_mindmaps(self) -> list[dict]:
        # Show 3 mindmaps at a time starting from current_index
        return self.favorite_mindmaps[self.current_index:self.current_index + 3]
    
    @rx.var
    def can_go_next(self) -> bool:
        return self.current_index + 3 < len(self.favorite_mindmaps)
    
    @rx.var 
    def can_go_prev(self) -> bool:
        return self.current_index > 0
        
    def next_slide(self):
        if self.can_go_next:
            self.current_index += 3
            
    def prev_slide(self):
        if self.can_go_prev:
            self.current_index -= 3
    ###################################################

    def set_search(self, value: str):
        """Set the search text."""
        self.search_text = value

    # @rx.event
    # def handle_search(self):
    #     """Handle search button click."""
    #     self.display_text = self.search_text
    #     return rx.redirect(f"/search?q={self.search_text}")
    @rx.event
    def handle_search(self):
        """Handle search button click for main page"""
        if not self.search_text:
            return
        self.display_text = self.search_text
        
        # Split into individual words and filter out empty strings
        search_words = [word.lower() for word in self.search_text.split() if word]
        
        # Filter mindmaps - match if any search word is in the name
        self.filtered_mindmaps = [
            mindmap for mindmap in self.Mind_map
            if any(word in mindmap["name"].lower() for word in search_words)
        ]

        # Filter contests - match if any search word is in the name
        self.filtered_contests = [
            contest for contest in self.Contest
            if any(word in contest["name"].lower() for word in search_words)
        ]

        return rx.redirect("/search")

    @rx.event 
    def handle_search_page(self):
        """Handle search button click for search page"""
        if not self.search_text:
            return
        self.display_text = self.search_text

        # Split into individual words and filter out empty strings
        search_words = [word.lower() for word in self.search_text.split() if word]
        
        # Filter mindmaps - match if any search word is in the name
        self.filtered_mindmaps = [
            mindmap for mindmap in self.Mind_map
            if any(word in mindmap["name"].lower() for word in search_words)
        ]

        # Filter contests - match if any search word is in the name
        self.filtered_contests = [
            contest for contest in self.Contest
            if any(word in contest["name"].lower() for word in search_words)
        ]



    @rx.var
    def check_results(self) -> str:
        # Both empty
        if len(self.filtered_mindmaps) == 0 and len(self.filtered_contests) == 0:
            return "none"
        # Only mindmaps have results
        elif len(self.filtered_mindmaps) > 0 and len(self.filtered_contests) == 0:
            return "mindmaps_only"
        # Only contests have results  
        elif len(self.filtered_mindmaps) == 0 and len(self.filtered_contests) > 0:
            return "contests_only"
        # Both have results
        else:
            return "both"

    # User data

    current_user: dict[str, str] = {
        "username": "Asayaa",  # Default user name
        "email": "66011148@kmitl.ac.th",
        "password": "12345678",
        "bookmark_mindmap" : [],
        "achievements_ids": [],
        "user_id": "1234567890",
        "image": "/prettestGirlInDaWorldo.png"
    }



    # Recent mindmaps data
    recent_mindmaps: list[dict] = [
        {
            "name": "Chinese Sentences",
            "terms": 27,
            "creator": "Sarita",
            "image": "/mindmaptail.png"
        },
        {
            "name": "German Sentences", 
            "terms": 27,
            "creator": "Sarita",
            "image": "/mindmaptail.png"
        },
        {
            "name": "Python Programming",
            "terms": 109, 
            "creator": "Sarita",
            "image": "/mindmaptail.png"
        },
        {
            "name": "I Love AI",
            "terms": 12,
            "creator": "Sarita", 
            "image": "/mindmaptail.png"
        }
    ]

    # Favorite mindmaps data 
    favorite_mindmaps: list[dict] = [
        {
            "name": "Python is the Best",
            "terms": 27,
            "creator": "Prang",
            "image": "/static/logo.png"
        },
        {
            "name": "Rust for beginner",
            "terms": 12, 
            "creator": "Khaopun",
            "image": "/static/logo.png"
        },
        {
            "name": "OOP for beginner",
            "terms": 20,
            "creator": "Bew",
            "image": "/static/logo.png" 
        },
        {
            "name": "idk",
            "terms": 24,
            "creator": "Bew",
            "image": "/static/logo.png" 
        }
    ]

    # Top creators data
    top_creators: list[dict] = [
        {
            "name": "Prang",
            "mindmap_count": 12,
            "contest_count": 5,
            "image": "/static/logo.png"
        },
        {
            "name": "karina",
            "mindmap_count": 5,
            "contest_count": 2,
            "image": "/static/logo.png"
        },
        {
            "name": "AsaBm",
            "mindmap_count": 122,
            "contest_count": 52,
            "image": "/static/logo.png"
        }
    ]

    # all mindmaps data 
    Mind_map: list[dict] = [
        {
            "name": "Python is the Best",
            "terms": 27,
            "creator": "Prang",
            "image": "/static/logo.png"
        },
        {
            "name": "Rust for beginner",
            "terms": 12, 
            "creator": "Khaopun",
            "image": "/static/logo.png"
        },
        {
            "name": "OOP for beginner",
            "terms": 20,
            "creator": "Bew",
            "image": "/static/logo.png" 
        },
        {
            "name": "oyh",
            "terms": 20,
            "creator": "Bew",
            "image": "/static/logo.png" 
        },
        {
            "name": "asaaaa",
            "terms": 20,
            "creator": "Bew",
            "image": "/static/logo.png" 
        }
    ]

    # all contests data 
    Contest: list[dict] = [
        {
            "name": "Python is the Best",
            "sets": 27,
            "creator": "Prang",
            "image": "/static/logo.png"
        },
        {
            "name": "Rust for beginner",
            "sets": 12, 
            "creator": "Khaopun",
            "image": "/static/logo.png"
        },
        {
            "name": "OOP for beginner",
            "sets": 20,
            "creator": "Bew",
            "image": "/static/logo.png" 
        },
        {
            "name": "C++ for u",
            "sets": 5,
            "creator": "bbeee",
            "image": "/static/logo.png" 
        }
    ]




#????? achievements page
#????? Achievements data use  name, image, category, completion,
class Achiecement_State(rx.State):
    """The app state."""
    # Achievement data structure based on your Achievement model
    achievements: list[dict] = [
        # Best of the best achievements
        {
            "id": "perfectionist",
            "name": "Perfectionist",
            "image": "/Perfectionist.png",
            "category": "best",
            "completion": True,
            # "description": "Get 100% on a mindmap"
        },
        {
            "id": "chicken_dinner", 
            "name": "Chicken dinner",
            "image": "/Chicken_dinner.png",
            "category": "best",
            "completion": True,
            # "description": "Win first place in a contest"
        },
        {
            "id": "one_take_wonder",
            "name": "One-Take Wonder", 
            "image": "/One_take_Wonder.png",
            "category": "best",
            "completion": True,
            # "description": "Complete a mindmap perfectly on first try"
        },

        # One step ahead achievements
        {
            "id": "mind_mapper",
            "name": "Mind Mapper",
            "image": "/Mind_Mapper.png", 
            "category": "neutral",
            "completion": False,
            # "description": "Create your first mindmap"
        },
        {
            "id": "brave_entry",
            "name": "Brave Entry",
            "image": "/Brave_Entry.png",
            "category": "neutral", 
            "completion": True,
            # "description": "Enter your first contest"
        },
        {
            "id": "creative_flow",
            "name": "Creative Flow",
            "image": "/Creative_Flow.png",
            "category": "neutral",
            "completion": False,
            # "description": "Create 5 mindmaps"
        },
        {
            "id": "first_step",
            "name": "First Step",
            "image": "/First_Step.png",
            "category": "neutral",
            "completion": True,
            # "description": "Complete your first mindmap"
        },
        {
            "id": "back_on_track",
            "name": "Back on Track",
            "image": "/Back_on_Track.png",
            "category": "neutral",
            "completion": True,
            # "description": "Resume learning after a break"
        },

        # Best of the worst achievements
        {
            "id": "epic_oops",
            "name": "Epic Oops",
            "image": "/Epic_Oops.png",
            "category": "worst",
            "completion": False,
            # "description": "Get 0% on a mindmap"
        },
        {
            "id": "better_luck",
            "name": "Better Luck Next Time",
            "image": "/Better_Luck_Next_Time.png",
            "category": "worst",
            "completion": False,
            # "description": "Fail a contest"
        },

        # Daily streak achievements
        {
            "id": "triple_flame",
            "name": "Triple Flame",
            "image": "/Triple_Flame.png",
            "category": "daily",
            "completion": False,
            # "description": "3 day streak"
        },
        {
            "id": "high_five",
            "name": "High Five Hustler",
            "image": "/High_Five_Hustler.png",
            "category": "daily",
            "completion": False,
            # "description": "5 day streak"
        },
        {
            "id": "tenacious",
            "name": "Tenacious Ten",
            "image": "/Tenacious_Ten.png",
            "category": "daily",
            "completion": False,
            # "description": "10 day streak"
        },
        {
            "id": "power_twenty",
            "name": "Power of Twenty",
            "image": "/Power_of_Twenty.png",
            "category": "daily",
            "completion": False,
            # "description": "20 day streak"
        },
        {
            "id": "thirty_titan",
            "name": "Thirty Day Titan",
            "image": "/Thirty_Day_Titan.png",
            "category": "daily",
            "completion": True,
            # "description": "30 day streak"
        }
    ]

    @rx.var
    def best_achievements(self) -> list[dict]:
        return [a for a in self.achievements if a["category"] == "best"]
    
    @rx.var
    def neutral_achievements(self) -> list[dict]:
        return [a for a in self.achievements if a["category"] == "neutral"]
    
    @rx.var 
    def worst_achievements(self) -> list[dict]:
        return [a for a in self.achievements if a["category"] == "worst"]
    
    @rx.var
    def daily_achievements(self) -> list[dict]:
        return [a for a in self.achievements if a["category"] == "daily"]
    
    @rx.var
    def completed_count(self) -> int:
        return len([a for a in self.achievements if a["completion"] == True])
    
    @rx.var 
    def user_level(self) -> str:
        if self.completed_count <= 5:
            return "Novice"
        elif self.completed_count <= 10:
            return "Competent"  
        elif self.completed_count <= 14:
            return "Master"
        else:
            return "Legend"
        
    @rx.var
    def level_image(self) -> str:
        if self.completed_count <= 5:
            return "/egg.png"
        elif self.completed_count <= 10:
            return "/eggChic.png"
        elif self.completed_count <= 14:
            return "/Chic.png"
        else:
            return "/chicOld.png"
        




#????? calendar page
#????? Calendar data use date that has login in form of like login_dates: list[dict]
#?????        |
#?????        |
#?????        |
#?????        |
#?????    \   |   /
#?????     \  |  /
#?????      \ | /
#?????       \|/
#?????        |

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