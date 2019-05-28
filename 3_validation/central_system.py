import asyncio
import logging
import websockets

from ocpp.routing import on, after
from ocpp.v16 import call_result, ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

class ChargePoint(cp):

    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        """ Route BootNotification calls. """
        return call_result.BootNotificationPayload(
            current_time="",
            interval="30",
            status=RegistrationStatus.accepted
        )

    @after(Action.BootNotification)
    def after_boot_notification(self):
        log.info("After BootNotification")


async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']
    )

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
