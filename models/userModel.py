from pydantic import BaseModel


class UserModel(BaseModel):
    userId: int | None
    accountId: int | None
    conversationId: int | None
    accessToken: str | None
