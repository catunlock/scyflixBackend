#!/bin/bash

git clone https://github.com/tonikelope/megadown.git
chmod +x megadown/megadown
./megadown/megadown https://mega.nz/#\!pp9GGBoR\!Hyt0Lxhtvu5t1YcdpqeVPY48MgQLjtrkrBYHZWy5QBc
unzip computer_science_doc2vec.zip
rm -rf megadown
rm computer_science_doc2vec.zip
rm -rf .megadown