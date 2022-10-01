import unittest

from rmidi.model.common.byte_block import ByteBlock

class ByteBlockTest(unittest.TestCase):
    def test_object(self):
        obj = ByteBlock(1, bytes(12))
        assert(True)

if __name__ == '__main__':
    unittest.main()
