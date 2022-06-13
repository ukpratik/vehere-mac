
class ZAlgorithm:

    def __init__(self, pattern, text):
        self.pattern = pattern
        self.text = text
        # we have to concatenate the pattern and the text
        self.S = pattern + text
        # int table for the Z values
        self.Z = [0 for _ in range(len(self.S))]

    def construct_z_table(self):

        # the first item (index 0) is the length of the S
        self.Z[0] = len(self.S)

        # the first and last items in the Z box
        left = 0
        right = 0

        # consider all the letters of the S string (starting with index 1)
        for k in range(1, len(self.S)):
            # we are not within a Z box (naive approach) CASE I
            if k > right:

                n = 0

                while n+k < len(self.S) and self.S[n] == self.S[n+k]:
                    n = n + 1

                self.Z[k] = n

                if n > 0:
                    left = k
                    right = k + n - 1
            else:
                # we are inside a Z box so maybe we can copy the values
                p = k - left
                # case II when we can copy the values of Z
                if self.Z[p] < right - k + 1:
                    self.Z[k] = self.Z[p]
                else:
                    # we can not copy the values (case III)
                    i = right + 1

                    while i < len(self.S) and self.S[i] == self.S[i - k]:
                        i = i + 1

                    self.Z[k] = i - k
                    left = k
                    right = i - 1

    def search(self):

        self.construct_z_table()

        # we just have to consider the values in the Z table in O(N+M)
        for i in range(1, len(self.Z)):
            if self.Z[i] >= len(self.pattern):
                print("Match found at index %s" % (i - len(self.pattern)))


if __name__ == "__main__":

    algorithm = ZAlgorithm('aabza', 'abzcaabzaabza')
    algorithm.search()
