class ClanNotFoundError(Exception):
    """Exception raised when a clan is not found."""

    def __init__(self):
        super().__init__("Clan not found.")


class ClanNotAssignedError(Exception):
    """Exception raised when a clan is not assigned."""

    def __init__(self):
        super().__init__("Clan not assigned.")


class MemberNotFoundError(Exception):
    """Exception raised when a member is not found in the clan."""

    def __init__(self):
        super().__init__("Member not found in the clan.")
