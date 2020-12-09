import logging
from io import BytesIO
import time
import pika
from pika.exceptions import AMQPConnectionError
from django.conf import settings
from pynetdicom import AE, evt, AllStoragePresentationContexts, debug_logger
from pydicom.filewriter import dcmwrite
from ..base.server_command import ServerCommand

FORCE_DEBUG_LOGGER = False

logger = logging.getLogger(__name__)


def on_connect(event):
    rabbit_url = settings.RABBITMQ_URL
    connection = None
    retries = 0
    while True:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(rabbit_url))
            break
        except AMQPConnectionError as err:
            retries += 1
            if retries <= 30:
                logger.error(
                    "Cannot connect to %s. Trying again in 2 seconds... (%d/30).",
                    rabbit_url,
                    retries,
                )
                time.sleep(2)
            else:
                logger.exception(
                    "Could not connect to %s. No more retries.", rabbit_url
                )
                raise err

    if connection and connection.is_open:
        logger.info("Connected to %s.", rabbit_url)
    else:
        raise AssertionError("No connection to RabbitMQ server established.")

    # We bind the RabbitMQ connection to assoc as this is the only object that is
    # shared between all events.
    event.assoc.rabbit_connection = connection


def on_close(event):
    connection = event.assoc.rabbit_connection
    if connection and connection.is_open:
        rabbit_url = settings.RABBITMQ_URL
        logger.info("Disconnected from %s.", rabbit_url)


# Implement a handler for evt.EVT_C_STORE
def handle_store(event):
    """Handle a C-STORE request event.

    The request is initiated with a C-MOVE request by ADIT itself to
    fetch images from a DICOM server that doesn't support C-GET requests.
    """
    ds = event.dataset
    ds.file_meta = event.file_meta

    called_ae = event.assoc.acceptor.primitive.called_ae_title
    called_ae = called_ae.decode("utf-8").strip()
    if called_ae != settings.ADIT_AE_TITLE:
        raise AssertionError(f"Invalid called AE title: {called_ae}")

    buffer = BytesIO()
    dcmwrite(buffer, ds, write_like_original=False)

    connection = event.assoc.rabbit_connection

    if not connection or not connection.is_open:
        raise AssertionError("No connection to RabbitMQ server established.")

    channel = connection.channel()
    channel.exchange_declare(exchange="received", exchange_type="direct")

    # Send the dataset to the workers using RabbitMQ
    calling_ae = event.assoc.remote["ae_title"].decode("utf-8").strip()
    routing_key = f"{calling_ae}\\{ds.StudyInstanceUID}\\{ds.SeriesInstanceUID}"
    properties = pika.BasicProperties(message_id=ds.SOPInstanceUID)
    channel.basic_publish(
        exchange="received_dicoms",
        routing_key=routing_key,
        properties=properties,
        body=buffer.getvalue(),
    )

    buffer.close()
    channel.close()

    return 0x0000  # Return a 'Success' status


class Command(ServerCommand):
    help = "Starts a C-STORE SCP for receiving DICOM files."

    server_name = "ADIT DICOM C-STORE SCP Receiver"
    default_port = 11112

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "--debug",
            action="store_true",
            help="Enable debug logger of pynetdicom.",
        )

    def run_server(self, **options):
        if options["debug"] or FORCE_DEBUG_LOGGER:
            debug_logger()

        ae = AE(ae_title=settings.ADIT_AE_TITLE)
        ae.supported_contexts = AllStoragePresentationContexts
        handlers = [
            (evt.EVT_CONN_OPEN, on_connect),
            (evt.EVT_CONN_CLOSE, on_close),
            (evt.EVT_C_STORE, handle_store),
        ]

        ae.start_server((self.addr, self.port), evt_handlers=handlers)
