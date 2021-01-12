


class MultiKey:
    """MultiKey table is a table design for holding long format actuarial tables.
    Files are parsed from csv files, with the last column becoming the value,
    and the remaining columns forming the key

    Source format:
    key1,key2,key3,keyN,value
    """
    def infer_type(self, val):
        constructors = [int, float, str]
        for c in constructors:
            try:
                return c(val)
            except ValueError:
                pass
        return val

    def __init__(self, filename, convert=True):
        self.from_csv(filename, convert)
    
    def get(self, **keys):
        """get value, with validation of keys.  This is around 1/5 of the speed of __getitem__"""
        try:
            tuple_keys = tuple(keys[field] for field in self.field_names)
            return self.data[tuple_keys]
        except KeyError:
            keys_passed = list(keys.keys())
            compare = f"Error: Keys Passed: {keys_passed} Fields: {self.field_names}"
            raise KeyError(compare)

    def __getitem__(self, keys):
        return self.data[keys]

    def r(self, keys):
        return self.data[keys]

    def __len__(self):
        return len(self.data)
    
    def __repr__(self):
        return f"<MultiKey fields:{self.field_names} items:{len(self)}>"

    def from_csv(self, filename, convert=True):
        with open(filename, "r") as csv_file:
            self.header = csv_file.readline().strip().split(",")
            self.field_names = self.header[0:-1]
            self.value_name = self.header[-1]
            self.data = {}
            for raw_row in csv_file.readlines():
                row = raw_row.strip().split(",")
                keys = tuple(row[0:-1])
                value = row[-1]
                if convert:
                    keys = tuple(self.infer_type(k) for k in keys)
                    value = self.infer_type(value)
                self.data[keys] = value

# various functions to test timings (use %timeit test1() at ipython/jupyter REPL

def test1():
    t = 0
    for i in range(100):
        t += mk.get(table_name='abc1234', age=50, sex='m')
    return t

def test2():
    t = 0
    for i in range(100):
        t += mk['abc1234', 50, 'm']
    return t

def test3():
    t = 0
    for i in range(100):
        t += mk.data['abc1234', 50, 'm']
    return t

def test4():
    t = 0
    for i in range(100):
        t += mk.r('abc1234', 50, 'm')
    return t


if __name__ == "__main__":
    mk = MultiKey(r"test/test.csv")
    print(mk.data)
    print(mk.get(table_name='abc1234', age=50, sex='m'))
    print(mk.get(age=50, table_name='abc1234', sex='m'))
    print(mk['abc1234', 50, 'm'])
    print(mk)

