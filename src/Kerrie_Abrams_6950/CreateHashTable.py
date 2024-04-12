class HashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=40):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Get bucket list where the item belongs
    def _get_bucket_list(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        return bucket_list

    # Inserts a new item into the hash table.
    def insert(self, key, item):
        # call _get_bucket_list to retrieve corresponding bucket list
        bucket_list = self._get_bucket_list(key)

        # update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # call _get_bucket_list to retrieve corresponding bucket list
        bucket_list = self._get_bucket_list(key)

        # search for the key in the bucket list
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # call _get_bucket_list to retrieve corresponding bucket list
        bucket_list = self._get_bucket_list(key)

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])

