from client import client
from config import END_BLOCK, SNAPSHOT_CSV


def load_snapshot():

    accounts = {}
    f = open(SNAPSHOT_CSV)
    for line in f.readlines():
        line = line.strip().replace('"', '').split(',')
        accounts[line[0]] = float(line[2])
    f.close()
    return accounts


def validate_unreg():
    accounts = load_snapshot()
    f = open('onchain_snapshot_unregistered.csv', 'w')
    all_actions = []
    total_value_1 = total_value_2 = 0
    total_accounts = 0
    for i in range(0, END_BLOCK):
        block = client.get_block(i+1)
        txs = block['transactions']
        print('%d fetching blocks, be patient' % (i+1))
        if len(txs):
            for tx in txs:
                actions = tx['trx']['transaction']['actions']
                all_actions.extend(actions)
                if total_accounts > 0:
                    print('%d account(s) verified!' % total_accounts)
                key = ''
                for action in actions:
                    if action['name'] == 'add' and action['account'] == 'eosio.unregd':
                        data = action['data']
                        key = data['ethereum_address']
                        balance = float(data['balance'].replace(' EOS', ''))
                        assert accounts[key] == balance
                        line = ",".join([key, str(balance)]) + '\n';
                        total_value_1 += balance
                        f.write(line)
                        total_accounts += 1
                    elif action['name'] == 'transfer' and action['data']['to'] == 'eosio.unregd':
                        data = action['data']
                        balance = float(data['quantity'].replace('EOS', ''))
                        total_value_2 += balance
                        assert accounts[key] == balance
    f.close()
    assert sum(accounts.values()) == total_value_1
    assert sum(accounts.values()) == total_value_1
    assert len(accounts.keys()) == total_accounts
    print("=======================================")
    print("validation of total value SUCCESS!!!")
    print("total value on chain", total_value_1)
    print("total value in snapshot", sum(accounts.values()))
    print("\n")
    print("=======================================")
    print("validation of total accounts SUCCESS!!!")
    print("total accounts on chain", total_accounts)
    print("total accounts in snapshot", len(accounts.keys()))
    print("onchain_snapshot_unregistered.csv generated!")

if __name__ == "__main__":
    validate_unreg()
