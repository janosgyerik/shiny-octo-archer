from __future__ import division
from __future__ import print_function


class Server:
    def __init__(self, size, capacity):
        self.size = size
        self.capacity = capacity
        self.score = capacity * capacity / size
        self.pool = None
        self.row = None
        self.slot = None

    def add_to_pool(self, pool):
        pool.add_server(self)
        self.pool = pool

    def undo_add_to_pool(self):
        self.pool.undo_add_server()
        self.pool = None

    def __repr__(self):
        return '{} {}'.format(self.capacity, self.size)


class Pool:
    def __init__(self, pool_num):
        self.pool_num = pool_num
        self.servers = []

    def add_server(self, server):
        self.servers.append(server)

    def undo_add_server(self):
        self.servers = self.servers[:-1]

    def calc_guaranteed_capacity(self):
        row_capacities = {}
        total_capacity = 0
        for server in self.servers:
            row = server.row
            if row in row_capacities:
                row_capacities[row] += server.capacity
            else:
                row_capacities[row] = server.capacity
            total_capacity += server.capacity

        lowest_capacity = total_capacity

        for row_capacity in row_capacities.values():
            capacity_without_row = total_capacity - row_capacity
            if capacity_without_row < lowest_capacity:
                lowest_capacity = capacity_without_row

        return lowest_capacity

    def calc_row_capacities(self):
        row_capacities = {}
        for server in self.servers:
            row = server.row
            if row:
                if row in row_capacities:
                    row_capacities[row] += server.capacity
                else:
                    row_capacities[row] = server.capacity

        return [capacity for _, capacity in sorted(row_capacities.items(), key=lambda (x, _): x.row_num)]

    def __str__(self):
        return str(self.pool_num)


class Row:
    def __init__(self, row_num, slots_num):
        self.row_num = row_num
        self.slots = [True] * slots_num
        self.servers = []

    def mark_unavailable(self, start, size):
        self.slots[start:start + size] = [False for _ in range(size)]

    def get_available_slot(self, target_size):
        start = 0
        end = 0
        while end < len(self.slots):
            if self.slots[end]:
                if end - start + 1 == target_size:
                    return start
            else:
                start = end + 1
            end += 1

        return None

    def add_server(self, server):
        slot = self.get_available_slot(server.size)

        if slot is not None:
            server.slot = slot
            server.row = self
            self.mark_unavailable(slot, server.size)
            self.servers.append(server)
            return True

        return False

    def __str__(self):
        return str(self.row_num)


def sort_pools_by_guaranteed_capacity(pools):
    # not great to mutate in-place. would be better to return sorted(...)
    pools.sort(key=lambda pool: pool.calc_guaranteed_capacity())


def sort_rows_by_pool_use(rows, pool):
    pool_use = [sum([server.capacity for server in row.servers if server in pool.servers])
                for row in rows]
    pool_use_by_row = dict(zip(rows, pool_use))
    # not great to mutate in-place. would be better to return sorted(...)
    rows.sort(key=lambda x: pool_use_by_row[x])


def servers_sorted_by_score(servers):
    return sorted(servers, key=lambda server: server.score, reverse=True)


def allocate_servers(servers, pools, rows):
    for server in servers_sorted_by_score(servers):
        sort_pools_by_guaranteed_capacity(pools)
        pool = pools[0]
        server.add_to_pool(pool)

        sort_rows_by_pool_use(rows, pool)
        for row in rows:
            if row.add_server(server):
                break
        else:
            server.undo_add_to_pool()


def parse_input(path):
    with open(path) as fh:
        line = fh.readline()
        rows_num, slots_num, unavailable_slots_num, pools_num, servers_num = (int(x) for x in line.split())

        rows = [Row(row_num, slots_num) for row_num in range(rows_num)]
        servers = []

        for _ in range(unavailable_slots_num):
            line = fh.readline()
            row_num, slot_num = (int(x) for x in line.split())
            row = rows[row_num]
            row.mark_unavailable(slot_num, 1)

        for _ in range(servers_num):
            line = fh.readline()
            size, capacity = (int(x) for x in line.split())
            servers.append(Server(size, capacity))

    pools = [Pool(pool_num) for pool_num in range(pools_num)]

    return pools, rows, servers


def write_allocations(servers, path_to_output):
    with open(path_to_output, "w") as fo:
        for server in servers:
            if server.row is None:
                fo.write("x\n")
            else:
                fo.write('{} {} {}\n'.format(server.row, server.slot, server.pool))


def print_pool_stats(pools):
    for pool in pools:
        print('\t'.join([str(x) for x in [pool.pool_num] + pool.calc_row_capacities() + [pool.calc_guaranteed_capacity()]]))


def calc_min_guaranteed_capacity(pools):
    return min([pool.calc_guaranteed_capacity() for pool in pools])


def main():
    # pools, rows, servers = parse_input('inputs/small.txt')
    pools, rows, servers = parse_input('inputs/large.txt')
    servers_orig_order = servers[:]

    allocate_servers(servers, pools, rows)

    # print_pool_stats(pools)
    # print(calc_min_guaranteed_capacity(pools))

    write_allocations(servers_orig_order, 'outputs/commands.txt')


if __name__ == '__main__':
    main()
