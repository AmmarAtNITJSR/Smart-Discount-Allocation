import unittest
from discount_engine.allocator import allocate_discounts

class TestAllocation(unittest.TestCase):

    def test_normal_allocation(self):
        agents = [
            {"id": "X1", "performanceScore": 95, "seniorityMonths": 24, "targetAchievedPercent": 90, "activeClients": 15},
            {"id": "X2", "performanceScore": 60, "seniorityMonths": 12, "targetAchievedPercent": 50, "activeClients": 5},
            {"id": "X3", "performanceScore": 80, "seniorityMonths": 6,  "targetAchievedPercent": 70, "activeClients": 10}
        ]
        result = allocate_discounts(10000, agents, {})
        allocs = {a['id']: a['assignedDiscount'] for a in result['allocations']}
        self.assertEqual(sum(allocs.values()), 10000)
        self.assertTrue(allocs["X1"] > allocs["X2"] and allocs["X1"] > allocs["X3"])

    def test_all_same_allocation(self):
        agents = [{"id": f"Y{i}", "performanceScore": 50, "seniorityMonths": 10, "targetAchievedPercent": 50, "activeClients": 5} for i in range(3)]
        result = allocate_discounts(999, agents, {})
        allocs = [a['assignedDiscount'] for a in result['allocations']]
        self.assertTrue(max(allocs) - min(allocs) <= 1)
        self.assertTrue(sum(allocs) >= 998 and sum(allocs) <= 999)

    def test_rounding_and_thresholds(self):
        agents = [
            {"id": "Z1", "performanceScore": 1, "seniorityMonths": 1, "targetAchievedPercent": 1, "activeClients": 1},
            {"id": "Z2", "performanceScore": 0, "seniorityMonths": 0, "targetAchievedPercent": 0, "activeClients": 0}
        ]
        result = allocate_discounts(5, agents, {"min_allocation_percent": 0.2})
        allocs = {a['id']: a['assignedDiscount'] for a in result['allocations']}
        self.assertTrue(allocs["Z1"] >= 1 and allocs["Z2"] >= 1)
        self.assertEqual(allocs["Z1"] + allocs["Z2"], 5)

if __name__ == '__main__':
    unittest.main()
