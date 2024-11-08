from pyfakefs.fake_filesystem_unittest import TestCase
import domain

# Test constants
LINE_1_WITH_KEYWORD = "line1 with keyword"
LINE_2_WITHOUT = "line2 without"
LINE_3_WITH = "line3 with KEYWORD"
SUBDIR = "subdir"
SUBDIR2 = "subdir2"
FILE_LOG = "file.log"
SUBDIR2_FILE_5 = f"/var/log/{SUBDIR}/{SUBDIR2}{FILE_LOG}.5"
SUBDIR2_FILE_5_CONTENTS = f"{SUBDIR2} {LINE_1_WITH_KEYWORD}\n{SUBDIR2} {LINE_2_WITHOUT}\n{SUBDIR2} {LINE_3_WITH}\n"


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        # setup the fake filesystem and 5 fake files.
        cls.fake_fs().create_file(
            f"/var/log/{FILE_LOG}",
            contents=f"{LINE_1_WITH_KEYWORD}\n{LINE_2_WITHOUT}\n{LINE_3_WITH}\n"
        )
        cls.fake_fs().create_file(
            f"/var/log/{FILE_LOG}.2",
            contents=f"2 {LINE_1_WITH_KEYWORD}\n2 {LINE_2_WITHOUT}\n2 {LINE_3_WITH}\n"
        )

        # create files in subdirectory
        cls.fake_fs().create_file(
            f"/var/log/{SUBDIR}/{FILE_LOG}.3",
            contents=f"{SUBDIR} {LINE_1_WITH_KEYWORD}\n{SUBDIR} {LINE_2_WITHOUT}\n{SUBDIR} {LINE_3_WITH}\n"
        )

        # create files in a deeper nested subdirectory
        cls.fake_fs().create_file(
            f"/var/log/{SUBDIR}/{SUBDIR2}{FILE_LOG}.4",
            contents=f"{SUBDIR2} {LINE_1_WITH_KEYWORD}\n{SUBDIR2} {LINE_2_WITHOUT}\n{SUBDIR2} {LINE_3_WITH}\n"
        )
        cls.fake_fs().create_file(
            SUBDIR2_FILE_5,
            contents=SUBDIR2_FILE_5_CONTENTS
        )

    def test_get_logs_one_file(self):
        res = domain.get_logs(filename=FILE_LOG, n=2, keyword="")
        expected = [LINE_3_WITH, LINE_2_WITHOUT]  # reverse list (not in place) and take first 2 items
        self.assertEqual(1, len(res))
        self.assertEqual(expected, res[0].logs)

    def test_get_logs_one_file_keyword_filter(self):
        res = domain.get_logs(filename=FILE_LOG, n=2, keyword="keyword")
        expected = [LINE_3_WITH, LINE_1_WITH_KEYWORD]
        self.assertEqual(1, len(res))
        self.assertEqual(expected, res[0].logs)

    def test_get_logs_one_file_no_filter_all_records(self):
        res = domain.get_logs(filename=FILE_LOG, n=100, keyword="")
        expected = [LINE_3_WITH, LINE_2_WITHOUT, LINE_1_WITH_KEYWORD]
        self.assertEqual(1, len(res))
        self.assertEqual(expected, res[0].logs)

    def test_get_logs_all_files_no_filter_all_records(self):
        res = domain.get_logs(filename="", n=100, keyword="")
        expected = [LINE_3_WITH, LINE_2_WITHOUT, LINE_1_WITH_KEYWORD]
        self.assertEqual(5, len(res))
        self.assertEqual(expected, res[0].logs)
        for file in res:
            if file.file_name == SUBDIR2_FILE_5:
                expected_list = SUBDIR2_FILE_5_CONTENTS.splitlines(keepends=False)
                expected_list.reverse()
                self.assertEqual(file.logs, expected_list)

    def test_get_logs_all_files_filter(self):
        res = domain.get_logs(filename="", n=2, keyword="keyword")
        expected = [LINE_3_WITH, LINE_1_WITH_KEYWORD]
        self.assertEqual(5, len(res))
        self.assertEqual(expected, res[0].logs)
        for file in res:
            if file.file_name == SUBDIR2_FILE_5:
                expected_list = SUBDIR2_FILE_5_CONTENTS.splitlines(keepends=False)
                expected_list.reverse()
                expected_list.pop(1)  # remove middle item
                self.assertEqual(file.logs, expected_list)
