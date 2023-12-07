from app.utility.base_world import BaseWorld
from plugins.profinet.app.profinet_gui import ProfinetGUI
from plugins.profinet.app.profinet_api import ProfinetAPI

name = 'Profinet'
description = 'The Profinet plugin for Caldera provides adversary emulation abilities specific to the Profinet protocol.'
address = '/plugin/profinet/gui'
access = BaseWorld.Access.RED


async def enable(services):
    app = services.get('app_svc').application
    profinet_gui = ProfinetGUI(services, name=name, description=description)
    app.router.add_static('/profinet', 'plugins/profinet/static/', append_version=True)
    app.router.add_route('GET', '/plugin/profinet/gui', profinet_gui.splash)

    profinet_api = ProfinetAPI(services)
    # Add API routes here
    app.router.add_route('POST', '/plugin/profinet/mirror', profinet_api.mirror)