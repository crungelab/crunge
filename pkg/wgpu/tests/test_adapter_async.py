from crunge import wgpu

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

    pump_task.cancel()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())