from cache import Cache


def test_example():
    cache = Cache(80)
    print('Insert 10BytesFile.txt')
    S1 = cache.get_file_content('files_for_tests/10BytesFile.txt')

    print('Insert 50BytesFile.txt')
    S2 = cache.get_file_content('files_for_tests/50BytesFile.txt')

    print('Insert 10BytesFile.txt')
    S3 = cache.get_file_content('files_for_tests/10BytesFile.txt')
    print('Insert 30BytesFile.txt - Exceed from available cache size. Remove 50KbFile')
    S4 = cache.get_file_content('files_for_tests/30BytesFile.txt')
    # Exceed from general cache size
    print('Insert 100BytesFile.txt which is bigger than cache size')
    S5 = cache.get_file_content('files_for_tests/100BytesFile.txt')

    print('Invalid file path (no file)')
    S0 = cache.get_file_content('files_for_tests/1000000BytesFile.txt')


def main():
    test_example()


if __name__ == '__main__':
    main()
