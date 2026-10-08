import random
import musicbrainzngs as mb

mb.set_useragent("random-release-ids", "0.1", "you@example.com")

MAX_OFFSET = 2_000  # conservative; raise it once you know what works


def random_release_ids(n: int, **search) -> list[str]:
    total = mb.search_releases(limit=1, **search)["release-count"]
    if total == 0:
        raise RuntimeError(f"No results for {search!r}")

    max_page = max(0, (min(total, MAX_OFFSET) - 100) // 100)
    pages = list(range(max_page + 1))
    random.shuffle(pages)

    found: set[str] = set()
    for page in pages:
        try:
            res = mb.search_releases(limit=100, offset=page * 100, **search)
        except mb.ResponseError as e:
            print(f"offset {page * 100} failed: {e}")
            continue
        found.update(r["id"] for r in res["release-list"])
        if len(found) >= n:
            break

    ids = list(found)
    random.shuffle(ids)
    return ids[:n]


if __name__ == "__main__":
    f = open("assets/release-ids.txt", "w")
    ids = random_release_ids(500, format="CD")
    print(len(ids))
    for rid in ids:
        f.write(rid + "\n")