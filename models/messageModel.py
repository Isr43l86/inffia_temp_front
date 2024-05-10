from pydantic import BaseModel


class MessageModel(BaseModel):
    userId: int | None
    accountId: int | None
    conversationId: int | None
    accessToken: str | None
