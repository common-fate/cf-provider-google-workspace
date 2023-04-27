import typing
from .provider import Provider
from provider import resources, tasks


class Group(resources.Resource):
    description: str
    """
    An extended description to help users determine the purpose of a group. For example, you can include information about who should join the group, the types of messages to send to the group, links to FAQs about the group, or related groups. Maximum length is `4,096` characters.
    """

    admin_created: bool
    """
    Value is `true` if this group was created by an administrator rather than a user.
    """


@resources.loader
def load_groups(p: Provider):
    tasks.call(ListGroups())


class ListGroups(tasks.Task):
    page: typing.Optional[str] = None

    def run(self, p: Provider) -> None:
        res = (
            p.directory_v1.groups()
            .list(customer=p.customer_id.get(), pageToken=self.page)
            .execute()
        )
        for g in res["groups"]:
            resources.register(
                Group(
                    id=g["id"],
                    name=g["name"],
                    description=g["description"],
                    admin_created=g["adminCreated"],
                )
            )

        next_page = res.get("nextPageToken", "")
        if next_page != "":
            tasks.call(ListGroups(page=next_page))
