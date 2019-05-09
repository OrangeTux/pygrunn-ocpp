import asyncio
import websockets

from ocpp import call_result
from ocpp.ocpp_16_enums import Action, RegistrationStatus
from ocpp.ocpp_16_cs import on, after

from demo.duct_tape import ServerWebSocket as WebSocket
from demo.duct_tape import ChargePoint as cp


class ChargePoint(cp):

    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        """ Route BootNotification calls. """
        return call_result.BootNotificationPayload(
            current_time="",
            interval=30,
            status=RegistrationStatus.Accepted
        )


async def on_connect(websocket, path):
    """ Create ChargePoint and start processing requests. """
    cp = ChargePoint(websocket)

    await cp.start()


asyncio.get_event_loop().run_until_complete(
    websockets.serve(on_connect, '0.0.0.0', 9000,
        subprotocols=['ocpp1.6', 'dcms'], create_protocol=WebSocket))
asyncio.get_event_loop().run_forever()
