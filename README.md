# imap_backup
Make a recursive backup from an IMAP Account, generating EML's.

## Requisites

``` pip install argparse imaplip ```

## Use

>usage: mail.py [-h] -s HOST -u USERNAME -p PASSWORD [-r REMOTE_FOLDER] -l
               LOCAL_FOLDER [-sd START_DATE] [-ed END_DATE]
               [-d DELETE_DESTINATION]
