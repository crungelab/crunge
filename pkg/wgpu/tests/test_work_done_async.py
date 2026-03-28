from crunge import wgpu
from crunge.wgpu.utils import create_device
from loguru import logger

instance = wgpu.Instance()
print(instance)

async def main():
    # Create an instance
    instance = wgpu.Instance()

    async def pump():
        while True:
            instance.process_futures()
            await asyncio.sleep(0.001)

    pump_task = asyncio.create_task(pump())

    # Request an adapter
    options = wgpu.RequestAdapterOptions()
    adapter = await instance.request_adapter_async(options)

    print(adapter)

    device = create_device(adapter)

    queue = device.get_queue()
    logger.debug("Submitting work to the queue...")
    queue.submit([])
    logger.debug("Waiting for work to be done...")
    await queue.on_submitted_work_done_async(instance)
    logger.debug("Work is done!")

    pump_task.cancel()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())