from loguru import logger

from crunge import wgpu


def main():
    colorTargetStates = [wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)]
    
    logger.debug(colorTargetStates)
    logger.debug(colorTargetStates[0].format)
    logger.debug(colorTargetStates[0].format.value)

if __name__ == "__main__":
    main()