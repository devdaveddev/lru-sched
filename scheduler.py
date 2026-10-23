def _check(evs):
    for start, end in evs:
        if end <= start:
            raise ValueError("invalid event " + str((start, end)) + ": end must be after start")


def can_attend(evs):
    _check(evs)

    srt = sorted(evs)

    for a, b in zip(srt, srt[1:]):
        pe = a[1]
        cs = b[0]
        if cs < pe:
            return False
    return True


def min_rooms(evs):
    _check(evs)

    if not evs:
        return 0

    starts = sorted(start for start, _ in evs)
    ends = sorted(end for _, end in evs)

    active = 0
    peak = 0
    j = 0

    for start in starts:
        while j < len(ends) and ends[j] <= start:
            active -= 1
            j += 1

        active += 1
        peak = max(peak, active)

    return peak


def assign(evs):
    import heapq

    order = sorted(range(len(evs)), key=lambda i: evs[i])

    busy = []
    free = []
    nxt = 0
    out = [None] * len(evs)

    for i in order:
        start, end = evs[i]

        while busy and busy[0][0] <= start:
            heapq.heappush(free, heapq.heappop(busy)[1])

        if free:
            room = heapq.heappop(free)
        else:
            room = nxt
            nxt += 1

        heapq.heappush(busy, (end, room))
        name = chr(65 + room) if room < 26 else str(room)
        out[i] = "Room " + name

    return out


if __name__ == "__main__":
    assert can_attend([(9, 10), (10, 11), (11, 12)]) is True
    assert can_attend([(9, 11), (10, 12)]) is False
    assert can_attend([]) is True

    assert min_rooms([(9, 10), (10, 11), (11, 12)]) == 1
    assert min_rooms([(9, 11), (10, 12), (10, 13)]) == 3
    assert min_rooms([(1, 5), (2, 3), (4, 6)]) == 2
    assert min_rooms([]) == 0

    for bad in ([(5, 5)], [(9, 8)]):
        for func in (can_attend, min_rooms):
            try:
                func(bad)
                assert False, "should have raised ValueError"
            except ValueError:
                pass

    orig = [(11, 12), (9, 10), (10, 11)]
    min_rooms(orig)
    can_attend(orig)
    assert orig == [(11, 12), (9, 10), (10, 11)]

    samp = [(9, 12), (10, 11), (10, 13), (12, 14)]
    rooms = assign(samp)
    assert len(set(rooms)) == min_rooms(samp)
    assert rooms == ["Room A", "Room B", "Room C", "Room A"]

    print("Scheduler, checks passed")
