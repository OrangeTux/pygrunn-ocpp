import asyncio
import websockets
from structlog import get_logger

from ocpp import call
from ocpp.ocpp_16_enums import Action, RegistrationStatus

from demo.duct_tape import ClientWebSocket as WebSocket
from demo.duct_tape import ChargePoint as cp

log = get_logger()


class ChargePoint(cp):
    async def boot_notification(self):
        payload = call.BootNotificationPayload(
            charge_point_vendor="Alfen BV",
            charge_point_model="ICU Eve Mini",
            firmware_version=12345,
        )

        response = await self.call(payload)
        if response.status == RegistrationStatus.Accepted:
            log.info('Charge Point accepted!')


async def main():
    async with websockets.connect("ws://localhost:9000/PyGrunn-CP", create_protocol=WebSocket,
        compression=None,
        subprotocols=['ocpp1.6']) as ws:
        cp = ChargePoint(ws)

        await asyncio.gather(cp.boot_notification(), cp.start())


asyncio.run(main())

