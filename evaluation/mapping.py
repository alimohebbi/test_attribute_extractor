from typing import List, Tuple, Dict
from Levenshtein import distance

class Mapping:
    src_app: str
    tgt_app: str
    src_size: int
    gt_size: int
    gen_size: int

    src_gt: Dict[int, List[int]]
    gt_gen: Dict[int, List[int]]

    def __init__(
            self,
            src_app: str,
            tgt_app: str,
            src_size: int,
            gt_size: int,
            gen_size: int
    ):
        self.src_app = src_app
        self.tgt_app = tgt_app
        self.src_size = src_size
        self.gt_size = gt_size
        self.gen_size = gen_size
        self.src_gt = {}
        self.gt_gen = {}

    def add_src_gt(self, src: int, gt: int):
        if src not in self.src_gt:
            self.src_gt[src] = []
        self.src_gt[src].append(gt)

    def add_gt_gen(self, gt: int, gen: int):
        if gt not in self.gt_gen:
            self.gt_gen[gt] = []
        self.gt_gen[gt].append(gen)
        # self._extract_one_to_one_gt_gen()

    # transitives
    def true_positive(self) -> int:
        return self._num_transitives()

    # src_size - (src_gt pairs)
    def true_negative(self) -> int:
        count = self.src_size
        for val in self.src_gt.values():
            count -= len(val)
        return count

    # gen_size - (gen_gt pairs)
    def false_positive(self) -> int:
        gen_size = self.gen_size
        gen_gt_pairs = self._num_gt_gen_distinct_pairs()
        return gen_size - gen_gt_pairs

    # (src_gt pairs) - transitives
    def false_negative(self) -> int:
        count = 0
        for val in self.src_gt.values():
            count += len(val)

        return count - self._num_transitives()

    def levenshtein_distance(self) -> int:
        char_mapping = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z', 26: 'A', 27: 'B', 28: 'C', 29: 'D', 30: 'E', 31: 'F', 32: 'G', 33: 'H', 34: 'I', 35: 'J', 36: 'K', 37: 'L', 38: 'M', 39: 'N', 40: 'O', 41: 'P', 42: 'Q', 43: 'R', 44: 'S', 45: 'T', 46: 'U', 47: 'V', 48: 'W', 49: 'X', 50: 'Y', 51: 'Z'}
        gt_str = ""
        gen_str = ["$"] * self.gen_size
        for i in range(self.gt_size):
            gt_str += char_mapping[i]

        for key, val in self.gt_gen.items():
            for gen_idx in val:
                gen_str[gen_idx] = gt_str[key]

        return distance(gt_str, ''.join(gen_str))


    def _num_transitives(self) -> int:
        count = 0
        for val in self.src_gt.values():
            for gt in val:
                if gt in self.gt_gen:
                    count += len(self.gt_gen[gt])
        return count

    def _num_gt_gen_distinct_pairs(self) -> int:
        count = 0
        removed = set()
        for val in self.gt_gen.values():
            for gen in val:
                if gen in removed:
                    continue
                count += 1
                removed.add(gen)
                break
        return count

    def extract_one_to_one_gt_gen(self):
        removed = set()
        for key, val in self.gt_gen.items():
            val = [x for x in val if x not in removed]
            if len(val) != 0:
                removed.add(val[0])
                self.gt_gen[key] = [val[0]]
            else:
                self.gt_gen[key] = []

    @staticmethod
    def id(src_app: str, tgt_app: str) -> str:
        return f"{src_app}_{tgt_app}"

    def __str__(self):
        return f"{self.src_app}_{self.tgt_app}"
