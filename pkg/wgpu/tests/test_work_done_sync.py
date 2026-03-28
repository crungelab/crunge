from loguru import logger

from crunge import wgpu


def main():
    wgpu_context = wgpu.Context()
    device = wgpu_context.device
    queue = device.get_queue()
    logger.debug("Submitting work to the queue...")
    queue.submit([])
    logger.debug("Waiting for work to be done...")
    queue.on_submitted_work_done_sync(wgpu_context.instance)
    logger.debug("Work is done!")

if __name__ == "__main__":
    main()