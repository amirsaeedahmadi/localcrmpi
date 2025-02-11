class PanelServiceRequestStatusChoices:
    CANCELED = 0
    CLOSED = 1
    DRAFT = 2
    SUBMITTED = 3
    INSPECTING = 4

    @classmethod
    @property
    def choices_map(cls):
        return dict(
            filter(
                lambda item: isinstance(item[1], int)
                and not str(item[0]).startswith("__"),
                cls.__dict__.items(),
            )
        )

    @classmethod
    @property
    def choices(cls):
        return list(cls.choices_map.values())


class CRMSalesStageChoices:
    Prospecting = "Prospecting"
    Qualification = "Qualification"
    Needs_Analysis = "Needs Analysis"
    Value_Proposition = "Value Proposition"
    Id_Decision_Makers = "Id. Decision Makers"
    Perception_Analysis = "Perception Analysis"
    Proposal_Price_Quote = "Proposal/Price Quote"
    Negotiation_Review = "Negotiation/Review"
    Closed_Won = "Closed Won"
    Closed_Lost = "Closed Lost"

    @classmethod
    @property
    def choices_map(cls):
        return dict(
            filter(
                lambda item: isinstance(item[1], str)
                and not str(item[0]).startswith("__"),
                cls.__dict__.items(),
            )
        )

    @classmethod
    @property
    def choices(cls):
        return list(cls.choices_map.values())
