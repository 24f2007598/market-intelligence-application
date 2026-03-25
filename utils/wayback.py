import requests

def get_snapshots(url, limit=3):
    cdx_api = f"http://web.archive.org/cdx/search/cdx?url={url}&output=json&limit={limit}"

    try:
        res = requests.get(cdx_api).json()

        if len(res) <= 1:
            return []

        snapshots = []
        for row in res[1:]:
            timestamp = row[1]
            snapshots.append(f"https://web.archive.org/web/{timestamp}/{url}")

        return snapshots

    except Exception as e:
        print(f"[Wayback ERROR] {url} -> {e}")
        return []

# def get_snapshots(url):
#     api = f"https://archive.org/wayback/available?url={url}"

#     try:
#         res = requests.get(api).json()

#         snapshots = res.get("archived_snapshots", {})

#         if "closest" in snapshots:
#             return [snapshots["closest"]["url"]]

#         return []

#     except Exception as e:
#         print(f"[Wayback ERROR] {url} -> {e}")
#         return []