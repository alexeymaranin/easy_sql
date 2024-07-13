from base_models import BaseModel


class Account(BaseModel):
    component = '7c851aad-118c-4193-b93c-0db5688b26e1'
    fields = ["Id", "BonusAccount", "EmailUser", "MainAccount", "PremiumAccount", "PromotionalAccount", "UserCatalog"]
    pk = "Id"


class Shares(BaseModel):
    component = '1047e42c-6a3b-416c-82a1-2d55ab984d32'
    fields = ["Id", "OnClearanceShares", "EmailUser", "OwnedShares", "ReservedShares", "UserCatalog"]
    pk = "Id"


class User(BaseModel):
    component = '83e6ce3f-1211-4183-905c-29a3e1dcf468'
    fields = ["Id", "FirstName", "LastName", "PhoneNumber", "AccountCatalog", "DateJoined", "Email", "Gender", "Inviter", "InviterDate", "InviterUserCatalog", "Status", "UserExtra", "SharesCatalog"]
    pk = "Email"
    fk = ((Account, "AccountCatalog"), (Shares, "SharesCatalog"))
