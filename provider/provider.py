from commonfate_provider import provider, args, resources
from google.oauth2 import service_account
import googleapiclient.discovery
import base64
import json


SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.group",
    "https://www.googleapis.com/auth/admin.directory.group.member",
]


class Provider(provider.Provider):
    customer_id = provider.String(usage="Google Workspace customer ID")
    admin_email = provider.String(
        usage="The email address of a Google Workspace directory administrator"
    )
    # to avoid any issues with multiline config variables, just take this as a Base64 encoded string.
    credentials_base64 = provider.String(
        usage="Google service account credentials in Base64-encoded JSON format",
        secret=True,
    )

    def __init__(self, config_loader={}):
        super().__init__(config_loader)

        # decode and load the JSON credentials from the supplied base64 format
        credentials_json = base64.b64decode(self.credentials_base64.get()).decode(
            "utf-8"
        )
        service_account_info = json.loads(credentials_json)

        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES
        )

        delegated_credentials = credentials.with_subject(self.admin_email.get())

        self.directory_v1 = googleapiclient.discovery.build(
            "admin", "directory_v1", credentials=delegated_credentials
        )


class Args(args.Args):
    group_id = args.String(title="Group")


@provider.grant()
def grant(p: Provider, subject, args: Args) -> provider.GrantResult:
    # https://googleapis.github.io/google-api-python-client/docs/dyn/admin_directory_v1.members.html#insert
    res = (
        p.directory_v1.members()
        .insert(
            groupKey=args.group_id,
            body={"email": subject},
        )
        .execute()
    )
    print("created group member", "id", res.get("id"))


@provider.revoke()
def revoke(p: Provider, subject, args: Args):
    p.directory_v1.members().delete(
        groupKey=args.group_id,
        memberKey=subject,
    ).execute()
