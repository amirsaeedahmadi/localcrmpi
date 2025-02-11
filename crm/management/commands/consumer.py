import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from django.conf import settings
from utils.kafka import create_consumer
from crm.services import (
    user_service,
    company_service,
    service_request_service,
    proforma_service,
)

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    help = "Starts consuming events and tasks."

    TOPICS = ["Users", "Orders"]

    CALLBACKS = {
        "UserCreated": lambda body: user_service.create_user(**body),
        "UserUpdated": lambda body: user_service.update_user(**body),
        "UserDeleted": lambda body: user_service.delete_user(**body),
        "CompanyCreated": lambda body: company_service.create_company(**body),
        "CompanyUpdated": lambda body: company_service.update_company(**body),
        "CompanyDeleted": lambda body: company_service.delete_company(**body),
        "ServiceRequestCreated": lambda body: service_request_service.create_service_request(
            **body
        ),
        "ServiceRequestUpdated": lambda body: service_request_service.update_service_request(
            **body
        ),
        "ServiceRequestSubmitted": lambda body: service_request_service.update_service_request(
            **body
        ),
        "ServiceRequestDrafted": lambda body: service_request_service.update_service_request(
            **body
        ),
        "ServiceRequestCanceled": lambda body: service_request_service.update_service_request(
            **body
        ),  # TODO Correct
        "ServiceRequestInspected": lambda body: service_request_service.update_service_request(
            **body
        ),
        "CRMProformaCreated": lambda body: proforma_service.on_crm_proforma_created(
            **body
        ),
    }

    def on_message(self, message):
        tp = message.value["type"]
        callback = self.CALLBACKS.get(tp)
        if callback:
            body = message.value["payload"]
            callback(body)

    def handle(self, *args, **options):
        bootstrap_servers = settings.KAFKA_URL
        logger.info("Connecting to Kafka...")
        # Create Kafka consumer
        consumer = create_consumer(bootstrap_servers, "crmapi", self.TOPICS)
        consumer.start_consuming(on_message=self.on_message)
