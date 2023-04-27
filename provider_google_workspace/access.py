from provider import target, access
from provider_google_workspace.provider import Provider
from provider_google_workspace.resources import Group


@access.target(kind="Group")
class GroupTarget:
    group = target.Resource(
        title="Group",
        description="The Google Workspace Group to grant access to",
        resource=Group,
    )


@access.grant()
def grant(p: Provider, subject: str, target: GroupTarget) -> access.GrantResult:
    # https://googleapis.github.io/google-api-python-client/docs/dyn/admin_directory_v1.members.html#insert
    res = (
        p.directory_v1.members()
        .insert(
            groupKey=target.group,
            body={"email": subject},
        )
        .execute()
    )

    print("created group member", "id", res.get("id"))


@access.revoke()
def revoke(p: Provider, subject: str, target: GroupTarget):
    p.directory_v1.members().delete(
        groupKey=target.group,
        memberKey=subject,
    ).execute()
