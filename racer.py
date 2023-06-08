from pracer.racer_client import RacerClient


def main():
    racer_client = RacerClient('192.168.56.1', 8088)
    racer_client.connect()
    racer_client.full_reset()
    result = racer_client.racer_read_file_('\"D:/Universitate/An_4/Licenta/Extractor/HelperFiles/a1.racer\"')
    print(result.value)
    result = racer_client.all_atomic_concepts_()
    print('CODE: ' + result.message_code)
    print('TYPE: ' + result.message_type)
    print('CONTENT: ' + result.message_content)
    result = racer_client.concept_instances_m("DATAMANAGEMENTFRAMEWORK")
    print(result)
    racer_client.disconnect()


def searchItem(item):
    racer_client = RacerClient('192.168.56.1', 8088)
    racer_client.connect()
    racer_client.full_reset()
    result = racer_client.racer_read_file_('\"D:/Universitate/An_4/Licenta/Extractor/HelperFiles/a1.racer\"')
    print(result.value)
    result = racer_client.all_atomic_concepts_()
    print('CODE: ' + result.message_code)
    print('TYPE: ' + result.message_type)
    print('CONTENT: ' + result.message_content)
    if item in result.message_content:
        return True
    return False


if __name__ == '__main__':
    main()
