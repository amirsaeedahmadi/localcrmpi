import logging
from .user import UserService
from .company import CompanyService
from .service_request import ServiceRequestService
from .proforma import ProformaService
from .perssonel import PersonnelService

from utils.kafka import KafkaEventStore
from django.conf import settings


logger = logging.getLogger(__name__)
bootstrap_servers = settings.KAFKA_URL
kafka_event_store = KafkaEventStore(bootstrap_servers=bootstrap_servers)


user_service = UserService()
company_service = CompanyService(kafka_event_store)
service_request_service = ServiceRequestService(kafka_event_store)
proforma_service = ProformaService(kafka_event_store)
personnel_service = PersonnelService(kafka_event_store)
