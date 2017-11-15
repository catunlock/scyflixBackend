#!/bin/bash

git clone https://github.com/tonikelope/megadown.git
chmod +x megadown/megadown
./megadown/megadown https://mega.nz/#\!1hUkRbLB\!2kzWb-nXONmAOmQ-c-_xpGolyYYTPKMFQ_fWHHQrCRY
unzip computer_science_magpie.zip
rm -rf megadown
rm computer_science_magpie.zip
rm -rf .megadown