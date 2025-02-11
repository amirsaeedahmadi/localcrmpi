class Event:
    name = None
    topic = "Users"

    def __init__(self, data):
        self.data = data
        # key is used as message key
        self.key = str(self.get_key())

    def get_key(self):
        return self.data["id"]

    def __str__(self):
        return f"{self.name}: {self.data}"


class UserCreated(Event):
    name = "UserCreated"


class UserUpdated(Event):
    name = "UserUpdated"


class UserDeleted(Event):
    name = "UserDeleted"


class CompanyCreated(Event):
    name = "CompanyCreated"


class CompanyUpdated(Event):
    name = "CompanyUpdated"


class CompanyDeleted(Event):
    name = "CompanyDeleted"


class ProformaCreated(Event):
    name = "ProformaCreated"


class ProformaUpdated(Event):
    name = "ProformaUpdated"


class ProformaDeleted(Event):
    name = "ProformaDeleted"


class CRMProformaCreated(Event):
    name = "CRMProformaCreated"

    def get_key(self):
        return self.data["request"]


class ProformaFileCreated(Event):
    name = "ProformaFileCreated"


class ProformaFileUpdated(Event):
    name = "ProformaFileUpdated"


class ProformaFileDeleted(Event):
    name = "ProformaFileDeleted"


class ServiceRequestCreated(Event):
    name = "ServiceRequestCreated"


class ServiceRequestUpdated(Event):
    name = "ServiceRequestUpdated"


class ServiceRequestSubmitted(Event):
    name = "ServiceRequestSubmitted"


class ServiceRequestInspected(Event):
    name = "ServiceRequestInspected"


class ServiceRequestDrafted(Event):
    name = "ServiceRequestDrafted"


class ServiceRequestCanceled(Event):
    name = "ServiceRequestCanceled"
