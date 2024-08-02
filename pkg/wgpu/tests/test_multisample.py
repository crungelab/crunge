from loguru import logger

from crunge import wgpu
from crunge.wgpu import utils


def main():
    multisample = wgpu.MultisampleState(
        count=1,
        mask=0xFFFFFFFF,
        alpha_to_coverage_enabled=False,
    )

    logger.debug(multisample.count)
    logger.debug(hex(multisample.mask))
    logger.debug(multisample.alpha_to_coverage_enabled)

if __name__ == "__main__":
    main()