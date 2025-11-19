import time

from core.use_cases.tests.flow.first_test_flow import FirstTestFlow
from utils.logs.logger import logger


def main():
    use_case: FirstTestFlow = FirstTestFlow()
    use_case.handle()


if __name__ == '__main__':
    logger.info("Iniciando processo de primeiros testes")
    START_TIME: float = time.time()
    STATUS: bool = True
    MESSAGE: None = None

    try:
        main()
    except Exception as e:
        logger.error(f"Erro no processo: {str(e)}", exc_info=True)
        STATUS: bool = False
        MESSAGE: str = str(e)

        raise Exception(MESSAGE) from e
    finally:
        ELAPSED_TIME: float = time.time() - START_TIME
        logger.info("Processing finished!")
        logger.info(f"Processing time: {ELAPSED_TIME:.2f} seconds")
