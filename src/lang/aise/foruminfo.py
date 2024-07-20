"""
Smart Platform Project: Forum Information Module.

Version: 2024.07.20.01
"""

from pydantic import BaseModel, Field, computed_field


class ForumConfig(BaseModel):
    """Forum Config Model."""

    forum_name: str = Field(
        kw_only=True,
        description="The forum name",
        init_var=True,
        min_length=4,
        frozen=True,
    )
    forum_url: str = Field(
        kw_only=True,
        description="The forum url path for all requests",
        init_var=True,
        min_length=4,
        frozen=True,
    )
    forum_user: str = Field(
        kw_only=True,
        description="Alias of user account",
        init_var=True,
        min_length=4,
    )
    username: str = Field(
        kw_only=True,
        description="Alias for user account",
        init=False,
        default="None",
        min_length=4,
    )
    password: str = Field(
        kw_only=True,
        description="Password for user account",
        init=False,
        default="None",
        min_length=4,
    )
    cookie_pass: bool = Field(
        kw_only=True,
        description="Cookie supported",
        init_var=True,
        default=False,
        frozen=True,
    )
    cookie_load: bool = Field(
        kw_only=True,
        description="Cookie loading status",
        init=False,
        default=False,
    )
    cookie_checkbox: bool = Field(
        kw_only=True,
        description="Cookie enable checkbox",
        init_var=True,
        default=False,
        frozen=True,
    )
    cookie_checkbox_name: str = Field(
        kw_only=True,
        description="Cookie checkbox name",
        init_var=True,
        default="None",
        min_length=4,
        frozen=True,
    )
    login_form: str = Field(
        kw_only=True,
        description="Login form name",
        init_var=True,
        min_length=4,
        frozen=True,
    )
    login_sel: bool = Field(
        kw_only=True,
        description="Login saving cookie checkbox",
        init_var=True,
        default=False,
        frozen=True,
    )
    login_sel_name: str = Field(
        kw_only=True,
        description="Login saving cookie checkbox name",
        init_var=True,
        default="None",
        min_length=4,
        frozen=True,
    )
    base_path: str = Field(
        kw_only=True,
        description="Forum main request path",
        init_var=True,
        min_length=4,
        frozen=True,
    )

    @computed_field  # type: ignore[misc]
    @property
    def cookie_file(self) -> str:
        """Cookie file path."""
        return f"cfg/{self.forum_name}-{self.forum_user}-cookie.json"


class ForumList:
    """Forum List Class."""

    # Dict for forums
    Forum_Dict: dict[str, ForumConfig] = {
        "oursteps": ForumConfig(
            forum_name="oursteps",
            forum_url="https://www.oursteps.com.au/bbs/",
            forum_user="azhz",
            login_form="lsform",
            cookie_pass=True,
            cookie_checkbox=True,
            cookie_checkbox_name="cookietime",
            login_sel=True,
            login_sel_name="fastloginfield",
            base_path="forum.php",
        ),
    }

    Forum_Account_Dict: dict[str, list[str]] = {
        "oursteps": ["azhz"],
    }

    @classmethod
    def get_forum_config(cls, name: str, user: str = "") -> ForumConfig | None:
        """Get forum config method."""
        if name not in cls.Forum_Dict or name not in cls.Forum_Account_Dict:
            return None

        if not (user and user in cls.Forum_Account_Dict[name]):
            user = cls.Forum_Account_Dict[name][0]
        fc = cls.Forum_Dict[name]
        fc.forum_user = user
        return fc
