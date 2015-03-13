from __future__ import division
from __future__ import print_function


class Server:
    def __init__(self, capacity, size):
        self.capacity = capacity
        self.size = size
        self.pool = None
        self.row = None
        self.score = capacity * capacity / size
        self.slot = None

    def add_to_pool(self, pool):
        pool.add(self)
        self.pool = pool

    def add_to_row(self, row):
        row.add(self)
        self.row = row

    def __repr__(self):
        return '{} {}'.format(self.capacity, self.size)


class Pool:
    def __init__(self, pool_num):
        self.pool_num = pool_num
        self.servers = []

    def add(self, server):
        self.servers.append(server)

    def calc_guaranteed_capacity(self):
        dic = {}
        total = 0
        for server in self.servers:
            if server.pool is self:
                row = server.row
                if row in dic:
                    dic[row] += server.capacity
                else:
                    dic[row] = server.capacity
                total += server.capacity

        guaranteed_capacity = total

        for key in dic.keys():
            row_capacity = dic[key]
            if total - row_capacity < guaranteed_capacity:
                guaranteed_capacity = total - row_capacity

        return guaranteed_capacity

    def __str__(self):
        return str(self.pool_num)


def find_worst_pool(pools):
    if len(pools) < 1:
        return None

    # initiate minimum capacity and minimum pool
    first_pool = pools[0]
    min_capacity = first_pool.calc_guaranteed_capacity()
    min_pool = first_pool
    # go through all the pools and compare them to the minimum
    for pool in pools:
        if pool.calc_guaranteed_capacity() < min_capacity:
            min_capacity = pool.calc_guaranteed_capacity()
            min_pool = pool

    return min_pool


class Row:
    def __init__(self, row_num, slots_num):
        self.row_num = row_num
        self.servers = []
        self.slots = [True] * slots_num

    def add(self, server):
        self.servers.append(server)

    def mark_unavailable(self, start, size):
        for i in range(start, start + size):
            self.slots[i] = False

    def get_available_slot(self, space):
        start = 0
        end = 0
        while end < len(self.slots):
            if self.slots[end]:
                if end - start + 1 >= space:
                    return start
                end += 1
            else:
                end += 1
                start = end
        return None

    def add_server(self, server):
        slot = self.get_available_slot(server.size)
        if slot is not None:
            server.slot = slot
            server.row = self
            self.mark_unavailable(slot, server.size)
            self.add(server)
            return True
        return False

    def __str__(self):
        return str(self.row_num)


def pools_sorted_by_guaranteed_capacity(pools):
    pools.sort(key=lambda pool: pool.calc_guaranteed_capacity())
    return pools


def sort_rows_by_pool_use(rows, pool):
    for row in rows:
        sum = 0
        for server in row.servers:
            if server in pool.servers:
                sum += server.capacity
        row.sum = sum
    rows.sort(key=lambda row: row.sum)


def servers_sorted_by_score(servers):
    return sorted(servers, key=lambda server: server.score, reverse=True)


def allocate_servers(servers, pools, rows):
    for server in servers_sorted_by_score(servers):
        pool = pools_sorted_by_guaranteed_capacity(pools)[0]
        server.add_to_pool(pool)

        sort_rows_by_pool_use(rows, pool)
        for row in rows:
            if row.add_server(server):
                break


def parse_input(path):
    with open(path) as fh:
        line = fh.readline()
        rows_num, slots_num, unavailable_slots_num, pools_num, servers_num = (int(i) for i in line.split())

        rows = [Row(row_num, slots_num) for row_num in range(rows_num)]
        servers = []

        for _ in range(unavailable_slots_num):
            line = fh.readline()
            row_num, slot_num = (int(i) for i in line.split())
            row = rows[row_num]
            row.mark_unavailable(slot_num, 1)

        for _ in range(servers_num):
            line = fh.readline()
            size, capacity = (int(i) for i in line.split())
            servers.append(Server(capacity, size))

    pools = [Pool(pool_num) for pool_num in range(pools_num)]

    return pools, rows, servers


def write_commands(servers, path_to_output):
    with open(path_to_output, "w") as fo:
        for server in servers:
            if server.row is None:
                fo.write("x\n")
            else:
                fo.write('{} {} {}\n'.format(server.row, server.slot, server.pool))


def main():
    # pools, rows, servers = parse_input('inputs/small.txt')
    pools, rows, servers = parse_input('inputs/large.txt')
    servers_orig_order = servers[:]

    allocate_servers(servers, pools, rows)

    write_commands(servers_orig_order, 'outputs/commands.txt')


if __name__ == '__main__':
    main()
