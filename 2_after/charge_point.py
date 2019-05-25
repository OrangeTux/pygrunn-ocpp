import asyncio
import logging
import websockets

from ocpp.v16 import call, ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class ChargePoint(cp):
    async def boot_notification(self):
        payload = call.BootNotificationPayload(
            charge_point_vendor="Alfen BV",
            charge_point_model="ICU Eve Mini",
            firmware_version="#1:3.4.0-2990#N:217H;1.0-223",
        )

        response = await self.call(payload)
        if response.status == RegistrationStatus.accepted:
            log.info('Charge Point accepted!')


async def main():
    async with websockets.connect(
        'ws://localhost:9000/CP_1',
         subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('CP_1', ws)

        await asyncio.gather(cp.start(), cp.boot_notification())


if __name__ == '__main__':
    asyncio.run(main())
