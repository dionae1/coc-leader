import coc
import os

from dotenv import load_dotenv

from core.database import Database
from ultils.exceptions import (
    ClanNotAssignedError,
    ClanNotFoundError,
    MemberNotFoundError,
)


class CoCService:
    def __init__(self, db: Database):
        self.coc_client = coc.Client()
        self.db = db

    async def login(self):
        load_dotenv()
        API_EMAIL = os.getenv("API_EMAIL")
        API_PASSWORD = os.getenv("API_PASSWORD")

        assert API_EMAIL is not None and API_PASSWORD is not None
        await self.coc_client.login(email=API_EMAIL, password=API_PASSWORD)

    async def get_clan(self, discord_id: int) -> coc.Clan:
        user = self.db.get_user(discord_id)
        if not user:
            raise ClanNotAssignedError()

        try:
            clan = await self.coc_client.get_clan(user[2])
            return clan

        except coc.errors.NotFound:
            raise ClanNotFoundError()

    async def get_current_war(self, discord_id: int) -> coc.ClanWar | None:
        user = self.db.get_user(discord_id)
        if not user:
            raise ClanNotAssignedError()

        try:
            war = await self.coc_client.get_clan_war(user[2])
            return war

        except Exception as e:
            print("Error fetching war data:", e)

    async def get_member(self, player_tag: str) -> coc.Player:
        try:
            member = await self.coc_client.get_player(player_tag)
            return member

        except coc.errors.NotFound:
            raise MemberNotFoundError()
