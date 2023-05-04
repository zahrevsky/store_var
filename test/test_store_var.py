import unittest
from unittest.mock import mock_open, patch

from src.store_var import stored


class TestStored(unittest.TestCase):
    def test_initEmpty(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [])
        
        self.assertEqual(len(l), 0)
    
    def test_init_empty(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt')
        
        self.assertEqual(len(l), 0)
    
    def test_initOne(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [1])

        mock.assert_called_once_with('test.txt', 'wb')
        self.assertEqual(l, [1])
    
    def test_initMany(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [1, 2, 3])
        
        self.assertEqual(l, [1, 2, 3])
    
    def test_initMany_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [1, 2, 3])

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, [1, 2, 3])
    
    def test_append(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [1, 2, 3])
            l.append(4)
        
        self.assertEqual(l, [1, 2, 3, 4])
    
    def test_append_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [1, 2, 3])
            l.append(4)

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, [1, 2, 3, 4])
    
    def test_extend(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [1, 2, 3])
            l.extend([4, 5, 6])
        
        self.assertEqual(l, [1, 2, 3, 4, 5, 6])
    
    def test_extend_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [1, 2, 3])
            l.extend([4, 5, 6])

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, [1, 2, 3, 4, 5, 6])

    def test_insert(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [1, 2, 4])
            l.insert(2, 3)
        
        self.assertEqual(l, [1, 2, 3, 4])
    
    def test_insert_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [1, 2, 4])
            l.insert(2, 3)

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, [1, 2, 3, 4])
    
    def test_remove(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [0, 1, 2, 3, 4])
            l.remove(2)
        
        self.assertEqual(l, [0, 1, 3, 4])
    
    def test_remove_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [0, 1, 2, 3, 4])
            l.remove(2)

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, [0, 1, 3, 4])
    
    def test_pop(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [0, 1, 2, 3, 4])
            l.pop()
        
        self.assertEqual(l, [0, 1, 2, 3])
    
    def test_pop_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [0, 1, 2, 3, 4])
            l.pop()

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, [0, 1, 2, 3])
    
    def test_popIndex(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [0, 1, 2, 3, 4])
            l.pop(2)
        
        self.assertEqual(l, [0, 1, 3, 4])
    
    def test_popIndex_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [0, 1, 2, 3, 4])
            l.pop(2)

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, [0, 1, 3, 4])
    
    def test_clear(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [0, 1, 2, 3, 4])
            l.clear()
        
        self.assertEqual(l, [])
    
    def test_clear_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [0, 1, 2, 3, 4])
            l.clear()

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, [])
    
    def test_index(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [0, 1, 2, 3, 4])

        self.assertEqual(l.index(2), 2)
    
    def test_count(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', [0, 1, 2, 2, 3, 4])

        self.assertEqual(l.count(2), 2)
    
    def test_delitem(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', ['a', 'b', 'c', 'd', 'e'])
            del l[2]
        
        self.assertEqual(l, ['a', 'b', 'd', 'e'])
    
    def test_delitem_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', ['a', 'b', 'c', 'd', 'e'])
            del l[2]

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, ['a', 'b', 'd', 'e'])
    
    def test_setitem(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', ['a', 'b', 'c', 'd', 'e'])
            l[2] = 'C'
        
        self.assertEqual(l, ['a', 'b', 'C', 'd', 'e'])
    
    def test_setitem_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', ['a', 'b', 'c', 'd', 'e'])
            l[2] = 'C'

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, ['a', 'b', 'C', 'd', 'e'])
    
    def test_iadd(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', ['a', 'b'])
            l += ['c', 'd']
        
        self.assertEqual(l, ['a', 'b', 'c', 'd'])
    
    def test_iadd_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', ['a', 'b'])
            l += ['c', 'd']

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, ['a', 'b', 'c', 'd'])
    
    def test_imul(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', ['a'])
            l *= 3
        
        self.assertEqual(l, ['a', 'a', 'a'])
    
    def test_imul_andRead(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', ['a'])
            l *= 3

        mock2 = mock_open(read_data=written_last(mock))
        with patch('builtins.open', mock2):
            l2 = stored('test.txt')

        self.assertEqual(l2, ['a', 'a', 'a'])
    
    def test_repr(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt', ['a', 'b', 'c'])
        
        self.assertEqual(repr(l), "stored(['a', 'b', 'c'])")
    
    def test_repr_empty(self):
        mock = mock_open(read_data=b'')

        with patch('builtins.open', mock):
            l = stored('test.txt')
        
        self.assertEqual(repr(l), "stored([])")


def written_last(open_mock):
    return [
        call[1][0] 
        for call in open_mock.mock_calls 
        if call[0] == '().write'
    ][-1]
    

if __name__ == '__main__':
    unittest.main()
