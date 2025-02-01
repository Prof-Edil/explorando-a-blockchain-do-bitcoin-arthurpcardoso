# How many new outputs were created by block 123,456?
bitcoin-cli getblock 0000000000002917ed80650c6174aac8dfc46f5fe36480aaef682ff6cd83c3ca 2 | jq '[.tx[].vout[]] | length'