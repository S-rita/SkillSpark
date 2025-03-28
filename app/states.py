import reflex as rx
import httpx

class LoginState(rx.State):
    username: str = ""
    password: str = ""
    login_error: str = ""
    is_logged_in: bool = False
    user_id: str = ""
    
    async def handle_login(self):
        try:
            if not self.username or not self.password:
                self.login_error = "Please enter both username and password"
                return

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/login",
                    json={"username": self.username, "password": self.password}
                )

                if response.status_code == 200:
                    result = response.json()
                    
                    # Update state
                    self.login_error = ""
                    self.is_logged_in = True
                    self.user_id = result.get("user_id", "")
                    
                    # Use yield instead of return for Reflex state updates
                    yield rx.window_alert("Login successful!")
                    yield rx.redirect("/main")  # Redirect properly
                else:
                    # Handle login error
                    result = response.json()
                    self.login_error = result.get("detail", "Invalid username or password")

        except Exception as e:
            self.login_error = f"An error occurred: {str(e)}"

    
    def check_login(self):
        """Verify login status when components initialize."""
        return self.is_logged_in
    
    def logout(self):
        """Handle user logout."""
        self.is_logged_in = False
        self.username = ""
        self.password = ""
        self.user_id = ""
        return rx.redirect("/")
    
class SignupState(rx.State):
    username: str = ""
    password: str = ""
    email: str = ""
    signup_error: str = ""
    is_signed_up: bool = False
    user_id: str = ""

    async def handle_signup(self):
        try:
            if not self.username or not self.password or not self.email:
                self.signup_error = "Please fill in all fields"
                return

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/signup",
                    json={"username": self.username, "password": self.password, "email": self.email}
                )

                if response.status_code == 200:
                    result = response.json()

                    # Update both SignupState and LoginState
                    self.signup_error = ""
                    self.is_signed_up = True

                    # Automatically log in the user after successful signup
                    LoginState.is_logged_in = True
                    LoginState.user_id = result.get("user_id", "")
                    LoginState.username = self.username  # Optional

                    yield rx.window_alert("Signup successful!")
                    yield rx.redirect("/main")  # Redirect properly
                else:
                    result = response.json()
                    self.signup_error = result.get("detail", "Signup failed")

        except Exception as e:
            self.signup_error = f"An error occurred: {str(e)}"    
