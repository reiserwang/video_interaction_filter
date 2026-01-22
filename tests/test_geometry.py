import unittest
from utils.geometry import bboxes_overlap, get_bbox_center

class TestGeometry(unittest.TestCase):
    def test_bboxes_overlap(self):
        # [x1, y1, x2, y2]
        bb1 = [0, 0, 10, 10]
        bb2 = [5, 5, 15, 15]
        self.assertTrue(bboxes_overlap(bb1, bb2), "Should overlap")
        
        bb3 = [20, 20, 30, 30]
        self.assertFalse(bboxes_overlap(bb1, bb3), "Should not overlap")
        
        # Edge case: touching
        bb4 = [10, 0, 20, 10]
        # Depending on > vs >= logic. Code uses < and > so touching usually doesn't count or barely counts. 
        # Code: bb1[2] < bb2[0] => 10 < 10 is False. 
        # So it might return True (overlap) if they share an edge.
        # Let's check code: not (10 < 10 or 0 > 20 ...) -> not (False) -> True.
        # So touching is overlap.
        self.assertTrue(bboxes_overlap(bb1, bb4), "Touching should be overlap")

    def test_center(self):
        bb = [0, 0, 10, 10]
        self.assertEqual(get_bbox_center(bb), (5, 5))

if __name__ == '__main__':
    unittest.main()
