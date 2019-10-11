class TestFolder:
    def test_is_empty_true_when_empty(self, created_folder):
        assert created_folder.is_empty

    def test_is_empty_false_when_populated(self, created_folder):
        with open(f'{created_folder.path}/test.txt', 'w') as file:
            file.write('')
        assert not created_folder.is_empty