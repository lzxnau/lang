"""
Smart Platform Project: ForumScraper Module.

AI Searching Engine Package: Web Searching Engine.

Version: 2024.07.19.01
"""

import asyncio
import json

import httpx
from lang.aise.foruminfo import ForumConfig
from selectolax.lexbor import LexborHTMLParser as HTMLParser


class ForumScraper:
    """Forum Scraper class."""

    def __init__(self, cfg: ForumConfig):
        """Class initialization."""
        self.cfg = cfg
        self.client = httpx.AsyncClient()

    def cfg_init(self) -> bool:
        """Initialize ForumConfig login details."""
        print(f"Forum: {self.cfg.forum_name} User:{self.cfg.forum_user}")

        retry = 2
        for i in range(3):
            name = input("Please enter username: ").strip()
            if name:
                self.cfg.username = name
                break
            elif i == retry:
                return False

        for j in range(3):
            pwd = input("Please enter password: ").strip()
            if pwd:
                self.cfg.password = pwd
                break
            elif j == retry:
                return False

        return True

    async def fetch_login_page(self) -> str:
        """Fetch login page."""
        response = await self.client.get(
            self.cfg.forum_url, follow_redirects=True
        )
        response.raise_for_status()
        return response.text

    def parse_login_form(self, html):
        """Parse the login form and return the login form."""
        tree = HTMLParser(html)

        # Select the form with id
        form_id = self.cfg.login_form
        form = tree.css_first(f"form#{form_id}")

        # Extract form action URL
        action = form.attributes.get("action")

        # Extract form fields
        form_data = {}
        for input_tag in form.css("input"):
            name = input_tag.attributes.get("name")
            value = input_tag.attributes.get("value", "")
            if name:
                form_data[name] = value

        # Extracting the checkbox value
        if self.cfg.cookie_checkbox:
            checkbox = form.css_first(
                f"input[type='checkbox'][name={self.cfg.cookie_checkbox_name}]"
            )
            if checkbox:
                form_data[checkbox.attributes.get("name")] = (
                    checkbox.attributes.get("value")
                )

        # Add the select field value
        if self.cfg.login_sel:
            # select tag name
            sname = self.cfg.login_sel_name
            select_tag = form.css_first(f"select[name={sname}]")
            if select_tag:
                form_data[select_tag.attributes.get("name")] = (
                    select_tag.css_first("option").attributes.get("value")
                )

        return action, form_data

    async def submit_login_form(self, action, form_data) -> httpx.Response:
        """Submit login form."""
        login_url = self.cfg.forum_url + action

        form_data.update(
            {
                "username": self.cfg.username,
                "password": self.cfg.password,
            }
        )

        response = await self.client.post(
            login_url, data=form_data, follow_redirects=True
        )

        return response

    async def save_cookies(self) -> None:
        """Save cookies."""
        cookies = self.client.cookies.jar
        for cookie in cookies:
            print(cookie)

        cookie_dict = {
            cookie.domain: {cookie.name: cookie.value} for cookie in cookies
        }
        with open(self.cfg.cookie_file, "w") as f:
            json.dump(cookie_dict, f)

    async def load_cookies(self) -> bool:
        """Load cookies."""
        try:
            with open(self.cfg.cookie_file) as f:
                cookie_dict = json.load(f)
                for domain, cookies in cookie_dict.items():
                    for name, value in cookies.items():
                        self.client.cookies.set(name, value, domain=domain)
            return True
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError as jde:
            print(jde)
        except Exception as e:
            print(e)

        return False

    async def login(self) -> httpx.Response:
        """Login method."""
        login_page_html = await self.fetch_login_page()
        action, form_data = self.parse_login_form(login_page_html)
        response = await self.submit_login_form(action, form_data)
        await self.save_cookies()
        return response

    async def access_protected_page(
        self, path: str | None = None
    ) -> str | None:
        """Access protected page."""
        if not (self.cfg.cookie_pass and await self.load_cookies()):
            if not self.cfg_init():
                print("Enter login detail failed.")
                return None
            await self.login()

        protected_page_url = self.cfg.forum_url + self.cfg.base_path
        if path:
            protected_page_url += path
        response = await self.client.get(protected_page_url)
        print(type(response))
        try:
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as he:
            print(he)

        return None

    async def process(self) -> None:
        """Process main function for testing."""
        result = await self.access_protected_page()
        if result:
            print(result)


if __name__ == "__main__":
    from lang.aise.foruminfo import ForumList

    forum_name = "oursteps"
    fc = ForumList.get_forum_config(forum_name)
    if fc is None:
        print("Forum config not found.")
    else:
        fs = ForumScraper(fc)
        asyncio.run(fs.process())
