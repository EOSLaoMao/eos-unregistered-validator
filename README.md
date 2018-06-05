## Verify Unregistered eosio balance


### 1. clone this project and install requirements

```
pip install requirements.txt
```

### 2. config the following params in `config.py`

```
# block chain http end point
HTTP_ENDPOINT = ""

# the block height to end register(after `eosio` resign)
END_BLOCK = 4550

# the snapshot used to verify unregistered, use the final/2 version: https://raw.githubusercontent.com/eosauthority/genesis/master/snapshot-files/final/2/snapshot_unregistered.csv
SNAPSHOT_CSV = "snapshot_unregistered.csv"
```


### 3. run validation

```
python validator.py
```

If any mismatch happened, verification process will abort.
