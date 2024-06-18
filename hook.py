from app.utility.base_world import BaseWorld
from plugins.profinet.app.profinet_svc import ProfinetService

name = 'Profinet'
description = 'The Profinet plugin for Caldera provides adversary emulation abilities specific to the Profinet protocol.'
address = '/plugin/profinet/gui'
access = BaseWorld.Access.RED


async def enable(services):
    profinet_svc = ProfinetService(services, name, description)
    app = services.get('app_svc').application
    app.router.add_route('GET', '/plugin/profinet/gui', profinet_svc.splash)
    app.router.add_route('GET', '/plugin/profinet/data', profinet_svc.plugin_data)