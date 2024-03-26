# Retrieve value K
def get_value(N, key_value_pairs, K):
    kv_dict = dict(key_value_pairs)
    return kv_dict[K]

N = int(input())
key_value_pairs = [input().split() for _ in range(N)]
K = input()

print(get_value(N, key_value_pairs, K))
